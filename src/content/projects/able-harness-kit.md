---
title: "able-harness-kit"
tagline: "从生产中提炼的 Agent 循环中间件"
kind: open
order: 4
year: "2026"
summary: "大多数失败不是模型不够聪明，而是循环缺少观察与控制。"
tags:
  - "LangChain"
  - "MIT"
links:
  - label: "GitHub"
    href: "https://github.com/hanlinlibham/able-harness-kit"
metrics: []
---
中间件各自对应一个真实失败模式：

- 识别「没有新信息的重复调用」，但不误伤轮询和翻页；
- 防止二进制读取被网关吞掉后模型谎称读过；
- 给超大工具结果设预算，避免过早压缩。

每个都只依赖 LangChain / LangGraph 的公开类型，与现有 harness 组合而不是替换它。
