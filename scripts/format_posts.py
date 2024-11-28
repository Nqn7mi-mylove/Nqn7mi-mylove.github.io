import os
import re
from datetime import datetime

def format_post_file(file_path):
    # 获取文件名和目录
    dir_path = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    
    # 检查文件是否已经有日期前缀
    date_pattern = r'^\d{4}-\d{1,2}-\d{1,2}-'
    if not re.match(date_pattern, file_name):
        # 获取文件的修改时间
        file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        date_prefix = file_time.strftime('%Y-%m-%d-')
        new_file_name = date_prefix + file_name
        new_file_path = os.path.join(dir_path, new_file_name)
        
        # 重命名文件
        os.rename(file_path, new_file_path)
        file_path = new_file_path
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经有YAML头部
    if not content.startswith('---\n'):
        # 从文件名提取标题
        title = os.path.splitext(os.path.basename(file_path))[0]
        title = re.sub(r'^\d{4}-\d{1,2}-\d{1,2}-', '', title)  # 移除日期前缀
        title = title+"题解"
        # 创建YAML头部
        yaml_header = f'''---
layout: post
title: {title}
date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} +0800
categories: Atcoder
---

'''
        # 添加头部到内容
        content = yaml_header + content
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Processed: {file_path}")

def process_posts_directory(posts_dir):
    # 遍历_posts目录
    for file_name in os.listdir(posts_dir):
        if file_name.endswith('.md') or file_name.endswith('.markdown'):
            file_path = os.path.join(posts_dir, file_name)
            format_post_file(file_path)

if __name__ == '__main__':
    # 获取脚本所在目录的父目录（即博客根目录）
    blog_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    posts_dir = os.path.join(blog_root, '_posts')
    
    if os.path.exists(posts_dir):
        process_posts_directory(posts_dir)
        print("All posts have been processed!")
    else:
        print(f"Error: Posts directory not found at {posts_dir}")
