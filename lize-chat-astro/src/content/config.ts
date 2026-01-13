import { defineCollection, z } from 'astro:content';

const dialogueCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    participants: z.array(z.string()).optional(), // 参与者列表
    summary: z.string().optional(), // 摘要
    tags: z.array(z.string()).optional(), // 标签
    slideUrl: z.string().optional(), // notebook生成的slide URL
  }),
});

// 保留 blog 集合以兼容现有内容
const blogCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    pubDate: z.coerce.date(),
    guest: z.string().optional(),
    host: z.string().optional(),
    slideUrl: z.string().optional(),
  }),
});

export const collections = {
  'dialogue': dialogueCollection,
  'blog': blogCollection,
};
