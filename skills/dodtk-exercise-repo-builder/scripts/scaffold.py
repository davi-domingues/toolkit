#!/usr/bin/env python3
"""
scaffold.py - cria o esqueleto padrao de um repositorio de exercicio.

Gera a "casca" comum a todos os repos de treino analisados; o conteudo especifico
(enunciado, codigo starter, testes, fixtures) e escrito depois pelo agente.

  <dest>/
  ├── README.md                         (template do tipo escolhido, com placeholders)
  ├── RUBRICA.md                        (apenas --type project)
  ├── .gitignore / .gitattributes       (comum + stack)
  ├── .gitlab-ci.yml                    (--ci gitlab|both)
  └── .github/
      ├── workflows/classroom.yml       (--ci github|both)
      └── classroom/
          ├── autograding.json          (1 teste TODO a substituir)
          └── grade.py                  (runner local/CI)

Uso:
  python scaffold.py --dest ./exercicio-filas --title "Fila de Atendimento" \
      --stack python --type implement --ci github --git
  python scaffold.py --list-stacks
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATES = SKILL_DIR / "templates"
TYPES = ("implement", "katas", "write-tests", "fix-bug", "project")
COMMON_IGNORE = [".idea/", ".vscode/", "*.iml", ".DS_Store", "Thumbs.db",
                 "grading-report.xml", "grading-result.json"]
COMMON_ATTR = ["* text=auto", "*.sh text eol=lf", "*.png binary", "*.jpg binary", "*.jpeg binary"]


def slugify(text: str) -> str:
    import unicodedata
    t = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-") or "exercicio"


def indent(block: str, spaces: int) -> str:
    pad = " " * spaces
    return "\n".join(pad + line if line.strip() else line for line in block.splitlines())


def render(text: str, ctx: dict) -> str:
    for k, v in ctx.items():
        text = text.replace("{{" + k + "}}", v)
    return text


def write(path: Path, content: str, force: bool, created: list, skipped: list) -> None:
    if path.exists() and not force:
        skipped.append(path)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    created.append(path)


def git_init(dest: Path) -> str:
    if (dest / ".git").exists():
        return "repositorio git ja existia"
    r = subprocess.run(["git", "init", "-b", "main"], cwd=dest, capture_output=True, text=True)
    if r.returncode != 0:  # git < 2.28
        subprocess.run(["git", "init"], cwd=dest, check=True, capture_output=True)
        subprocess.run(["git", "symbolic-ref", "HEAD", "refs/heads/main"], cwd=dest, check=True)
    return "git init (branch main)"


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    except Exception:
        pass
    stacks = json.loads((TEMPLATES / "ci" / "stacks.json").read_text(encoding="utf-8"))
    stacks.pop("_doc", None)

    ap = argparse.ArgumentParser(description="Cria o esqueleto de um repositorio de exercicio.")
    ap.add_argument("--dest", help="pasta do novo repositorio")
    ap.add_argument("--title", help="titulo do exercicio")
    ap.add_argument("--slug", help="nome curto (padrao: derivado do titulo)")
    ap.add_argument("--stack", default="generic", help="perfil de stack (ver --list-stacks)")
    ap.add_argument("--type", default="implement", choices=TYPES)
    ap.add_argument("--ci", default="github", choices=["github", "gitlab", "both", "none"])
    ap.add_argument("--deadline", default="", help="prazo opcional (texto livre, ex.: 2026-11-30 23:59)")
    ap.add_argument("--git", action="store_true", help="executa git init -b main (sem commit)")
    ap.add_argument("--force", action="store_true", help="sobrescreve arquivos existentes")
    ap.add_argument("--list-stacks", action="store_true")
    args = ap.parse_args()

    if args.list_stacks:
        for k, v in stacks.items():
            print(f"{k:<12} {v['label']}")
        return 0
    if not args.dest or not args.title:
        ap.error("--dest e --title sao obrigatorios")
    if args.stack not in stacks:
        print(f"stack desconhecida '{args.stack}'. Use uma de: {', '.join(stacks)} (ou 'generic' e edite o CI)")
        return 2

    st = stacks[args.stack]
    dest = Path(args.dest).resolve()
    dest.mkdir(parents=True, exist_ok=True)
    slug = args.slug or slugify(args.title)
    ctx = {
        "TITLE": args.title,
        "SLUG": slug,
        "STACK_LABEL": st["label"],
        "DEADLINE_LINE": f"> ⏰ **Prazo:** {args.deadline}\n" if args.deadline else "",
        "BUILD_CMD": st["build"],
        "GITHUB_SETUP": indent(st["github_setup"], 6) if st["github_setup"] else "",
        "GITLAB_IMAGE": st["gitlab_image"],
        "YEAR": str(dt.date.today().year),
    }
    created: list = []
    skipped: list = []

    readme = (TEMPLATES / "readme" / f"{args.type}.md").read_text(encoding="utf-8")
    write(dest / "README.md", render(readme, ctx), args.force, created, skipped)
    if args.type == "project":
        write(dest / "RUBRICA.md", render((TEMPLATES / "RUBRICA.md").read_text(encoding="utf-8"), ctx),
              args.force, created, skipped)

    ag = (TEMPLATES / "autograding.json").read_text(encoding="utf-8")
    write(dest / ".github" / "classroom" / "autograding.json", ag, args.force, created, skipped)
    for script in ("grade.py", "integrity.py"):
        dst = dest / ".github" / "classroom" / script
        if dst.exists() and not args.force:
            skipped.append(dst)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(SKILL_DIR / "scripts" / script, dst)
            created.append(dst)

    if args.ci in ("github", "both"):
        wf_tpl = (TEMPLATES / "ci" / "github-workflow.yml").read_text(encoding="utf-8")
        if not st["github_setup"]:
            wf_tpl = wf_tpl.replace("{{GITHUB_SETUP}}\n", "")
        write(dest / ".github" / "workflows" / "classroom.yml", render(wf_tpl, ctx), args.force, created, skipped)
    if args.ci in ("gitlab", "both"):
        gl = render((TEMPLATES / "ci" / "gitlab-ci.yml").read_text(encoding="utf-8"), ctx)
        write(dest / ".gitlab-ci.yml", gl, args.force, created, skipped)

    write(dest / ".gitignore", "\n".join(st["gitignore"] + [""] + COMMON_IGNORE) + "\n",
          args.force, created, skipped)
    write(dest / ".gitattributes", "\n".join(COMMON_ATTR + st["gitattributes"]) + "\n",
          args.force, created, skipped)

    git_msg = git_init(dest) if args.git else "git nao inicializado (use --git)"

    print(f"Exercicio '{args.title}' ({args.type}, {st['label']}) em {dest}")
    for p in created:
        print(f"  + {p.relative_to(dest)}")
    for p in skipped:
        print(f"  = {p.relative_to(dest)} (ja existia; use --force)")
    print(f"  {git_msg}")
    print("\nProximos passos: escrever README (substituir <!-- ... -->), starter, testes, fixtures;\n"
          "substituir o teste TODO do autograding.json; validar com scripts/verify.py.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
