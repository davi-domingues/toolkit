import { test } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { parseFrontmatter, validateSkills, listAssets } from "../scripts/lib.mjs";
import { run, parseArgs } from "../scripts/toolkit.mjs";

function fixture() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "tk-root-"));
  fs.mkdirSync(path.join(root, "skills", "demo"), { recursive: true });
  fs.writeFileSync(path.join(root, "skills", "demo", "SKILL.md"), "---\nname: demo\ndescription: skill de teste\n---\n# demo\n");
  fs.mkdirSync(path.join(root, "rules"));
  fs.writeFileSync(path.join(root, "rules", "global.md"), "# regras\n");
  fs.mkdirSync(path.join(root, "prompts"));
  fs.writeFileSync(path.join(root, "prompts", "p.md"), "prompt\n");
  fs.writeFileSync(path.join(root, "prompts", ".gitkeep"), "");
  process.env.TOOLKIT_HOME = fs.mkdtempSync(path.join(os.tmpdir(), "tk-home-"));
  return root;
}

test("parseFrontmatter le name e description", () => {
  assert.deepEqual(parseFrontmatter("---\nname: a\ndescription: \"b c\"\n---\nx"), { name: "a", description: "b c" });
  assert.deepEqual(parseFrontmatter("sem frontmatter"), {});
});

test("validateSkills acusa name divergente e description ausente", () => {
  const root = fixture();
  fs.writeFileSync(path.join(root, "skills", "demo", "SKILL.md"), "---\nname: outro\n---\n");
  const problems = validateSkills(root);
  assert.equal(problems.length, 2);
});

test("parseArgs rejeita opcao desconhecida", () => {
  assert.throws(() => parseArgs(["install", "--x"]), /desconhecida/);
});

test("install e uninstall sao idempotentes e nao tocam em arquivos alheios", () => {
  const root = fixture();
  const home = process.env.TOOLKIT_HOME;
  const foreign = path.join(home, ".kiro", "skills", "demo");
  fs.mkdirSync(foreign, { recursive: true });

  const first = run(["install", "--tools", "kiro"], root);
  assert.ok(first.some((l) => l.includes("kiro/skills/demo: PULADO")));
  assert.ok(fs.existsSync(path.join(home, ".kiro", "steering", "global.md")));
  assert.ok(fs.existsSync(path.join(home, ".kiro", "prompts", "p.md")));

  fs.rmSync(foreign, { recursive: true });
  run(["install", "--tools", "kiro"], root);
  assert.ok(run(["install", "--tools", "kiro"], root).every((l) => l.includes("ja instalado")));

  run(["uninstall", "--tools", "kiro"], root);
  assert.equal(fs.existsSync(foreign), false);
  assert.equal(fs.existsSync(path.join(root, "skills", "demo", "SKILL.md")), true);
});

test("list mostra rules e prompts com destinos e ignora .gitkeep", () => {
  const root = fixture();
  const lines = run(["list"], root);
  assert.ok(lines.some((l) => l.startsWith("rules (1)") && l.includes("steering") && l.includes(path.join(".claude", "rules"))));
  assert.ok(lines.some((l) => l.startsWith("prompts (1)") && l.includes("commands")));
  assert.ok(lines.includes("  - p.md"));
});

test("dry-run nao altera o disco", () => {
  const root = fixture();
  run(["install", "--dry-run"], root);
  assert.equal(fs.existsSync(path.join(process.env.TOOLKIT_HOME, ".kiro")), false);
});

test("repo real tem skills validas", () => {
  assert.equal(listAssets("skills").length > 0, true);
  assert.deepEqual(validateSkills(), []);
});

test("validate falha quando ha skill invalida", () => {
  const root = fixture();
  fs.writeFileSync(path.join(root, "skills", "demo", "SKILL.md"), "---\nname: outro\n---\n");
  assert.throws(() => run(["validate"], root), /ERRO demo/);
});

test("bin le o conteudo do diretorio do pacote, nao do cwd", () => {
  const bin = fileURLToPath(new URL("../bin/toolkit.js", import.meta.url));
  const cwd = fs.mkdtempSync(path.join(os.tmpdir(), "tk-cwd-"));
  const ok = spawnSync(process.execPath, [bin, "list"], { cwd, encoding: "utf8" });
  assert.equal(ok.status, 0, ok.stderr);
  assert.ok(ok.stdout.includes("  - java-testing-patterns"));

  const bad = spawnSync(process.execPath, [bin, "nada"], { cwd, encoding: "utf8" });
  assert.equal(bad.status, 1);
  assert.match(bad.stderr, /Uso: toolkit/);
});
