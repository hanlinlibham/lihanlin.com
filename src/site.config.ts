/** 站点级配置：文案、导航、联系方式和数据源开关集中在这里，改文案不用碰组件。 */
export const site = {
  name: "Hanlin Li",
  role: "AI 产品经理｜Agent / Harness",
  tagline: "让 Agent 理解业务背景，并在持续工作中用好知识与任务记录。",
  description:
    "Hanlin Li：AI 产品经理，关注 Agent Harness、上下文工程与知识编译。开源 AutoWiki、TaskKit、findatamcp、able-harness-kit 等。",
  email: "itseekqq@gmail.com",
  github: "https://github.com/hanlinlibham",
  githubAlt: "https://github.com/abuttoncc",
  nav: [
    { href: "/#about", label: "ABOUT" },
    { href: "/#open-source", label: "OPEN SOURCE" },
    { href: "/#architecture", label: "ARCHITECTURE" },
    { href: "/progress/", label: "PROGRESS" },
    { href: "/daily/", label: "DAILY" },
    { href: "/#contact", label: "CONTACT" },
  ],
  heroStats: [
    { value: 6, label: "开源仓库", suffix: "" },
    { value: 2, label: "私有产品线", suffix: "" },
    { value: 42, label: "行工程源码（万）", suffix: " 万" },
    { value: "2024.12", label: "主导起点", suffix: "" },
  ],
  focus: [
    ["harness", "Agent Loop · Tool Use · Subagent · HITL"],
    ["context", "知识编译 · 召回 · 跨会话接续"],
    ["memory", "候选 → 校验 → 晋升，保留来源与版本"],
    ["runtime", "DeepSeek Harness 插件 · MCP · Skills"],
    ["stack", "Python · TypeScript / React · LangChain"],
    ["domain", "金融研究与数据"],
    ["now", "无感切换 session 的个人助理"],
  ],
} as const;
