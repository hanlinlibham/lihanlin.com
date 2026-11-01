/** 从 task-harness 任务目录读取工作进展。只发布 allowlist 里登记过的任务。 */
import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { cfg, root, readJson, writeData } from "./lib.mjs";

const allow = JSON.parse(readFileSync(join(root, "scripts/collect/progress.allow.json"), "utf8"));
const items = [];

for (const entry of allow.published) {
  const dir = join(cfg.progress.tasksRoot, entry.slug);
  if (!existsSync(dir)) { console.warn(`  ⚠ 任务不存在，跳过: ${entry.slug}`); continue; }
  const task = readJson(join(dir, "task.json"), {});
  const handoffsDir = join(dir, "handoffs");
  let updatedAt = entry.updatedAt || task.created_at || null;
  let handoffs = 0;
  if (existsSync(handoffsDir)) {
    const { readdirSync, statSync } = await import("node:fs");
    const files = readdirSync(handoffsDir).filter((f) => f.endsWith(".md"));
    handoffs = files.length;
    if (files.length) {
      const latest = files.map((f) => ({ f, t: statSync(join(handoffsDir, f)).mtime }))
        .sort((a, b) => b.t - a.t)[0];
      updatedAt = latest.t.toISOString().slice(0, 10);
    }
  }
  items.push({
    slug: entry.slug,
    title: entry.title,
    summary: entry.summary,
    status: entry.status || "active",
    question: task.question || "",
    createdAt: task.created_at || null,
    updatedAt,
    handoffs,
  });
}

items.sort((a, b) => String(b.updatedAt).localeCompare(String(a.updatedAt)));
writeData("progress", { generatedAt: new Date().toISOString(), items });
