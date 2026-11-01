---
title: "AbleMind DSH 版"
tagline: "以 DeepSeek Harness 为宿主、不改内核的插件产品"
kind: private
order: 3
year: "2026"
summary: "宿主的 agent loop、Session、ToolRuntime、权限与人机交互直接复用；自建知识召回、笔记、研究选路等插件。"
tags:
  - "Cordis 插件"
  - "TypeScript"
links: []
metrics:
  - "自建知识召回与选路插件"
  - "统一插件开发规范"
  - "用插件而非 hook 实现自进化"
---
宿主的 agent loop、Session、ToolRuntime、权限与人机交互直接复用；自建知识召回、笔记、研究选路、任务收尾门等插件，工作台外壳在社区插件上改造。每个包按「自建 / fork / 社区原装」记血缘。

## 插件开发规范

通读上游六十多天、一万两千多次提交的开发史，加上一次真实的任务收尾事故，沉淀成一个 Skill，写插件时自动加载：先调研 → 过设计门 → 最小包 → 在缝内实现 → 验证真插件 → 记账。

## 自进化：插件，而不是 hook

原先在 Claude Code 里靠四个生命周期 hook 维持。一次盲测发现，任务换到 DSH 上跑时这些 hook 全程没执行，也没有任何信号。于是改判据：只有「单次代价高 × 判据精确」的才配站在循环里拦截；其余改为插件注入，以及读会话事件流做传感。
