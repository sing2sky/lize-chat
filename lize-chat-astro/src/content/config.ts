import { defineCollection, z } from 'astro:content';

// 统一的内容架构：既支持对话，也支持普通文章
const blogCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    // 将日期字段改为可选，或同时兼容 date 和 pubDate
    date: z.coerce.date().optional(), 
    pubDate: z.coerce.date().optional(),
    description: z.string().optional(),
    participants: z.array(z.string()).optional(),
    guest: z.string().optional(),
    host: z.string().optional(),
    tags: z.array(z.string()).optional(),
    slideUrl: z.string().optional(),
  }),
});

export const collections = {
  // 确保这里的键名 'blog' 对应您的文件夹 src/content/blog
  'blog': blogCollection,
};