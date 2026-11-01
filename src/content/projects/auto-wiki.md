---
title: "AutoWiki"
tagline: "把材料编译成持久化知识库的 Agent Skill"
kind: open
order: 1
year: "2026"
summary: "读到新材料就和已有页面比对：该更新的更新、该新建的新建、说法矛盾的标成 contested，并保留来源与时间。"
tags:
  - "Python"
  - "MIT"
  - "Skill"
links:
  - label: "GitHub"
    href: "https://github.com/hanlinlibham/auto-wiki"
metrics: []
---
## 问题

Agent 做完研究就忘了。RAG 能检索，但不能积累：每次都从原始文档重新推导，旧结论失效也没人知道。

## 做法

知识以 Markdown 页面加 SQLite 数据点存放，可在 Obsidian 里浏览，并生成图谱报告。建库不先教本体术语：`init` 访谈真实工作流，反推领域、节点类型和关系；已有笔记的用 `survey` 只读扫目录，先出提案再动手。完成标准是回归问题能引用具体页面回答，而不是「目录建好了」。

## 八个模式

`survey` 勘察已有笔记 · `init` 从工作流建库 · `source` 按清单取材 · `recall` 加载领域上下文 · `ingest` 比较新旧并编译 · `query` 带引用回答 · `lint` 断链与矛盾检查 · `deep-dive` 补齐知识缺口。

## 在私有项目里

作为知识编译内核接入研究平台：模型只提候选，内核负责比较、校验与正式提交，宿主管权限与发布。一个完整批次编译了一百多份研究材料，形成上千个可追溯页面。
