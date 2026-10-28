import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

/**
 * Parses the leading YAML frontmatter of a markdown document.
 * Supports flat `key: value` pairs, which is all a SKILL.md requires.
 *
 * @param {string} text markdown content
 * @returns {Record<string, string>} parsed key/value pairs, empty when absent
 */
export function parseFrontmatter(text) {
  const match = text.replace(/^\uFEFF/, "").match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) return {};
  const data = {};
  for (const line of match[1].split(/\r?\n/)) {
    const pair = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (pair) data[pair[1]] = pair[2].trim().replace(/^["']|["']$/g, "");
  }
  return data;
}

/**
 * Lists the assets of one kind found in the toolkit.
 *
 * @param {"skills"|"agents"|"rules"} kind asset kind
 * @param {string} [root] toolkit root
 * @returns {{name: string, path: string, isDir: boolean}[]} discovered assets
 */
export function listAssets(kind, root = ROOT) {
  const base = path.join(root, kind);
  if (!fs.existsSync(base)) return [];
  return fs
    .readdirSync(base, { withFileTypes: true })
    .filter((e) => !e.name.startsWith(".") && e.name !== "README.md")
    .filter((e) => (kind === "skills" ? e.isDirectory() : e.isFile() && e.name.endsWith(".md")))
    .map((e) => ({ name: e.name, path: path.join(base, e.name), isDir: e.isDirectory() }));
}

/**
 * Resolves where each tool expects every asset kind.
 *
 * @param {string} [home] user home directory
 * @returns {Record<string, Partial<Record<"skills"|"agents"|"rules", string>>>} tool targets
 */
export function resolveTargets(home = process.env.TOOLKIT_HOME || os.homedir()) {
  return {
    kiro: {
      skills: path.join(home, ".kiro", "skills"),
      rules: path.join(home, ".kiro", "steering"),
    },
    claude: {
      skills: path.join(home, ".claude", "skills"),
      agents: path.join(home, ".claude", "agents"),
      rules: path.join(home, ".claude", "rules"),
    },
    opencode: {
      skills: path.join(home, ".config", "opencode", "skills"),
    },
  };
}

/**
 * Validates every skill in the toolkit.
 *
 * @param {string} [root] toolkit root
 * @returns {string[]} human readable problems, empty when valid
 */
export function validateSkills(root = ROOT) {
  const problems = [];
  for (const skill of listAssets("skills", root)) {
    const file = path.join(skill.path, "SKILL.md");
    if (!fs.existsSync(file)) {
      problems.push(`${skill.name}: SKILL.md ausente`);
      continue;
    }
    const meta = parseFrontmatter(fs.readFileSync(file, "utf8"));
    if (meta.name !== skill.name) problems.push(`${skill.name}: 'name' (${meta.name ?? "vazio"}) difere da pasta`);
    if (!meta.description) problems.push(`${skill.name}: 'description' ausente`);
  }
  return problems;
}
