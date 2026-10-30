#!/usr/bin/env python3
"""
integrity.py - protege arquivos que o aluno nao pode alterar (testes, fixtures, CI).

  python integrity.py --write  tests/ .github/workflows/ src/test/   # autor: gera o manifesto
  python integrity.py --check                                        # pipeline: confere

O manifesto fica em .github/classroom/protected.sha256 (formato `sha256  caminho`).
Finais de linha (CRLF == LF) e BOM UTF-8 sao normalizados para nao quebrar no Windows.
No autograding.json use como teste com "required": true -> se falhar, a nota vira 0.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

MANIFEST = Path(".github/classroom/protected.sha256")
SKIP_DIRS = {".git", "node_modules", "target", "build", "dist", "bin", "obj", "__pycache__", ".venv"}


def digest(p: Path) -> str:
    data = p.read_bytes().replace(b"\r\n", b"\n")
    if data.startswith(b"\xef\xbb\xbf"):  # BOM adicionado por editores no Windows nao conta como alteracao
        data = data[3:]
    return hashlib.sha256(data).hexdigest()


def expand(root: Path, items):
    for item in items:
        p = (root / item)
        if p.is_file():
            yield p
        elif p.is_dir():
            for f in sorted(p.rglob("*")):
                if f.is_file() and not (set(f.relative_to(root).parts) & SKIP_DIRS):
                    yield f
        else:
            print(f"[aviso] nao encontrado: {item}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", nargs="+", metavar="CAMINHO", help="gera manifesto com estes arquivos/pastas")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    manifest = root / MANIFEST

    if args.write:
        files = sorted({f.relative_to(root).as_posix() for f in expand(root, args.write)})
        files = [f for f in files if f != MANIFEST.as_posix()]
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text("".join(f"{digest(root / f)}  {f}\n" for f in files), encoding="utf-8", newline="\n")
        print(f"manifesto com {len(files)} arquivos -> {MANIFEST.as_posix()}")
        return 0

    if not manifest.is_file():
        print("manifesto inexistente")
        return 1
    bad = []
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        h, rel = line.split("  ", 1)
        f = root / rel
        if not f.is_file():
            bad.append(f"removido: {rel}")
        elif digest(f) != h:
            bad.append(f"alterado: {rel}")
    if bad:
        print("Arquivos protegidos foram modificados:")
        print("\n".join("  - " + b for b in bad))
        return 1
    print("integridade OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
