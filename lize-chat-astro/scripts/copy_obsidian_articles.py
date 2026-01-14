#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 Obsidian Vault 复制文章到项目
"""

import shutil
from pathlib import Path
import re
from datetime import datetime

# 源目录和目标目录
SOURCE_DIR = Path(r"D:\Documents\Obsidian Vault\lizechat\lize-chat-astro\src\content\blog")
TARGET_DIR = Path(__file__).parent.parent / "src" / "content" / "blog"

TARGET_DIR.mkdir(parents=True, exist_ok=True)


def sanitize_filename(filename):
    """清理文件名，移除特殊字符"""
    # 保留中文、英文、数字、连字符、下划线和空格
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    return filename


def ensure_frontmatter(content, filepath):
    """确保文件有正确的 frontmatter"""
    # 检查是否已有 frontmatter
    if content.startswith('---'):
        # 提取现有的 frontmatter
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter_text = parts[1].strip()
            body = parts[2].strip()
            
            # 解析 frontmatter
            frontmatter = {}
            for line in frontmatter_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    frontmatter[key] = value
            
            # 确保有必需的字段
            if 'pubDate' not in frontmatter and 'date' not in frontmatter:
                # 尝试从文件名或内容中提取日期，否则使用当前日期
                frontmatter['pubDate'] = datetime.now().strftime('%Y-%m-%d')
            elif 'date' in frontmatter:
                # 将 date 转换为 pubDate（blog 集合使用 pubDate）
                frontmatter['pubDate'] = frontmatter.pop('date')
            
            # 重新生成 frontmatter
            new_frontmatter_lines = ['---']
            for key, value in frontmatter.items():
                if isinstance(value, str) and (' ' in value or ':' in value):
                    new_frontmatter_lines.append(f'{key}: "{value}"')
                else:
                    new_frontmatter_lines.append(f'{key}: {value}')
            new_frontmatter_lines.append('---')
            
            return '\n\n'.join(['\n'.join(new_frontmatter_lines), body])
    
    # 如果没有 frontmatter，从文件名生成
    filename = filepath.stem
    title = filename
    
    # 生成默认 frontmatter
    frontmatter = f"""---
title: "{title}"
pubDate: {datetime.now().strftime('%Y-%m-%d')}
---

"""
    
    return frontmatter + content


def copy_articles():
    """复制文章文件"""
    if not SOURCE_DIR.exists():
        print(f"[ERROR] 源目录不存在: {SOURCE_DIR}")
        return
    
    files = list(SOURCE_DIR.glob("*.md"))
    
    if not files:
        print(f"[ERROR] 源目录中没有找到 Markdown 文件")
        return
    
    print(f"源目录: {SOURCE_DIR}")
    print(f"目标目录: {TARGET_DIR}")
    print(f"找到 {len(files)} 个文件\n")
    
    copied = []
    skipped = []
    errors = []
    
    for source_file in files:
        try:
            # 读取文件内容
            content = source_file.read_text(encoding='utf-8')
            
            # 确保有正确的 frontmatter
            content = ensure_frontmatter(content, source_file)
            
            # 目标文件名
            target_filename = sanitize_filename(source_file.name)
            target_file = TARGET_DIR / target_filename
            
            # 如果文件已存在，询问是否覆盖（这里直接覆盖）
            if target_file.exists():
                print(f"[!] 文件已存在，将覆盖: {target_filename}")
            
            # 写入目标文件
            target_file.write_text(content, encoding='utf-8')
            
            copied.append(target_filename)
            print(f"[OK] 已复制: {target_filename}")
            
        except Exception as e:
            errors.append((source_file.name, str(e)))
            print(f"[ERROR] 复制失败 {source_file.name}: {str(e)}")
    
    # 打印总结
    print("\n" + "="*60)
    print("复制完成！")
    print("="*60)
    print(f"成功: {len(copied)}")
    if errors:
        print(f"失败: {len(errors)}")
        for filename, error in errors:
            print(f"  - {filename}: {error}")
    
    if copied:
        print("\n已复制的文件:")
        for filename in copied:
            print(f"  [OK] {filename}")


if __name__ == '__main__':
    copy_articles()
