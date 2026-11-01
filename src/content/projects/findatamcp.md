---
title: "findatamcp"
tagline: "一次工具调用，同时拿到给模型看的数据和给人看的图表"
kind: open
order: 3
year: "2026"
summary: "围绕两个实测失败模式设计：工具太多模型选不动，用渐进披露；结果太大挤爆上下文，超 200 行落成 jsonl。"
tags:
  - "MCP"
  - "MIT"
links:
  - label: "GitHub"
    href: "https://github.com/hanlinlibham/findatamcp"
metrics: []
---
围绕两个实测的失败模式设计：

- **工具太多，模型选不动**：一次性把几十个工具塞进 system prompt，近似工具互相干扰。解法是渐进披露——先给目录，再按需展开。
- **结果太大，挤爆上下文**：超过 200 行的结果落成 jsonl 并返回数据地址，模型只读摘要，图表在沙箱 iframe 里渲染。
