import { test } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { parseFrontmatter, validateSkills, listAssets } from "../scripts/lib.mjs";
import { run, parseArgs } from "../scripts/toolkit.mjs";

function fixture() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "tk-root-"));
  fs.mkdirSync(path.join(root, "skills", "demo"), { recursive: true });
  fs.writeFileSync(path.join(root, "skills", "demo", "SKILL.md"), "---\nname: demo\ndescription: skill de teste\n---\n# demo\n");
  fs.mkdirSync(path.join(root, "steering"));
  fs.writeFileSync(path.join(root, "steering", "global.md"), "# regras\n");
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

  fs.rmSync(foreign, { recursive: true });
  run(["install", "--tools", "kiro"], root);
  assert.ok(run(["install", "--tools", "kiro"], root).every((l) => l.includes("ja instalado")));

  run(["uninstall", "--tools", "kiro"], root);
  assert.equal(fs.existsSync(foreign), false);
  assert.equal(fs.existsSync(path.join(root, "skills", "demo", "SKILL.md")), true);
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
