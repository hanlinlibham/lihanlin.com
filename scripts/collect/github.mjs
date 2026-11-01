/** 从 GitHub 读取公开仓库的 star、最近更新与版本，生成作品区的数据快照。 */
import { cfg, writeData } from "./lib.mjs";

const token = process.env.GITHUB_TOKEN;
const headers = { accept: "application/vnd.github+json", "user-agent": "lihanlin-site-collector" };
if (token) headers.authorization = `Bearer ${token}`;

async function api(path) {
  const res = await fetch(`https://api.github.com${path}`, { headers });
  if (!res.ok) throw new Error(`${path} → ${res.status}`);
  return res.json();
}

const repos = [];
for (const user of cfg.github.users) {
  const list = await api(`/users/${user}/repos?per_page=100&sort=pushed`);
  for (const r of list) {
    if (r.fork || r.archived) continue;
    repos.push({
      full: r.full_name, name: r.name, description: r.description || "",
      url: r.html_url, stars: r.stargazers_count, language: r.language || "",
      pushedAt: r.pushed_at, topics: r.topics || [],
    });
  }
}

repos.sort((a, b) => new Date(b.pushedAt) - new Date(a.pushedAt));
writeData("repos", {
  generatedAt: new Date().toISOString(),
  count: repos.length,
  repos: repos.slice(0, cfg.github.maxRepos),
});
