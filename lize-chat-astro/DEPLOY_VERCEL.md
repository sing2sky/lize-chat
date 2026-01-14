# Vercel 部署指南

## 问题诊断

网站 https://www.lize.chat 仍然显示"（对话列表组件即将上线...）"占位符，说明部署的是旧版本。

## 解决方案

### 方法 1: 通过 Git 自动部署（推荐）

1. **提交代码到 Git 仓库**：
   ```bash
   git add .
   git commit -m "更新首页：添加文章列表显示"
   git push
   ```

2. **Vercel 会自动检测并部署**：
   - 如果已连接 Git 仓库，Vercel 会自动触发部署
   - 在 Vercel Dashboard 中查看部署状态

### 方法 2: 手动触发重新部署

1. **登录 Vercel Dashboard**：
   - 访问 https://vercel.com/dashboard
   - 找到 `lize-chat` 项目

2. **触发重新部署**：
   - 点击项目进入详情页
   - 点击 "Deployments" 标签
   - 找到最新的部署记录
   - 点击右侧的 "..." 菜单
   - 选择 "Redeploy"

3. **清除缓存（如果需要）**：
   - 在项目设置中找到 "Build & Development Settings"
   - 点击 "Clear Build Cache"
   - 然后重新部署

### 方法 3: 使用 Vercel CLI

```bash
# 安装 Vercel CLI（如果还没有）
npm i -g vercel

# 登录
vercel login

# 部署
cd lize-chat-astro
vercel --prod
```

## 验证部署

部署完成后，访问 https://www.lize.chat/#dialogues，应该能看到：

✅ "最新讲会" 标题  
✅ 5 篇文章卡片（网格布局）  
❌ 不再显示占位符文本

## 当前应该显示的文章

1. **别在头骨上打洞了，去芯片里"投胎"吧** (2026年1月14日)
2. **龙湖七章：一场关于碳基与硅基的灵魂共振** (2025年12月20日)
3. **AI 与人类协作的未来** (2024年1月20日)
4. **探索 Web3 与去中心化未来** (2024年1月20日)
5. **AI 与人类的未来对话** (2024年1月15日)

## 检查清单

- [ ] 代码已提交到 Git 仓库
- [ ] Vercel 项目已连接 Git 仓库
- [ ] 触发重新部署
- [ ] 部署状态显示 "Ready"
- [ ] 清除浏览器缓存后访问网站
- [ ] 文章列表正常显示

## 如果问题仍然存在

1. **检查构建日志**：
   - 在 Vercel Dashboard 中查看部署日志
   - 确认构建过程中没有错误

2. **检查环境变量**：
   - 确认没有影响构建的环境变量

3. **检查文件路径**：
   - 确认 `src/content/blog/` 目录下的文件都存在
   - 确认 frontmatter 格式正确

4. **本地测试**：
   ```bash
   npm run build
   npm run preview
   ```
   在本地预览构建结果，确认文章列表正常显示
