/** 读本地 monorepo 的提交活动，只输出聚合数字，不含任何业务内容。 */
import { execFileSync } from "node:child_process";
import { cfg, writeData } from "./lib.mjs";

const repo = `${cfg.servicesRoot}`;
const since = `--since=${cfg.activity.days} days ago`;
const git = (args) => execFileSync("git", ["-C", repo, ...args], { encoding: "utf8" }).trim();

const branch = "origin/monorepo";
const count = (extra) => {
  const out = git(["log", branch, since, "--format=%x00", ...extra]);
  return out.split("\x00").filter(Boolean).length;
};
const authors = git(["log", branch, since, "--format=%an"])
  .split("\n").filter(Boolean)
  .reduce((m, a) => ((m[a] = (m[a] || 0) + 1), m), {});
const days = new Set(git(["log", branch, since, "--format=%ad", "--date=short"]).split("\n").filter(Boolean));

writeData("activity", {
  generatedAt: new Date().toISOString(),
  windowDays: cfg.activity.days,
  branch,
  commits: count([]),
  nonMerge: count(["--no-merges"]),
  merges: count(["--merges"]),
  activeDays: days.size,
  authors: Object.entries(authors).sort((a, b) => b[1] - a[1]).slice(0, 6).map(([name, n]) => ({ name, n })),
});
