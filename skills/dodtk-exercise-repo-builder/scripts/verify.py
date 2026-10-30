#!/usr/bin/env python3
"""
verify.py - portao de qualidade de um repositorio de exercicio.

Garante as duas propriedades que tornam um repo de treino confiavel:
  1. STARTER: o codigo inicial NAO ganha pontos (ou no maximo --starter-max %).
     Testes que passam no starter sao "pontos gratis" e sao listados.
  2. GABARITO: aplicando a solucao de referencia (--solution), a nota e 100%.

Cada rodada acontece numa copia temporaria do repo (o repo original nao e tocado).
A pasta da solucao espelha os caminhos do repo e e sobreposta a copia.

Uso:
  python verify.py --repo ./meu-exercicio --solution ../gabarito-tmp
  python verify.py --repo . --starter-max 10        # permite aquecimento valer ate 10%
  python verify.py --repo . --only-starter
"""
from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import grade  # noqa: E402

IGNORE = shutil.ignore_patterns(
    ".git", "node_modules", "target", "build", "dist", "out", ".gradle", ".venv", "venv",
    "__pycache__", ".pytest_cache", ".mypy_cache", "bin", "obj", ".idea", ".vscode", "coverage",
)


def copy_repo(src: Path, overlay: Path | None) -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="exercise-verify-"))
    dst = tmp / src.name
    shutil.copytree(src, dst, ignore=IGNORE)
    if overlay:
        shutil.copytree(overlay, dst, dirs_exist_ok=True, ignore=IGNORE)
    return dst


def run_round(label: str, repo: Path, cfg_rel: Path, shell: str, quiet: bool):
    cfg = grade.load_config(repo / cfg_rel)

    def on_result(i, n, r):
        if not quiet:
            mark = "PASS" if r["passed"] else "FAIL"
            print(f"  [{label}] [{i:>2}/{n}] {mark} {r['name']}" + ("" if r["passed"] else f" -> {r['reason']}"))

    results, summary = grade.run_suite(cfg, repo, shell, on_result=on_result)
    return results, summary


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Valida starter (nota ~0) e gabarito (nota 100).")
    ap.add_argument("--repo", required=True)
    ap.add_argument("--solution", help="pasta com os arquivos da solucao (mesmos caminhos do repo)")
    ap.add_argument("--starter-max", type=float, default=0.0, help="percentual maximo aceito no starter")
    ap.add_argument("--only-starter", action="store_true")
    ap.add_argument("--shell", default="auto", choices=["auto", "bash", "sh", "cmd", "powershell"])
    ap.add_argument("--keep-temp", action="store_true", help="nao apaga as copias temporarias")
    ap.add_argument("-q", "--quiet", action="store_true")
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    cfg_path = grade.find_config(repo)
    if not cfg_path:
        print("autograding.json nao encontrado no repo")
        return 2
    cfg_rel = cfg_path.resolve().relative_to(repo)
    errors, warnings = grade.validate_config(grade.load_config(cfg_path))
    for w in warnings:
        print(f"[aviso] {w}")
    if errors:
        for e in errors:
            print(f"[erro] {e}")
        return 2

    ok = True
    temps = []

    print("== Rodada 1: STARTER (esperado: sem pontos)")
    starter_repo = copy_repo(repo, None)
    temps.append(starter_repo.parent)
    s_results, s_sum = run_round("starter", starter_repo, cfg_rel, args.shell, args.quiet)
    free = [r for r in s_results if r["passed"]]
    print(f"  -> starter: {s_sum['earned']}/{s_sum['total']} ({s_sum['percent']}%)")
    if s_sum["percent"] > args.starter_max:
        ok = False
        print(f"  [FALHA] starter passou do limite de {args.starter_max}%. Testes com pontos gratis:")
        for r in free:
            print(f"     - {r['name']}")

    if args.solution and not args.only_starter:
        sol = Path(args.solution).resolve()
        if not sol.is_dir():
            print(f"pasta de solucao inexistente: {sol}")
            return 2
        print("\n== Rodada 2: GABARITO (esperado: 100%)")
        sol_repo = copy_repo(repo, sol)
        temps.append(sol_repo.parent)
        g_results, g_sum = run_round("gabarito", sol_repo, cfg_rel, args.shell, args.quiet)
        print(f"  -> gabarito: {g_sum['earned']}/{g_sum['total']} ({g_sum['percent']}%)")
        if g_sum["percent"] < 100:
            ok = False
            print("  [FALHA] gabarito nao atingiu 100%. Testes reprovados:")
            for r in g_results:
                if not r["passed"]:
                    print(f"     - {r['name']} -> {r['reason']}")
                    print("       | " + grade._tail(r["stdout"] + "\n" + r["stderr"], 15).replace("\n", "\n       | "))
    elif not args.only_starter:
        print("\n[aviso] sem --solution: nao foi provado que os testes sao passaveis")

    if args.keep_temp:
        print("\nCopias temporarias mantidas: " + ", ".join(str(t) for t in temps))
    else:
        for t in temps:
            shutil.rmtree(t, ignore_errors=True)

    print("\nRESULTADO: " + ("OK" if ok else "REPROVADO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
