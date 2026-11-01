import { execFileSync } from "node:child_process";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const steps = ["github", "activity", "progress", "digest"];
for (const step of steps) {
  console.log(`[collect] ${step}`);
  try {
    execFileSync(process.execPath, [join(here, `${step}.mjs`)], { stdio: "inherit" });
  } catch (err) {
    console.warn(`  ⚠ ${step} 失败：${err.message.split("\n")[0]}`);
  }
}
