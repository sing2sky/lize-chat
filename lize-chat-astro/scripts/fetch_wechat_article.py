#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章抓取脚本
将微信公众号文章转换为符合 lize.chat 项目格式的 Markdown 文件
"""

import requests
from bs4 import BeautifulSoup
import re
import os
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
import html2text
import json

# 配置
CONTENT_DIR = Path(__file__).parent.parent / "src" / "content" / "blog"
CONTENT_DIR.mkdir(parents=True, exist_ok=True)

# 设置 User-Agent，模拟浏览器访问
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

# 初始化 html2text 转换器
h = html2text.HTML2Text()
h.ignore_links = False
h.ignore_images = False
h.body_width = 0  # 不限制宽度
h.unicode_snob = True  # 使用 Unicode 字符


def sanitize_filename(title):
    """将标题转换为安全的文件名"""
    # 移除特殊字符，保留中文、英文、数字、连字符和下划线
    filename = re.sub(r'[^\w\s-]', '', title)
    # 将空格替换为连字符
    filename = re.sub(r'\s+', '-', filename)
    # 限制长度
    filename = filename[:100]
    return filename


def extract_wechat_article(url):
    """
    提取微信公众号文章内容
    注意：微信公众号文章通常需要特殊访问方式，此脚本处理可直接访问的 URL
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取标题
        title = None
        title_selectors = [
            'h1#activity-name',
            'h1.rich_media_title',
            'h1',
            'title'
        ]
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                title = title_elem.get_text(strip=True)
                break
        
        if not title:
            title = soup.find('title')
            if title:
                title = title.get_text(strip=True)
                # 移除常见的后缀
                title = re.sub(r'\s*-\s*.*$', '', title)
        
        # 提取发布日期
        pub_date = None
        date_selectors = [
            '#publish_time',
            '.publish_time',
            'em#publish_time',
            'em.rich_media_meta_text',
        ]
        for selector in date_selectors:
            date_elem = soup.select_one(selector)
            if date_elem:
                date_text = date_elem.get_text(strip=True)
                # 尝试解析日期
                try:
                    # 微信公众号日期格式通常是 "2024-01-15" 或 "2024年1月15日"
                    date_match = re.search(r'(\d{4})[年\-/](\d{1,2})[月\-/](\d{1,2})', date_text)
                    if date_match:
                        year, month, day = date_match.groups()
                        pub_date = datetime(int(year), int(month), int(day))
                        break
                except:
                    pass
        
        # 如果没有找到日期，使用当前日期
        if not pub_date:
            pub_date = datetime.now()
        
        # 提取正文内容
        content = None
        content_selectors = [
            '#js_content',
            '.rich_media_content',
            'div[class*="content"]',
            'article',
        ]
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                content = content_elem
                break
        
        if not content:
            # 如果找不到特定容器，尝试查找包含大量文本的 div
            content = soup.find('div', class_=re.compile(r'content|article|text'))
        
        if not content:
            raise ValueError("无法找到文章内容")
        
        # 转换为 Markdown
        markdown_content = h.handle(str(content))
        
        # 清理 Markdown 内容
        # 移除多余的空行
        markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
        # 移除首尾空白
        markdown_content = markdown_content.strip()
        
        return {
            'title': title or '未命名文章',
            'date': pub_date,
            'content': markdown_content,
            'url': url
        }
        
    except Exception as e:
        raise Exception(f"抓取文章失败: {str(e)}")


def generate_frontmatter(title, date, description=None, guest=None, host=None, slide_url=None):
    """生成 Frontmatter"""
    frontmatter = {
        'title': title,
        'pubDate': date.strftime('%Y-%m-%d'),
    }
    
    if description:
        frontmatter['description'] = description
    
    if guest:
        frontmatter['guest'] = guest
    
    if host:
        frontmatter['host'] = host
    
    if slide_url:
        frontmatter['slideUrl'] = slide_url
    
    # 格式化为 YAML
    lines = ['---']
    for key, value in frontmatter.items():
        if isinstance(value, str):
            # 如果值包含特殊字符，使用引号
            if ':' in value or '"' in value or "'" in value:
                lines.append(f'{key}: "{value}"')
            else:
                lines.append(f'{key}: {value}')
        else:
            lines.append(f'{key}: {value}')
    lines.append('---')
    
    return '\n'.join(lines)


def save_article(article_data, output_dir=None):
    """保存文章到文件"""
    if output_dir is None:
        output_dir = CONTENT_DIR
    
    # 生成文件名
    filename = sanitize_filename(article_data['title'])
    filepath = output_dir / f"{filename}.md"
    
    # 如果文件已存在，添加时间戳
    if filepath.exists():
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = output_dir / f"{filename}_{timestamp}.md"
    
    # 生成摘要（取前100个字符）
    description = None
    if article_data['content']:
        # 移除 Markdown 格式标记，提取纯文本
        text_content = re.sub(r'[#*_\[\]()]', '', article_data['content'])
        text_content = re.sub(r'\n+', ' ', text_content)
        description = text_content[:100].strip()
        if len(text_content) > 100:
            description += '...'
    
    # 生成 Frontmatter
    frontmatter = generate_frontmatter(
        title=article_data['title'],
        date=article_data['date'],
        description=description
    )
    
    # 组合内容
    full_content = f"{frontmatter}\n\n{article_data['content']}"
    
    # 保存文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    print(f"✅ 文章已保存: {filepath}")
    return filepath


def process_urls(urls):
    """批量处理多个 URL"""
    results = []
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] 正在处理: {url}")
        try:
            article_data = extract_wechat_article(url)
            filepath = save_article(article_data)
            results.append({
                'url': url,
                'success': True,
                'filepath': str(filepath),
                'title': article_data['title']
            })
        except Exception as e:
            print(f"❌ 处理失败: {str(e)}")
            results.append({
                'url': url,
                'success': False,
                'error': str(e)
            })
    
    return results


def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python fetch_wechat_article.py <URL1> [URL2] [URL3] ...")
        print("\n或者从文件读取 URL 列表:")
        print("  python fetch_wechat_article.py --file urls.txt")
        print("\n示例:")
        print("  python fetch_wechat_article.py https://mp.weixin.qq.com/s/xxxxx")
        return
    
    urls = []
    
    # 检查是否从文件读取
    if sys.argv[1] == '--file' and len(sys.argv) > 2:
        filepath = sys.argv[2]
        with open(filepath, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    else:
        urls = sys.argv[1:]
    
    if not urls:
        print("❌ 没有提供有效的 URL")
        return
    
    print(f"📝 准备处理 {len(urls)} 篇文章...")
    results = process_urls(urls)
    
    # 打印总结
    print("\n" + "="*50)
    print("处理完成！")
    print("="*50)
    success_count = sum(1 for r in results if r['success'])
    print(f"成功: {success_count}/{len(results)}")
    
    if success_count > 0:
        print("\n成功保存的文章:")
        for r in results:
            if r['success']:
                print(f"  - {r['title']}")
                print(f"    文件: {r['filepath']}")


if __name__ == '__main__':
    main()
