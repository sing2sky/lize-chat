import { defineCollection, z } from 'astro:content';

const blogCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(), // 只有标题是必须的
    date: z.coerce.date().optional(), // 日期可有可无，不填也不崩溃
    pubDate: z.coerce.date().optional(), // 兼容 pubDate 字段
    description: z.string().optional(),
  }),
});

export const collections = {
  'blog': blogCollection, // 确保对应 src/content/blog 文件夹
};