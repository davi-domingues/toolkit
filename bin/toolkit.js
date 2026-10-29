#!/usr/bin/env node
import { run } from "../scripts/toolkit.mjs";

try {
  console.log(run(process.argv.slice(2)).join("\n"));
} catch (e) {
  console.error(e.message);
  process.exit(1);
}
