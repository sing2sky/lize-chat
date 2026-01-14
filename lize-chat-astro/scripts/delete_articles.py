#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
删除文章脚本
"""

from pathlib import Path
import sys

BLOG_DIR = Path(__file__).parent.parent / "src" / "content" / "blog"
DIALOGUE_DIR = Path(__file__).parent.parent / "src" / "content" / "dialogue"


def delete_articles(filenames):
    """删除指定的文章文件"""
    deleted = []
    not_found = []
    
    for filename in filenames:
        # 尝试在 blog 目录查找
        blog_file = BLOG_DIR / filename
        dialogue_file = DIALOGUE_DIR / filename
        
        if blog_file.exists():
            blog_file.unlink()
            deleted.append(('blog', filename))
            print(f"✅ 已删除: blog/{filename}")
        elif dialogue_file.exists():
            dialogue_file.unlink()
            deleted.append(('dialogue', filename))
            print(f"✅ 已删除: dialogue/{filename}")
        else:
            not_found.append(filename)
            print(f"❌ 未找到: {filename}")
    
    print(f"\n删除完成: 成功 {len(deleted)} 个，未找到 {len(not_found)} 个")
    return deleted, not_found


def list_all_articles():
    """列出所有文章供参考"""
    print("\n当前所有文章:")
    blog_files = list(BLOG_DIR.glob("*.md"))
    dialogue_files = list(DIALOGUE_DIR.glob("*.md"))
    
    if blog_files:
        print("\n📝 Blog 文章:")
        for f in blog_files:
            print(f"  - {f.name}")
    
    if dialogue_files:
        print("\n💬 Dialogue 文章:")
        for f in dialogue_files:
            print(f"  - {f.name}")
    
    if not blog_files and not dialogue_files:
        print("  (无文章)")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python delete_articles.py <文件名1> [文件名2] ...")
        print("\n示例:")
        print("  python delete_articles.py first-conversation.md second-conversation.md")
        print()
        list_all_articles()
        sys.exit(1)
    
    filenames = sys.argv[1:]
    print(f"准备删除 {len(filenames)} 个文件...")
    deleted, not_found = delete_articles(filenames)
    
    if not_found:
        print("\n未找到的文件:")
        for f in not_found:
            print(f"  - {f}")
        print("\n提示: 运行 'python list_articles.py' 查看所有文章")
