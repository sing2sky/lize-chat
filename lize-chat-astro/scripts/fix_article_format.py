#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复文章格式，确保符合项目要求
"""

from pathlib import Path
import re
from datetime import datetime

BLOG_DIR = Path(__file__).parent.parent / "src" / "content" / "blog"


def fix_frontmatter(content, filename):
    """修复 frontmatter 格式"""
    if not content.startswith('---'):
        # 如果没有 frontmatter，添加默认的
        title = filename.replace('.md', '')
        frontmatter = f'''---
title: "{title}"
pubDate: {datetime.now().strftime('%Y-%m-%d')}
---

'''
        return frontmatter + content
    
    # 解析现有的 frontmatter
    parts = content.split('---', 2)
    if len(parts) < 3:
        return content
    
    frontmatter_text = parts[1].strip()
    body = parts[2].strip()
    
    # 解析字段
    frontmatter_dict = {}
    for line in frontmatter_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            frontmatter_dict[key] = value
    
    # 确保必需的字段存在
    if 'title' not in frontmatter_dict:
        frontmatter_dict['title'] = filename.replace('.md', '')
    
    # 处理日期字段
    if 'date' in frontmatter_dict and 'pubDate' not in frontmatter_dict:
        frontmatter_dict['pubDate'] = frontmatter_dict.pop('date')
    elif 'pubDate' not in frontmatter_dict:
        frontmatter_dict['pubDate'] = datetime.now().strftime('%Y-%m-%d')
    
    # 移除不需要的字段（blog 集合不支持 author 和 tags）
    frontmatter_dict.pop('author', None)
    frontmatter_dict.pop('tags', None)
    
    # 重新生成 frontmatter
    frontmatter_lines = ['---']
    for key, value in frontmatter_dict.items():
        if isinstance(value, str) and (' ' in value or ':' in value or '"' in value):
            # 转义引号
            value = value.replace('"', '\\"')
            frontmatter_lines.append(f'{key}: "{value}"')
        else:
            frontmatter_lines.append(f'{key}: {value}')
    frontmatter_lines.append('---')
    
    return '\n\n'.join(['\n'.join(frontmatter_lines), body])


def fix_all_articles():
    """修复所有文章"""
    files = list(BLOG_DIR.glob("*.md"))
    
    print(f"找到 {len(files)} 个文件\n")
    
    fixed = []
    for filepath in files:
        try:
            content = filepath.read_text(encoding='utf-8')
            fixed_content = fix_frontmatter(content, filepath.name)
            
            if fixed_content != content:
                filepath.write_text(fixed_content, encoding='utf-8')
                fixed.append(filepath.name)
                print(f"[OK] 已修复: {filepath.name}")
            else:
                print(f"[SKIP] 无需修复: {filepath.name}")
        except Exception as e:
            print(f"[ERROR] 处理失败 {filepath.name}: {str(e)}")
    
    print(f"\n修复完成！共修复 {len(fixed)} 个文件")


if __name__ == '__main__':
    fix_all_articles()
