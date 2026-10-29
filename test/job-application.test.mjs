import { test } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const SKILL = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "skills", "dodtk-job-application");

function files(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((e) => {
    const p = path.join(dir, e.name);
    return e.isDirectory() ? files(p) : [p];
  });
}

test("links relativos do SKILL.md da job-application apontam para arquivos que existem", () => {
  const text = fs.readFileSync(path.join(SKILL, "SKILL.md"), "utf8");
  const links = [...text.matchAll(/\]\(((?:references|templates)\/[^)]+)\)/g)].map((m) => m[1]);
  assert.ok(links.length >= 6);
  for (const link of links) assert.ok(fs.existsSync(path.join(SKILL, link)), `link quebrado: ${link}`);
});

test("templates da job-application so trazem placeholders, sem dado real", () => {
  const templates = files(path.join(SKILL, "templates"));
  assert.equal(templates.length, 3);
  for (const file of templates) {
    const text = fs.readFileSync(file, "utf8");
    assert.doesNotMatch(text, /R\$\s*\d/, `${file}: valor em reais`);
    assert.doesNotMatch(text, /[\w.+-]+@[\w-]+\.[\w.]+/, `${file}: e-mail`);
    assert.doesNotMatch(text, /https?:\/\/(?!github\.com\/davi-domingues\/toolkit)/, `${file}: url`);
    assert.match(text, /<[^>\n]+>/, `${file}: sem placeholders`);
  }
});

test("a skill job-application nao contem valor salarial em reais nem e-mail", () => {
  for (const file of files(SKILL)) {
    const text = fs.readFileSync(file, "utf8");
    assert.doesNotMatch(text, /R\$\s*\d/, `${file}: valor em reais`);
    assert.doesNotMatch(text, /[\w.+-]+@[\w-]+\.[\w.]+/, `${file}: e-mail`);
  }
});
