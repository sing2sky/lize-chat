# 微信公众号文章抓取脚本

这个脚本可以将微信公众号文章转换为符合 lize.chat 项目格式的 Markdown 文件。

## 安装依赖

```bash
pip install -r requirements.txt
```

或者单独安装：

```bash
pip install requests beautifulsoup4 html2text lxml
```

## 脚本版本

### 基础版本 (`fetch_wechat_article.py`)

简单易用，适合快速抓取文章。

**使用方法：**

```bash
# 单个 URL
python fetch_wechat_article.py https://mp.weixin.qq.com/s/xxxxx

# 多个 URL
python fetch_wechat_article.py https://mp.weixin.qq.com/s/xxxxx https://mp.weixin.qq.com/s/yyyyy

# 从文件读取
python fetch_wechat_article.py --file urls.txt
```

### 增强版本 (`fetch_wechat_article_enhanced.py`) ⭐ 推荐

功能更强大，支持命令行参数和自定义配置。

**使用方法：**

```bash
# 基础用法
python fetch_wechat_article_enhanced.py https://mp.weixin.qq.com/s/xxxxx

# 指定嘉宾和主持人
python fetch_wechat_article_enhanced.py https://mp.weixin.qq.com/s/xxxxx --guest "张三" --host "丽泽"

# 添加标签
python fetch_wechat_article_enhanced.py https://mp.weixin.qq.com/s/xxxxx --tags "AI,技术,对话"

# 指定输出目录
python fetch_wechat_article_enhanced.py https://mp.weixin.qq.com/s/xxxxx --output ./custom_dir

# 从文件读取并批量处理
python fetch_wechat_article_enhanced.py --file urls.txt --guest "GPT-4" --tags "AI,技术"
```

**命令行参数：**

- `--file, -f`: 从文件读取 URL 列表
- `--guest, -g`: 指定嘉宾名称
- `--host, -h`: 指定主持人名称（默认为"丽泽"）
- `--tags, -t`: 标签，用逗号分隔
- `--output, -o`: 输出目录（默认为 `src/content/blog`）

### 从文件读取 URL 列表

创建一个 `urls.txt` 文件，每行一个 URL：

```
https://mp.weixin.qq.com/s/xxxxx
https://mp.weixin.qq.com/s/yyyyy
# 这是注释，会被忽略
```

然后运行：

```bash
python fetch_wechat_article.py --file urls.txt
# 或
python fetch_wechat_article_enhanced.py --file urls.txt
```

## 输出格式

脚本会将文章保存到 `src/content/blog/` 目录下，文件格式如下：

```markdown
---
title: "文章标题"
description: "文章摘要（自动生成）"
pubDate: 2024-01-15
---

文章正文内容（Markdown 格式）
```

## 注意事项

1. **微信公众号访问限制**：
   - 微信公众号文章通常需要特殊访问方式
   - 如果直接访问失败，可能需要：
     - 使用微信内置浏览器打开链接
     - 使用专门的微信公众号抓取工具（如 wechatsogou）
     - 手动复制文章内容

2. **日期提取**：
   - 脚本会尝试从页面提取发布日期
   - 如果无法提取，会使用当前日期

3. **内容清理**：
   - 脚本会自动清理 HTML 标签并转换为 Markdown
   - 可能会丢失一些格式（如图片、特殊样式等）

4. **文件命名**：
   - 文件名基于文章标题生成
   - 如果文件已存在，会自动添加时间戳

## 高级用法

如果需要更精确的内容提取，可以修改脚本中的选择器：

```python
# 在 extract_wechat_article 函数中修改这些选择器
title_selectors = ['h1#activity-name', ...]
content_selectors = ['#js_content', ...]
```

## 故障排除

如果遇到问题：

1. **无法访问文章**：
   - 检查 URL 是否正确
   - 尝试在浏览器中打开 URL
   - 可能需要登录微信账号

2. **内容提取不完整**：
   - 检查页面结构是否变化
   - 修改选择器以匹配新的页面结构

3. **日期格式错误**：
   - 检查页面中的日期格式
   - 修改日期解析的正则表达式
