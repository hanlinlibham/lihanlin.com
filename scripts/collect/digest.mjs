/** 读取 digest-pipeline 的每日产出，裁剪成站点用的日报数据。 */
import { join } from "node:path";
import { cfg, readJson, writeData } from "./lib.mjs";

const src = readJson(join(cfg.servicesRoot, cfg.digest.source), []);
if (!Array.isArray(src) || !src.length) { console.warn("  ⚠ 没有日报数据"); process.exit(0); }

const days = src
  .filter((d) => d && d.date)
  .slice(-cfg.digest.days)
  .map((d) => ({
    date: d.date,
    issue: d.issue ?? null,
    tldr: (d.tldr || []).slice(0, 4),
    topics: (d.topics || []).map((t) => ({
      id: t.id,
      title: t.title,
      consensus: t.consensus || "",
      voices: (t.voices || []).slice(0, 5).map((v) => ({
        name: v.name || "", handle: v.handle || "", kind: v.kind || "",
        take: v.take || "", url: v.url || "", metric: v.metric || "",
      })),
    })).filter((t) => t.title),
    stats: d.stats ? {
      voices: d.stats.voices ?? d.stats.total ?? null,
      topics: (d.topics || []).length,
    } : { topics: (d.topics || []).length },
  }));

writeData("digest", {
  generatedAt: new Date().toISOString(),
  source: cfg.digest.source,
  latest: days.length ? days[days.length - 1].date : null,
  days: days.reverse(),
});
