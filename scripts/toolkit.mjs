import fs from "node:fs";
import path from "node:path";
import { listAssets, resolveTargets, validateSkills, validatePrefix, ROOT } from "./lib.mjs";

const PKG = JSON.parse(fs.readFileSync(path.join(ROOT, "package.json"), "utf8"));

const USAGE = `Usage: dod-toolkit <command> [options]

Commands:
  install     Installs skills/agents/rules/prompts into the tools (default: link)
  uninstall   Removes only what this toolkit installed
  status      Shows the state of each asset in each tool
  list        Lists the toolkit assets and where each kind is installed
  validate    Validates the skills and the dodtk- asset prefix

Options:
  --tools kiro,claude,opencode   Target tools (default: all)
  --copy                         Copies instead of linking
  --dry-run                      Shows what would be done
  -h, --help                     Shows this help
  -v, --version                  Shows the version
`;

/**
 * Builds the help text, identifying the package, its author and license.
 *
 * @returns {string} help text
 */
export function help() {
  return `${PKG.name} ${PKG.version}, by ${PKG.author.name}
${PKG.description}

${USAGE}
Copyright (c) 2026 ${PKG.author.name}. ${PKG.license} License.
${PKG.homepage}`;
}

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
    else throw new Error(`Unknown option: ${argv[i]}`);
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
      // no symlink permission (e.g. Windows for files): fall back to copy
    }
  }
  fs.cpSync(asset.path, dest, { recursive: true });
  return "copy";
}

function plan(opts, root) {
  const targets = resolveTargets();
  const chosen = opts.tools ?? Object.keys(targets);
  const unknown = chosen.filter((t) => !targets[t]);
  if (unknown.length) throw new Error(`Unknown tool: ${unknown.join(", ")}`);
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
  if (argv.some((a) => a === "-h" || a === "--help") || argv[0] === "help") return [help()];
  if (argv[0] === "-v" || argv[0] === "--version") return [`${PKG.name} ${PKG.version}`];
  const opts = parseArgs(argv);
  const out = [];
  if (opts.command === "validate") {
    const problems = [...validateSkills(root), ...validatePrefix(root)];
    if (problems.length) throw new Error(problems.map((p) => `ERROR ${p}`).join("\n"));
    return ["OK: all skills are valid"];
  }
  if (opts.command === "list") {
    const targets = resolveTargets();
    for (const kind of ["skills", "agents", "rules", "prompts"]) {
      const names = listAssets(kind, root).map((a) => a.name);
      const where = Object.entries(targets).filter(([, t]) => t[kind]).map(([tool, t]) => `${tool}:${t[kind]}`);
      out.push(`${kind} (${names.length}) -> ${where.join(" | ") || "no target"}`);
      names.forEach((n) => out.push(`  - ${n}`));
    }
    return out;
  }
  if (!["install", "uninstall", "status"].includes(opts.command)) throw new Error(help());

  for (const { tool, kind, asset, dest } of plan(opts, root)) {
    const label = `${tool}/${kind}/${asset.name}`;
    const owned = isOwned(dest, asset);
    if (opts.command === "status") {
      out.push(`${label}: ${owned ? "linked" : exists(dest) ? "present (not managed)" : "missing"}`);
    } else if (opts.command === "install") {
      if (owned) out.push(`${label}: already installed`);
      else if (exists(dest)) out.push(`${label}: SKIPPED, destination exists and does not belong to this toolkit`);
      else out.push(`${label}: ${opts.dryRun ? "would install" : place(asset, dest, opts.copy)}`);
    } else if (owned) {
      if (!opts.dryRun) fs.rmSync(dest, { recursive: true });
      out.push(`${label}: ${opts.dryRun ? "would remove" : "removed"}`);
    }
  }
  return out;
}
