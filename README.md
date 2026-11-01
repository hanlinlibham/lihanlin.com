# lihanlin.com

个人站点：作品、工作进展与科技日报。Astro 静态站点，CI 构建，静态部署到本机 nginx。

## 结构

```
src/
  site.config.ts          站点文案、导航、联系方式（改文案不用碰页面）
  styles/                 tokens.css（设计 token）· base.css · layout.css · motion.css
  components/ui/          Button · Badge · SectionHead · Stat
  components/site/        Nav · Footer · Ticker · ProgressBar · ScrollCue
  layouts/BaseLayout.astro
  content/projects/       作品（Markdown + frontmatter）
  content/notes/          外部文章目录
  content/research/       系列研究（月份、状态、对象与提纲）
  data/                   采集生成的 JSON 快照（提交进仓库）
  pages/                  index · projects/[slug] · research/[slug] · progress · daily · 404
scripts/
  collect/                数据采集：GitHub / 提交活动 / 任务进展 / 日报
  sync.sh                 把 CI 产物同步到本机 web 根
```

## 常用命令

```bash
npm run collect   # 采集数据到 src/data/*.json（本机运行，读取私有源的只在这里）
npm run dev       # 本地预览
npm run build     # 构建（正式构建在 CI）
bash scripts/sync.sh   # 下载最新 CI 产物并部署到本机
```

## 数据来源

| 数据 | 来源 | 说明 |
| --- | --- | --- |
| `repos.json` | GitHub API | 公开仓库的 star、最近更新、语言 |
| `activity.json` | 本地 services 仓库 `git log` | 只有聚合数字，不含业务内容 |
| `progress.json` | `task-harness` 任务目录 + `progress.allow.json` | 只发布登记过的任务 |
| `digest.json` | `apps/digest-pipeline/data/digests.json` | 科技日报，AI builders 公开动态 |

**隐私边界**：采集脚本只读取，不写入；私有内容一律不落进 `src/data/`。新增公开条目必须在 `progress.allow.json` 里显式登记。

## 发布

1. 本机 `npm run collect` 更新快照并提交
2. push 到 `main` → GitHub Actions 构建并把 `dist.zip` 挂到 `build-latest` release
3. 本机 `bash scripts/sync.sh` 下载产物、备份旧站点、安装到 `/var/www/html`
