import rss from "@astrojs/rss";
import type { APIContext } from "astro";
import digest from "../../data/digest.json";

export function GET(context: APIContext) {
  return rss({
    title: "科技日报 · Hanlin Li",
    description: "每天汇总 AI builders 的公开动态。",
    site: context.site!,
    items: digest.days.slice(0, 30).map((d) => ({
      title: `${d.date} 第 ${d.issue} 期`,
      pubDate: new Date(`${d.date}T08:00:00+08:00`),
      link: `/daily/${d.date}/`,
      description: d.tldr.join(" / "),
    })),
    customData: "<language>zh-cn</language>",
  });
}
