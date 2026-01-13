#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章抓取脚本（增强版）
支持更多内容提取选项和自定义配置
"""

import requests
from bs4 import BeautifulSoup
import re
import os
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse, urljoin
import html2text
import json
import argparse

# 配置
CONTENT_DIR = Path(__file__).parent.parent / "src" / "content" / "blog"
CONTENT_DIR.mkdir(parents=True, exist_ok=True)

# 设置 User-Agent
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

# 初始化 html2text 转换器
h = html2text.HTML2Text()
h.ignore_links = False
h.ignore_images = True  # 忽略图片，因为微信公众号图片通常需要特殊处理
h.body_width = 0
h.unicode_snob = True
h.mark_code = True  # 保留代码块


def sanitize_filename(title):
    """将标题转换为安全的文件名"""
    filename = re.sub(r'[^\w\s-]', '', title)
    filename = re.sub(r'\s+', '-', filename)
    filename = filename[:100]
    return filename


def parse_date(date_str):
    """解析各种日期格式"""
    if not date_str:
        return None
    
    # 常见日期格式
    patterns = [
        (r'(\d{4})[年\-/](\d{1,2})[月\-/](\d{1,2})[日]?', '%Y-%m-%d'),
        (r'(\d{4})-(\d{2})-(\d{2})', '%Y-%m-%d'),
        (r'(\d{4})/(\d{2})/(\d{2})', '%Y-%m-%d'),
    ]
    
    for pattern, _ in patterns:
        match = re.search(pattern, date_str)
        if match:
            try:
                year, month, day = match.groups()
                return datetime(int(year), int(month), int(day))
            except:
                continue
    
    return None


def extract_wechat_article(url, extract_images=False):
    """
    提取微信公众号文章内容
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
            'h1.rich_media_title#activity-name',
            'h1',
            'title'
        ]
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                title = title_elem.get_text(strip=True)
                # 移除常见的后缀
                title = re.sub(r'\s*[-|]\s*.*微信公众号.*$', '', title, flags=re.IGNORECASE)
                title = re.sub(r'\s*[-|]\s*.*$', '', title)
                if title:
                    break
        
        if not title:
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.get_text(strip=True)
                title = re.sub(r'\s*[-|]\s*.*$', '', title)
        
        if not title:
            title = '未命名文章'
        
        # 提取发布日期
        pub_date = None
        date_selectors = [
            '#publish_time',
            '.publish_time',
            'em#publish_time',
            'em.rich_media_meta_text',
            'span#publish_time',
            'div.rich_media_meta_text',
        ]
        
        for selector in date_selectors:
            date_elem = soup.select_one(selector)
            if date_elem:
                date_text = date_elem.get_text(strip=True)
                pub_date = parse_date(date_text)
                if pub_date:
                    break
        
        # 如果还没找到，尝试从 meta 标签获取
        if not pub_date:
            meta_date = soup.find('meta', property='article:published_time')
            if meta_date:
                date_str = meta_date.get('content', '')
                try:
                    pub_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                except:
                    pass
        
        # 如果还是没有，使用当前日期
        if not pub_date:
            pub_date = datetime.now()
        
        # 提取正文内容
        content = None
        content_selectors = [
            '#js_content',
            '.rich_media_content',
            'div[id*="content"]',
            'div[class*="content"]',
            'article',
            'div.article-content',
        ]
        
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                content = content_elem
                break
        
        if not content:
            # 尝试查找包含大量文本的 div
            divs = soup.find_all('div', class_=re.compile(r'content|article|text|rich'))
            for div in divs:
                text_length = len(div.get_text())
                if text_length > 500:  # 假设正文至少500字符
                    content = div
                    break
        
        if not content:
            raise ValueError("无法找到文章内容")
        
        # 清理不需要的元素
        for elem in content.find_all(['script', 'style', 'iframe', 'noscript']):
            elem.decompose()
        
        # 移除微信公众号特有的元素
        for elem in content.find_all(class_=re.compile(r'qr|code|ad|advertisement|promotion')):
            elem.decompose()
        
        # 转换为 Markdown
        markdown_content = h.handle(str(content))
        
        # 清理 Markdown 内容
        # 移除多余的空行
        markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
        # 移除首尾空白
        markdown_content = markdown_content.strip()
        # 移除微信公众号二维码等提示
        markdown_content = re.sub(r'长按.*关注.*\n?', '', markdown_content, flags=re.IGNORECASE)
        markdown_content = re.sub(r'扫码.*关注.*\n?', '', markdown_content, flags=re.IGNORECASE)
        
        return {
            'title': title,
            'date': pub_date,
            'content': markdown_content,
            'url': url
        }
        
    except requests.RequestException as e:
        raise Exception(f"网络请求失败: {str(e)}")
    except Exception as e:
        raise Exception(f"提取文章失败: {str(e)}")


def generate_frontmatter(title, date, description=None, guest=None, host=None, slide_url=None, tags=None):
    """生成 Frontmatter"""
    frontmatter = {
        'title': f'"{title}"',  # 标题用引号包裹，避免特殊字符问题
        'pubDate': date.strftime('%Y-%m-%d'),
    }
    
    if description:
        frontmatter['description'] = f'"{description}"'
    
    if guest:
        frontmatter['guest'] = f'"{guest}"'
    
    if host:
        frontmatter['host'] = f'"{host}"'
    
    if slide_url:
        frontmatter['slideUrl'] = f'"{slide_url}"'
    
    if tags:
        if isinstance(tags, list):
            tags_str = '[' + ', '.join([f'"{tag}"' for tag in tags]) + ']'
            frontmatter['tags'] = tags_str
        else:
            frontmatter['tags'] = f'"{tags}"'
    
    # 格式化为 YAML
    lines = ['---']
    for key, value in frontmatter.items():
        lines.append(f'{key}: {value}')
    lines.append('---')
    
    return '\n'.join(lines)


def extract_summary(content, max_length=150):
    """从内容中提取摘要"""
    if not content:
        return None
    
    # 移除 Markdown 格式标记
    text = re.sub(r'[#*_\[\]()]', '', content)
    text = re.sub(r'\n+', ' ', text)
    text = text.strip()
    
    # 取前 max_length 个字符
    if len(text) > max_length:
        # 尝试在句号处截断
        sentences = re.split(r'[。！？]', text[:max_length * 2])
        if len(sentences) > 1:
            summary = '。'.join(sentences[:-1]) + '。'
        else:
            summary = text[:max_length] + '...'
    else:
        summary = text
    
    return summary


def save_article(article_data, output_dir=None, guest=None, host=None, tags=None):
    """保存文章到文件"""
    if output_dir is None:
        output_dir = CONTENT_DIR
    
    # 生成文件名
    filename = sanitize_filename(article_data['title'])
    filepath = output_dir / f"{filename}.md"
    
    # 如果文件已存在，添加时间戳
    counter = 1
    original_filepath = filepath
    while filepath.exists():
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = output_dir / f"{filename}_{timestamp}_{counter}.md"
        counter += 1
    
    # 生成摘要
    description = extract_summary(article_data['content'])
    
    # 生成 Frontmatter
    frontmatter = generate_frontmatter(
        title=article_data['title'],
        date=article_data['date'],
        description=description,
        guest=guest,
        host=host,
        tags=tags
    )
    
    # 组合内容
    full_content = f"{frontmatter}\n\n{article_data['content']}"
    
    # 保存文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    return filepath


def main():
    parser = argparse.ArgumentParser(description='抓取微信公众号文章并转换为 Markdown')
    parser.add_argument('urls', nargs='*', help='微信公众号文章 URL')
    parser.add_argument('--file', '-f', help='从文件读取 URL 列表')
    parser.add_argument('--guest', '-g', help='嘉宾名称')
    parser.add_argument('--host', '-h', help='主持人名称（默认为"丽泽"）', default='丽泽')
    parser.add_argument('--tags', '-t', help='标签，用逗号分隔', default='')
    parser.add_argument('--output', '-o', help='输出目录（默认为 src/content/blog）')
    
    args = parser.parse_args()
    
    # 获取 URL 列表
    urls = []
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    else:
        urls = args.urls
    
    if not urls:
        parser.print_help()
        return
    
    # 解析标签
    tags = [tag.strip() for tag in args.tags.split(',')] if args.tags else None
    
    # 设置输出目录
    output_dir = Path(args.output) if args.output else CONTENT_DIR
    
    print(f"📝 准备处理 {len(urls)} 篇文章...")
    print(f"📁 输出目录: {output_dir}")
    
    results = []
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] 正在处理: {url}")
        try:
            article_data = extract_wechat_article(url)
            filepath = save_article(
                article_data,
                output_dir=output_dir,
                guest=args.guest,
                host=args.host,
                tags=tags
            )
            results.append({
                'url': url,
                'success': True,
                'filepath': str(filepath),
                'title': article_data['title']
            })
            print(f"✅ 成功: {article_data['title']}")
            print(f"   保存到: {filepath}")
        except Exception as e:
            print(f"❌ 失败: {str(e)}")
            results.append({
                'url': url,
                'success': False,
                'error': str(e)
            })
    
    # 打印总结
    print("\n" + "="*60)
    print("处理完成！")
    print("="*60)
    success_count = sum(1 for r in results if r['success'])
    print(f"成功: {success_count}/{len(results)}")
    
    if success_count > 0:
        print("\n成功保存的文章:")
        for r in results:
            if r['success']:
                print(f"  ✓ {r['title']}")
                print(f"    {r['filepath']}")


if __name__ == '__main__':
    main()
