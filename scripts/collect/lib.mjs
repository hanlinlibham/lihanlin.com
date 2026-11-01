import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

export const root = join(dirname(fileURLToPath(import.meta.url)), "../..");
export const cfg = JSON.parse(readFileSync(join(root, "scripts/collect/config.json"), "utf8"));

export function writeData(name, data) {
  const dir = join(root, "src/data");
  mkdirSync(dir, { recursive: true });
  const file = join(dir, `${name}.json`);
  writeFileSync(file, JSON.stringify(data, null, 2) + "\n");
  const kb = (statSync(file).size / 1024).toFixed(1);
  console.log(`  → src/data/${name}.json (${kb} KB)`);
}

export function readJson(path, fallback = null) {
  if (!existsSync(path)) return fallback;
  return JSON.parse(readFileSync(path, "utf8"));
}

export { readdirSync, statSync, join, existsSync };
