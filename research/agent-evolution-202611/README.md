# 智能体的演进 · 2026 年 11 月

资料截至 2026-11-01，编成于 2026-11-02。正文、研究证据和生成文件均在本目录或下列固定位置维护。报告不依赖在线字体、脚本或外部图片，机制图为内联 SVG；手机提供等价文字。

## 文件

- `manuscript.md`：01—30，阅读框架、外部案例和比较。
- `part-2.md`：31—48，比较与 AbleWork 当前应用。
- `part-3.md`：49—60，情境、未来判断、建设方法与来源说明。
- `sources.json`：公开文献和脱敏作者核查的来源台账。
- `report.css`：网页版与 A4 打印版；每节为独立编辑单元。
- `manifest.json`：实际检查结果与交付文件指纹。
- `content-stats.json`：生成器的章节完整性记录。

正式输出：`public/research/agent-evolution/report/index.html`、`public/research/agent-evolution/agent-evolution-202611.pdf` 和 `public/research/agent-evolution/cover.svg`。研究入口由 Astro 内容集合管理。

## 再生成

本次工具版本：Python Markdown 3.10.3、Playwright 1.61.0、PyMuPDF 1.28.2；Chromium 与 Noto CJK 字体由系统提供。无需增加站点运行时依赖。

```sh
python3 scripts/research/build_agent_report.py
python3 scripts/research/export_agent_report.py --chromium /usr/bin/chromium
npm run build
```

导出检查正文与目录是否溢出、PDF 实际页数及每节所在页。页面更改后，仍需检查桌面和手机的首屏、密集章节、来源页，以及实际 PDF 图文效果。当前 PDF 为 63 页：封面 1 页、目录 2 页、正文与来源 60 页；20 幅机制图不计封面示意。

CI 复制已经检查的静态产物，不在构建期间访问外部研究来源或调用模型。更新正文后先生成和检查，再提交源稿与产物；来源、统计截止与未来建议的性质一并复核。私有底稿和运行证据不进入本仓。
