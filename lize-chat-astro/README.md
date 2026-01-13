# 丽泽讲会 (lize.chat)

对话驱动的专栏网站，使用 Astro + Tailwind CSS 构建。

## 视觉风格

### 配色方案
- **主色（Cyan）**: `#00AEEF` - 用于强调、链接、按钮
- **深色（Deep Blue）**: `#0054A6` - 用于深色背景、重要元素
- **文字色**: `#1F2937` - 深灰色，确保可读性
- **背景色**: `#FFFFFF` - 纯白背景，极简风格
- **浅灰背景**: `#F9FAFB` - 用于卡片、消息气泡

### 字体
- **标题**: 使用衬线体（Noto Serif SC / Source Han Serif SC），体现专栏的深度感
- **正文**: 使用无衬线体（系统默认），保证可读性

## 功能特性

- 🎨 **极简主义设计**：纯白背景，深灰色文字，呼吸感十足
- 💬 **对话式内容**：内容页采用聊天对话框样式，左侧是嘉宾，右侧是丽泽（主持人）
- 📝 **Markdown 支持**：从 `src/content/dialogue/` 或 `src/content/blog/` 文件夹读取 Markdown 文件生成页面
- 🏷️ **标签系统**：支持为对话添加标签，便于分类和搜索
- 🎯 **演示文稿集成**：支持在内容页中间放置 notebook 生成的 slide
- 🧭 **简洁导航**：包含导航栏（Logo、讲会存档、关于）和页脚

## 项目结构

```
lize-chat-astro/
├── src/
│   ├── components/          # 组件
│   │   ├── Navbar.astro     # 导航栏（Logo + 菜单）
│   │   ├── Footer.astro     # 页脚
│   │   ├── Hero.astro       # Hero 区域（介绍 + 搜索框）
│   │   ├── ChatMessage.astro # 聊天消息组件
│   │   └── ConversationCard.astro # 对话卡片组件
│   ├── content/
│   │   ├── dialogue/        # 对话内容文件（新格式）
│   │   ├── blog/            # 博客内容文件（兼容旧格式）
│   │   └── config.ts        # 内容集合配置
│   ├── layouts/
│   │   └── Layout.astro     # 主布局
│   └── pages/
│       ├── index.astro      # 首页（Hero + 对话列表）
│       ├── about.astro      # 关于页
│       ├── subscribe.astro  # 订阅页
│       ├── dialogue/
│       │   └── [slug].astro # 对话内容页（新格式）
│       └── blog/
│           └── [slug].astro # 博客内容页（兼容旧格式）
├── public/
│   └── logo.png            # Logo 文件（需要添加）
└── tailwind.config.mjs     # Tailwind 配置
```

## 内容格式

### Dialogue 格式（推荐）

在 `src/content/dialogue/` 目录下创建 Markdown 文件：

```markdown
---
title: "对话标题"
date: 2024-01-20
participants: ["嘉宾1", "嘉宾2"]
summary: "对话摘要"
tags: ["标签1", "标签2"]
slideUrl: "https://example.com/slides"  # 可选
---

## Guest: 嘉宾名称

这是嘉宾的发言内容，支持 Markdown 格式。

## 丽泽: 

这是丽泽（主持人）的提问或回应。

## Guest: 另一个嘉宾

也可以有多个嘉宾参与对话。
```

### Blog 格式（兼容）

在 `src/content/blog/` 目录下创建 Markdown 文件（兼容旧格式）：

```markdown
---
title: "对话标题"
description: "对话描述"
pubDate: 2024-01-15
guest: "嘉宾名称"
host: "主持人名称"
slideUrl: "https://example.com/slides"  # 可选
---

## Guest: 嘉宾名称

内容...

## Host: 主持人名称

内容...
```

## Logo 设置

1. 将 Logo 图片重命名为 `logo.png`
2. 放入 `public/` 文件夹
3. Logo 会自动显示在导航栏左侧，高度控制在 40px 左右

如果 Logo 文件不存在，导航栏会显示文字"丽泽讲会"作为后备。

## 开发

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产版本
npm run preview
```

## 技术栈

- [Astro](https://astro.build/) - 静态站点生成器
- [Tailwind CSS](https://tailwindcss.com/) - 实用优先的 CSS 框架
- [Markdown-it](https://github.com/markdown-it/markdown-it) - Markdown 解析器
- [@tailwindcss/typography](https://tailwindcss.com/docs/plugins/typography) - Tailwind Typography 插件

## 页面说明

### 首页 (`/`)
- Hero 区域：显示"丽泽讲会：思想的流转与碰撞"和搜索框
- 对话列表：以卡片形式展示所有对话，包含标题、日期、摘要和标签

### 对话内容页 (`/dialogue/[slug]`)
- 对话界面：左侧显示嘉宾发言，右侧显示丽泽（主持人）发言
- 支持 Markdown 渲染
- 可选的演示文稿区域

### 关于页 (`/about`)
- 介绍丽泽讲会的理念和特色

### 订阅页 (`/subscribe`)
- 邮件订阅表单和 RSS 链接

## 注意事项

1. **Logo 文件**：确保 `public/logo.png` 存在，否则导航栏会显示文字
2. **内容格式**：推荐使用新的 `dialogue` 格式，支持更多功能（标签、参与者列表等）
3. **搜索功能**：首页的搜索框目前是前端实现，可以根据需要添加后端搜索功能
