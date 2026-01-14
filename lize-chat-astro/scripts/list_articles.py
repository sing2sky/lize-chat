#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
列出所有文章文件
"""

from pathlib import Path
import frontmatter

BLOG_DIR = Path(__file__).parent.parent / "src" / "content" / "blog"
DIALOGUE_DIR = Path(__file__).parent.parent / "src" / "content" / "dialogue"


def list_articles():
    """列出所有文章"""
    print("=" * 60)
    print("当前文章列表")
    print("=" * 60)
    
    # Blog 文章
    blog_files = list(BLOG_DIR.glob("*.md"))
    if blog_files:
        print(f"\n📝 Blog 文章 ({len(blog_files)} 篇):")
        for i, file in enumerate(blog_files, 1):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)
                    title = post.get('title', '未命名')
                    date = post.get('pubDate', '未知日期')
                    print(f"  {i}. {file.name}")
                    print(f"     标题: {title}")
                    print(f"     日期: {date}")
            except Exception as e:
                print(f"  {i}. {file.name} (读取错误: {e})")
    else:
        print("\n📝 Blog 文章: 无")
    
    # Dialogue 文章
    dialogue_files = list(DIALOGUE_DIR.glob("*.md"))
    if dialogue_files:
        print(f"\n💬 Dialogue 文章 ({len(dialogue_files)} 篇):")
        for i, file in enumerate(dialogue_files, 1):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)
                    title = post.get('title', '未命名')
                    date = post.get('date', '未知日期')
                    print(f"  {i}. {file.name}")
                    print(f"     标题: {title}")
                    print(f"     日期: {date}")
            except Exception as e:
                print(f"  {i}. {file.name} (读取错误: {e})")
    else:
        print("\n💬 Dialogue 文章: 无")
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    list_articles()
