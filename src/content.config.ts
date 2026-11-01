import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const projects = defineCollection({
  loader: glob({ pattern: "*.md", base: "./src/content/projects" }),
  schema: z.object({
    title: z.string(),
    tagline: z.string(),
    kind: z.enum(["open", "private"]),
    order: z.number().default(99),
    year: z.string().optional(),
    tags: z.array(z.string()).default([]),
    links: z.array(z.object({ label: z.string(), href: z.string() })).default([]),
    metrics: z.array(z.string()).default([]),
    summary: z.string().default(""),
    draft: z.boolean().default(false),
  }),
});

const notes = defineCollection({
  loader: glob({ pattern: "*.md", base: "./src/content/notes" }),
  schema: z.object({
    title: z.string(),
    href: z.string(),
    summary: z.string(),
    order: z.number().default(99),
  }),
});

export const collections = { projects, notes };
