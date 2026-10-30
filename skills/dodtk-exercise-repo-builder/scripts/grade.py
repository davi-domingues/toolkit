#!/usr/bin/env python3
"""
grade.py - runner de autograding agnostico (stdlib apenas, Python 3.8+).

Le um arquivo no formato do GitHub Classroom (`.github/classroom/autograding.json`),
executa cada teste (setup + run), compara saida/exit code e calcula a nota.
Funciona localmente (Windows/Linux/macOS) e em qualquer CI.

Formato de cada teste:
  {
    "name": "1.1. GET /recurso - lista itens",   # obrigatorio, unico
    "setup": "",                                 # comando opcional executado antes do run
    "run": "./mvnw -q test -Dtest='X#y'",        # obrigatorio
    "input": "",                                 # stdin opcional para o run
    "output": "",                                # se vazio: passa se exit code == 0
    "comparison": "included",                    # exact | included | regex (usado se output != "")
    "timeout": 10,                               # minutos (compativel com Classroom)
    "points": 1,                                 # inteiro >= 0
    "required": false                            # extensao: se true e falhar, nota final = 0
  }

Uso:
  python grade.py                       # roda tudo (procura o autograding.json a partir do cwd)
  python grade.py --list                # lista testes e pontos
  python grade.py --validate            # valida o arquivo e sai
  python grade.py -k "POST"             # filtra testes por regex no nome
  python grade.py --junit report.xml    # gera relatorio JUnit (GitLab/Jenkins/etc.)
  python grade.py --json result.json    # gera resumo em JSON
  python grade.py --fail-under 70       # exit 0 se nota >= 70%
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from xml.etree import ElementTree as ET

CONFIG_CANDIDATES = (
    ".github/classroom/autograding.json",
    "autograding.json",
    ".grading/autograding.json",
)
VALID_COMPARISONS = {"exact", "included", "regex"}
REQUIRED_FIELDS = ("name", "run")

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------


def find_config(start: Path) -> Optional[Path]:
    """Procura o autograding.json subindo a partir de `start`."""
    for base in [start, *start.parents]:
        for rel in CONFIG_CANDIDATES:
            p = base / rel
            if p.is_file():
                return p
    return None


def repo_root_for(config_path: Path) -> Path:
    """Diretorio onde os comandos rodam (raiz do repo)."""
    parts = config_path.resolve().parts
    if len(parts) >= 3 and parts[-3:-1] == (".github", "classroom"):
        return config_path.resolve().parents[2]
    if config_path.parent.name == ".grading":
        return config_path.resolve().parents[1]
    return config_path.resolve().parent


def load_config(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8-sig") as fh:
        return json.load(fh)


def validate_config(cfg: Any) -> Tuple[List[str], List[str]]:
    """Retorna (erros, avisos)."""
    errors: List[str] = []
    warnings: List[str] = []
    if not isinstance(cfg, dict) or not isinstance(cfg.get("tests"), list):
        return ["raiz deve ser um objeto com a lista 'tests'"], warnings
    tests = cfg["tests"]
    if not tests:
        errors.append("'tests' esta vazio")
    seen = set()
    for i, t in enumerate(tests):
        where = f"tests[{i}]"
        if not isinstance(t, dict):
            errors.append(f"{where}: deve ser objeto")
            continue
        for f in REQUIRED_FIELDS:
            if not str(t.get(f, "")).strip():
                errors.append(f"{where}: campo obrigatorio '{f}' vazio")
        name = str(t.get("name", ""))
        if name in seen:
            errors.append(f"{where}: nome duplicado '{name}'")
        seen.add(name)
        cmp_ = t.get("comparison", "included")
        if cmp_ not in VALID_COMPARISONS:
            errors.append(f"{where}: comparison '{cmp_}' invalido (use {sorted(VALID_COMPARISONS)})")
        pts = t.get("points", 0)
        if not isinstance(pts, int) or pts < 0:
            errors.append(f"{where}: points deve ser inteiro >= 0")
        to = t.get("timeout", 10)
        if not isinstance(to, (int, float)) or to <= 0:
            errors.append(f"{where}: timeout deve ser numero > 0 (minutos)")
        if cmp_ == "regex" and t.get("output"):
            try:
                re.compile(t["output"])
            except re.error as e:
                errors.append(f"{where}: regex invalida em output: {e}")
        if "TODO" in name or "TODO" in str(t.get("run", "")):
            warnings.append(f"{where}: contem 'TODO' (placeholder nao substituido?)")
        m = re.search(r"\[(\d+)\s*pts?\]", name)
        if m and int(m.group(1)) != pts:
            warnings.append(f"{where}: nome diz [{m.group(1)}pt] mas points={pts}")
    return errors, warnings


# ---------------------------------------------------------------------------
# Shell
# ---------------------------------------------------------------------------


def _git_bash_windows() -> Optional[str]:
    candidates: List[Path] = []
    git = shutil.which("git")
    if git:
        p = Path(git).resolve()
        for anc in list(p.parents)[:4]:
            candidates += [anc / "bin" / "bash.exe", anc / "usr" / "bin" / "bash.exe"]
    for env in ("ProgramFiles", "ProgramW6432", "ProgramFiles(x86)", "LOCALAPPDATA"):
        base = os.environ.get(env)
        if base:
            candidates += [Path(base) / "Git" / "bin" / "bash.exe",
                           Path(base) / "Programs" / "Git" / "bin" / "bash.exe"]
    for c in candidates:
        if c.is_file():
            return str(c)
    return None  # nao usar o bash.exe do WindowsApps (WSL): ambiente diferente


def resolve_shell(pref: str) -> Tuple[str, Optional[str]]:
    """Retorna (tipo, executavel). tipo em bash|sh|cmd|powershell."""
    if pref == "auto":
        if os.name == "nt":
            gb = _git_bash_windows()
            return ("bash", gb) if gb else ("cmd", None)
        b = shutil.which("bash")
        return ("bash", b) if b else ("sh", "/bin/sh")
    if pref == "bash":
        exe = _git_bash_windows() if os.name == "nt" else shutil.which("bash")
        if not exe:
            raise SystemExit("bash nao encontrado (no Windows instale o Git for Windows)")
        return ("bash", exe)
    if pref == "sh":
        return ("sh", shutil.which("sh") or "/bin/sh")
    if pref == "powershell":
        return ("powershell", shutil.which("pwsh") or shutil.which("powershell") or "powershell")
    return ("cmd", None)


def build_argv(shell: Tuple[str, Optional[str]], command: str) -> Tuple[Any, bool]:
    kind, exe = shell
    if kind in ("bash", "sh"):
        return [exe, "-c", command], False
    if kind == "powershell":
        return [exe, "-NoProfile", "-NonInteractive", "-Command", command], False
    return command, True  # cmd via shell=True


def _kill_tree(proc: subprocess.Popen) -> None:
    try:
        if os.name == "nt":
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            os.killpg(proc.pid, signal.SIGKILL)
    except Exception:
        proc.kill()


def run_command(shell, command: str, cwd: Path, timeout_s: float,
                stdin_text: Optional[str]) -> Dict[str, Any]:
    argv, use_shell = build_argv(shell, command)
    kwargs: Dict[str, Any] = {}
    if os.name == "nt":
        kwargs["creationflags"] = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
    else:
        kwargs["start_new_session"] = True
    env = dict(os.environ)
    env.setdefault("CI", "true")
    env.setdefault("PYTHONIOENCODING", "utf-8")
    start = time.time()
    proc = subprocess.Popen(argv, cwd=str(cwd), shell=use_shell, env=env,
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True, encoding="utf-8", errors="replace", **kwargs)
    timed_out = False
    try:
        out, err = proc.communicate(input=stdin_text or None, timeout=timeout_s)
    except subprocess.TimeoutExpired:
        timed_out = True
        _kill_tree(proc)
        try:
            out, err = proc.communicate(timeout=10)
        except Exception:
            out, err = "", ""
    return {"code": proc.returncode, "stdout": out or "", "stderr": err or "",
            "seconds": round(time.time() - start, 2), "timed_out": timed_out}


# ---------------------------------------------------------------------------
# Execucao
# ---------------------------------------------------------------------------


def _norm(s: str) -> str:
    return "\n".join(line.rstrip() for line in s.replace("\r\n", "\n").split("\n")).strip()


def check_output(expected: str, actual: str, comparison: str) -> bool:
    if not expected:
        return True
    if comparison == "exact":
        return _norm(actual) == _norm(expected)
    if comparison == "regex":
        return re.search(expected, actual, re.MULTILINE) is not None
    return _norm(expected) in _norm(actual)


def run_test(test: Dict[str, Any], cwd: Path, shell, timeout_unit: str) -> Dict[str, Any]:
    timeout = float(test.get("timeout", 10))
    timeout_s = timeout * 60 if timeout_unit == "minutes" else timeout
    result: Dict[str, Any] = {"name": test["name"], "points": int(test.get("points", 0)),
                              "required": bool(test.get("required", False)),
                              "passed": False, "reason": "", "seconds": 0.0,
                              "stdout": "", "stderr": ""}
    setup = str(test.get("setup", "") or "").strip()
    if setup:
        r = run_command(shell, setup, cwd, timeout_s, None)
        result["seconds"] += r["seconds"]
        if r["timed_out"] or r["code"] != 0:
            result.update(reason="setup falhou" + (" (timeout)" if r["timed_out"] else f" (exit {r['code']})"),
                          stdout=r["stdout"], stderr=r["stderr"])
            return result
    r = run_command(shell, str(test["run"]), cwd, timeout_s, test.get("input") or None)
    result["seconds"] = round(result["seconds"] + r["seconds"], 2)
    result["stdout"], result["stderr"] = r["stdout"], r["stderr"]
    if r["timed_out"]:
        result["reason"] = f"timeout ({timeout:g} {timeout_unit})"
    elif r["code"] != 0:
        result["reason"] = f"exit code {r['code']}"
    elif not check_output(str(test.get("output", "") or ""), r["stdout"], test.get("comparison", "included")):
        result["reason"] = f"saida nao confere ({test.get('comparison', 'included')})"
    else:
        result["passed"] = True
    return result


def summarize(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = sum(r["points"] for r in results)
    earned = sum(r["points"] for r in results if r["passed"])
    if total == 0:  # sem pontos definidos: nota = proporcao de testes aprovados
        total, earned = len(results), sum(1 for r in results if r["passed"])
    gate_failed = [r["name"] for r in results if r.get("required") and not r["passed"]]
    if gate_failed:  # teste "required" reprovado (ex.: integridade) zera a nota
        earned = 0
    pct = round(100.0 * earned / total, 2) if total else 0.0
    return {"earned": earned, "total": total, "percent": pct,
            "passed": sum(1 for r in results if r["passed"]), "count": len(results),
            "gate_failed": gate_failed}


def run_suite(cfg: Dict[str, Any], cwd: Path, shell_pref: str = "auto", pattern: Optional[str] = None,
              timeout_unit: str = "minutes", on_result=None) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    shell = resolve_shell(shell_pref)
    tests = cfg["tests"]
    if pattern:
        rx = re.compile(pattern, re.IGNORECASE)
        tests = [t for t in tests if rx.search(t["name"])]
    results = []
    for i, t in enumerate(tests, 1):
        r = run_test(t, cwd, shell, timeout_unit)
        results.append(r)
        if on_result:
            on_result(i, len(tests), r)
    return results, summarize(results)


# ---------------------------------------------------------------------------
# Relatorios
# ---------------------------------------------------------------------------


def _tail(text: str, n: int) -> str:
    lines = text.rstrip().splitlines()
    return "\n".join(lines[-n:]) if n > 0 else "\n".join(lines)


def write_junit(results: List[Dict[str, Any]], summary: Dict[str, Any], path: Path) -> None:
    suite = ET.Element("testsuite", name="autograding", tests=str(len(results)),
                       failures=str(sum(1 for r in results if not r["passed"])),
                       time=str(round(sum(r["seconds"] for r in results), 2)))
    for r in results:
        case = ET.SubElement(suite, "testcase", classname="autograding",
                             name=f"{r['name']} ({r['points']}pt)", time=str(r["seconds"]))
        if not r["passed"]:
            fail = ET.SubElement(case, "failure", message=r["reason"])
            fail.text = _tail(r["stdout"] + "\n" + r["stderr"], 80)
    props = ET.SubElement(suite, "properties")
    for k, v in summary.items():
        ET.SubElement(props, "property", name=k, value=str(v))
    ET.ElementTree(suite).write(str(path), encoding="utf-8", xml_declaration=True)


def write_step_summary(results: List[Dict[str, Any]], summary: Dict[str, Any]) -> None:
    target = os.environ.get("GITHUB_STEP_SUMMARY")
    if not target:
        return
    lines = [f"## Autograding: {summary['earned']}/{summary['total']} pontos ({summary['percent']}%)", "",
             "| | Teste | Pontos | Motivo |", "|---|---|---|---|"]
    for r in results:
        mark = "✅" if r["passed"] else "❌"
        pts = f"{r['points'] if r['passed'] else 0}/{r['points']}"
        lines.append(f"| {mark} | {r['name']} | {pts} | {r['reason']} |")
    with open(target, "a", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: Optional[List[str]] = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Runner de autograding (formato GitHub Classroom).")
    ap.add_argument("-c", "--config", help="caminho do autograding.json (padrao: busca automatica)")
    ap.add_argument("-C", "--cwd", help="diretorio onde os comandos rodam (padrao: raiz do repo)")
    ap.add_argument("-k", "--filter", help="regex para filtrar testes pelo nome")
    ap.add_argument("--shell", default="auto", choices=["auto", "bash", "sh", "cmd", "powershell"])
    ap.add_argument("--timeout-unit", default="minutes", choices=["minutes", "seconds"])
    ap.add_argument("--list", action="store_true", help="lista os testes e sai")
    ap.add_argument("--validate", action="store_true", help="valida o arquivo e sai")
    ap.add_argument("--junit", help="grava relatorio JUnit XML")
    ap.add_argument("--json", help="grava resumo JSON")
    ap.add_argument("--tail", type=int, default=30, help="linhas de log exibidas por falha (0 = tudo)")
    ap.add_argument("-q", "--quiet", action="store_true", help="nao mostra logs de falhas")
    ap.add_argument("--fail-under", type=float, default=100.0,
                    help="exit 0 se percentual >= valor (padrao 100)")
    ap.add_argument("--no-fail", action="store_true", help="sempre exit 0 (apenas reporta)")
    args = ap.parse_args(argv)

    cfg_path = Path(args.config) if args.config else find_config(Path.cwd())
    if not cfg_path or not cfg_path.is_file():
        print("autograding.json nao encontrado (procurado: " + ", ".join(CONFIG_CANDIDATES) + ")")
        return 2
    try:
        cfg = load_config(cfg_path)
    except json.JSONDecodeError as e:
        print(f"JSON invalido em {cfg_path}: {e}")
        return 2
    errors, warnings = validate_config(cfg)
    for w in warnings:
        print(f"[aviso] {w}")
    if errors:
        for e in errors:
            print(f"[erro] {e}")
        return 2
    if args.validate:
        n = len(cfg["tests"])
        pts = sum(int(t.get("points", 0)) for t in cfg["tests"])
        print(f"OK: {cfg_path} - {n} testes, {pts} pontos")
        return 0
    if args.list:
        for i, t in enumerate(cfg["tests"], 1):
            print(f"{i:>3}. [{t.get('points', 0)}pt] {t['name']}\n       $ {t['run']}")
        return 0

    cwd = Path(args.cwd) if args.cwd else repo_root_for(cfg_path)
    shell = resolve_shell(args.shell)
    print(f"Autograding: {cfg_path}  (cwd={cwd}, shell={shell[0]})\n")

    def on_result(i: int, n: int, r: Dict[str, Any]) -> None:
        mark = "PASS" if r["passed"] else "FAIL"
        got = r["points"] if r["passed"] else 0
        print(f"[{i:>2}/{n}] {mark}  {got}/{r['points']}pt  {r['name']}  ({r['seconds']}s)"
              + ("" if r["passed"] else f"  -> {r['reason']}"))
        if not r["passed"] and not args.quiet:
            log = _tail((r["stdout"] or "") + ("\n" + r["stderr"] if r["stderr"] else ""), args.tail)
            if log.strip():
                print("        | " + log.replace("\n", "\n        | "))

    results, summary = run_suite(cfg, cwd, args.shell, args.filter, args.timeout_unit, on_result)
    print(f"\nNota: {summary['earned']}/{summary['total']} pontos ({summary['percent']}%) - "
          f"{summary['passed']}/{summary['count']} testes aprovados")
    if summary["gate_failed"]:
        print("Nota zerada: teste obrigatorio reprovado -> " + ", ".join(summary["gate_failed"]))

    if args.junit:
        write_junit(results, summary, Path(args.junit))
    if args.json:
        data = {"summary": summary, "results": [{k: v for k, v in r.items() if k not in ("stdout", "stderr")}
                                                for r in results]}
        Path(args.json).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    write_step_summary(results, summary)

    if args.no_fail:
        return 0
    return 0 if summary["percent"] >= args.fail_under else 1


if __name__ == "__main__":
    sys.exit(main())
