#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { listAssets, resolveTargets, validateSkills, ROOT } from "./lib.mjs";

const USAGE = `Uso: node scripts/toolkit.mjs <comando> [opcoes]

Comandos:
  install     Instala skills/agents/rules/prompts nas ferramentas (padrao: link)
  uninstall   Remove somente o que este toolkit instalou
  status      Mostra o estado de cada asset em cada ferramenta
  list        Lista os assets do toolkit e onde cada tipo e instalado
  validate    Valida as skills do repo

Opcoes:
  --tools kiro,claude,opencode   Ferramentas alvo (padrao: todas)
  --copy                         Copia em vez de linkar
  --dry-run                      Mostra o que seria feito
`;

/**
 * @param {string[]} argv raw arguments
 * @returns {{command: string, tools: string[]|null, copy: boolean, dryRun: boolean}} parsed options
 */
export function parseArgs(argv) {
  const opts = { command: argv[0] ?? "", tools: null, copy: false, dryRun: false };
  for (let i = 1; i < argv.length; i++) {
    if (argv[i] === "--copy") opts.copy = true;
    else if (argv[i] === "--dry-run") opts.dryRun = true;
    else if (argv[i] === "--tools") opts.tools = (argv[++i] ?? "").split(",").filter(Boolean);
    else throw new Error(`Opcao desconhecida: ${argv[i]}`);
  }
  return opts;
}

function isLinkTo(dest, source) {
  try {
    return fs.lstatSync(dest).isSymbolicLink() && path.resolve(path.dirname(dest), fs.readlinkSync(dest)) === path.resolve(source);
  } catch {
    return false;
  }
}

function isOwned(dest, asset) {
  if (isLinkTo(dest, asset.path)) return true;
  if (asset.isDir || !exists(dest) || fs.lstatSync(dest).isSymbolicLink()) return false;
  return fs.readFileSync(dest).equals(fs.readFileSync(asset.path));
}

function exists(p) {
  try {
    fs.lstatSync(p);
    return true;
  } catch {
    return false;
  }
}

function place(asset, dest, copy) {
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  if (!copy) {
    try {
      fs.symlinkSync(asset.path, dest, asset.isDir ? "junction" : "file");
      return "link";
    } catch {
      // sem permissao de symlink (ex.: Windows para arquivos): cai para copia
    }
  }
  fs.cpSync(asset.path, dest, { recursive: true });
  return "copia";
}

function plan(opts, root) {
  const targets = resolveTargets();
  const chosen = opts.tools ?? Object.keys(targets);
  const unknown = chosen.filter((t) => !targets[t]);
  if (unknown.length) throw new Error(`Ferramenta desconhecida: ${unknown.join(", ")}`);
  const items = [];
  for (const tool of chosen) {
    for (const [kind, dir] of Object.entries(targets[tool])) {
      for (const asset of listAssets(kind, root)) {
        items.push({ tool, kind, asset, dest: path.join(dir, asset.name) });
      }
    }
  }
  return items;
}

/**
 * Runs a toolkit command.
 *
 * @param {string[]} argv command line arguments
 * @param {string} [root] toolkit root
 * @returns {string[]} output lines
 */
export function run(argv, root = ROOT) {
  const opts = parseArgs(argv);
  const out = [];
  if (opts.command === "validate") {
    const problems = validateSkills(root);
    return problems.length ? problems.map((p) => `ERRO ${p}`) : ["OK: todas as skills validas"];
  }
  if (opts.command === "list") {
    const targets = resolveTargets();
    for (const kind of ["skills", "agents", "rules", "prompts"]) {
      const names = listAssets(kind, root).map((a) => a.name);
      const where = Object.entries(targets).filter(([, t]) => t[kind]).map(([tool, t]) => `${tool}:${t[kind]}`);
      out.push(`${kind} (${names.length}) -> ${where.join(" | ") || "sem destino"}`);
      names.forEach((n) => out.push(`  - ${n}`));
    }
    return out;
  }
  if (!["install", "uninstall", "status"].includes(opts.command)) throw new Error(USAGE);

  for (const { tool, kind, asset, dest } of plan(opts, root)) {
    const label = `${tool}/${kind}/${asset.name}`;
    const owned = isOwned(dest, asset);
    if (opts.command === "status") {
      out.push(`${label}: ${owned ? "linkado" : exists(dest) ? "presente (nao gerenciado)" : "ausente"}`);
    } else if (opts.command === "install") {
      if (owned) out.push(`${label}: ja instalado`);
      else if (exists(dest)) out.push(`${label}: PULADO, destino existe e nao e deste toolkit`);
      else out.push(`${label}: ${opts.dryRun ? "instalaria" : place(asset, dest, opts.copy)}`);
    } else if (owned) {
      if (!opts.dryRun) fs.rmSync(dest, { recursive: true });
      out.push(`${label}: ${opts.dryRun ? "removeria" : "removido"}`);
    }
  }
  return out;
}

if (process.argv[1] && path.resolve(process.argv[1]) === path.resolve(import.meta.filename)) {
  try {
    console.log(run(process.argv.slice(2)).join("\n"));
  } catch (e) {
    console.error(e.message);
    process.exit(1);
  }
}
