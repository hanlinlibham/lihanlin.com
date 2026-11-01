---
title: "TaskKit"
tagline: "给 Agent 一套工作秩序：任务按需建档，过程与成果各有归处"
kind: open
order: 2
year: "2026"
summary: "先认工作区、读已有规则；简单问题直接做，同一目标续做原任务，需要留存的新目标才建目录。"
tags:
  - "Python"
  - "v0.5.0"
  - "Skill"
links:
  - label: "GitHub"
    href: "https://github.com/abuttoncc/agent-taskkit"
metrics: []
---
## 问题

新会话不知道目标、进度、产物和停止条件；工具一升级，个人积累的规则可能被覆盖。

## 做法

新任务起步只有三个文件，阶段结束写交接快照，已交付文件不原位改写。公共 Skill 与个人资料分开，升级不覆盖。默认没有后台服务，也没有 hook。

```
工作区/
├── AGENTS.md          规则（已有的保留）
├── WORKSPACE.md       导航与收纳约定
└── projects/<任务>/
    ├── README.md      任务入口
    ├── request.md     目标·范围·完成条件
    └── task.json      类型与版本
```

## 来历：一次产品减法

它从更重的 Workspace Cycle 里减出来。那套系统有召回、交付门、复盘、经验晋升，确实让下一次任务复用了上一次的方法；但门禁、归档和分发漂移本身也成了负担。TaskKit 只保留真正减少重复探索的部分。

v0.3 补齐金融研究资源与可溯源计算；v0.4 把工作区秩序作为统一入口；v0.5 将金融研究拆成独立 Skill。
