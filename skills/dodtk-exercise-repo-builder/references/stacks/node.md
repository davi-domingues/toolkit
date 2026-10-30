# Stack: JavaScript / TypeScript (Node.js)

Perfil do scaffold: `node`. Runner recomendado: **Vitest** (ou `node:test` sem dependências; Jest se o usuário pedir).

## Layout
```
package.json  package-lock.json  (tsconfig.json)
src/            # produção (starter)
test/           # testes do autor — *.test.js|ts
test/fixtures/{request,response,datasets}/
```
Sempre commite `package-lock.json` (CI usa `npm ci`). Fixe versões exatas (`npm i -D -E vitest@x.y.z`).

## Seletores
```bash
npx vitest run test/usuarios.test.js -t "POST /usuarios"   # arquivo + describe/it por regex
node --test --test-name-pattern="POST /usuarios" test/      # node:test (Node ≥ 20)
npx jest test/usuarios.test.js -t "POST /usuarios"
npx cucumber-js --tags @cadastrar-duplicado
```
Defina scripts no package.json (`"test": "vitest run"`) e use-os no README; no autograding use o comando explícito com filtro. Atenção: `vitest -t` com padrão que não casa nada **passa** com "no tests" em algumas versões — use `--passWithNoTests=false` (padrão no `run`) e confirme no starter que reprova.

## Padrões
- **HTTP:** exporte o `app` (Express/Fastify/Hono) sem `listen`, teste com `supertest` (`request(app).post('/x').send(body).expect(201)`) ou `fastify.inject`.
- **Golden:** `expect(res.body).toEqual(JSON.parse(readFileSync('test/fixtures/response/x.json','utf8')))`.
- **Banco:** SQLite em memória (`better-sqlite3`, Prisma com `file::memory:`) ou repositório em memória injetado; seed por fixture em `beforeEach`.
- **Inválidos:** `it.each(casos)('400 quando %s', ...)`.
- **Arquitetura:** `dependency-cruiser` com regras `forbidden` (`from: {path:'^src/controllers'}, to: {path:'^src/repositories'}`); rode `npx depcruise src --config .dependency-cruiser.cjs` como entrada própria.
- **UI/e2e:** Playwright (`npx playwright test -g "nome"`), seletores `data-testid` definidos no README; servir a página com `npx http-server` no `webServer` da config.
- **Tipos:** `npx tsc --noEmit` como entrada "compila".
- **Lint/restrições:** `npx eslint src` ou script que verifica `dependencies` do package.json contra lista permitida.

## Cobertura em degraus
`npx vitest run --coverage --coverage.include=src/services --coverage.thresholds.branches=50` (requer `@vitest/coverage-v8`). Cada degrau = uma entrada com threshold diferente (cada uma reroda a suíte — suítes Node são rápidas). Jest: `--coverageThreshold='{"global":{"branches":50}}'`.
Mutação: Stryker (`npx stryker run`, `thresholds.break`).

## Starter idioms
```js
// TODO: implemente
export function ehPalindromo(palavra) { throw new Error('Não implementado'); }
router.get('/:id', (req, res) => res.status(501).end()); // TODO
```
