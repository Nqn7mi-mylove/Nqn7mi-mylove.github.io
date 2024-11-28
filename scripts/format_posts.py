import os
import re
from datetime import datetime

def format_title(title):
    # 替换 ABC 为完整比赛名称，题解替换为 Solution
    title = title.replace('ABC', 'AtCoder Beginner Contest ')
    title = title.replace('题解', 'Solution')
    return title

def extract_date_from_filename(file_name):
    # 从文件名提取日期
    date_match = re.match(r'(\d{4})-(\d{1,2})-(\d{1,2})', file_name)
    if date_match:
        year, month, day = map(int, date_match.groups())
        # 设置为当天中午12点
        return datetime(year, month, day, 12, 0, 0)
    return datetime.now()

def update_or_create_yaml_header(content, title, post_date):
    yaml_header = f'''---
layout: post
title: {title}
excerpt: {title.replace('Solution', '题解')}
date: {post_date.strftime('%Y-%m-%d %H:%M:%S')} +0800
categories: AtCoder
---

'''
    if content.startswith('---\n'):
        # 找到第二个 '---' 的位置
        end_of_yaml = content.find('---', 4)
        if end_of_yaml != -1:
            # 保留正文内容
            content = content[end_of_yaml + 4:]  # +4 to skip '---\n'
    return yaml_header + content

def format_post_file(file_path):
    # 获取文件名和目录
    dir_path = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    original_file_name = file_name
    
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
        file_name = new_file_name
        print(f"Renamed: {original_file_name} -> {file_name}")
    
    # 读取文件内容
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        print(f"Warning: Unable to read {file_path} with UTF-8 encoding, skipping...")
        return
    
    # 从文件名提取标题
    title = os.path.splitext(os.path.basename(file_path))[0]
    title = re.sub(r'^\d{4}-\d{1,2}-\d{1,2}-', '', title)  # 移除日期前缀
    if not title.endswith('Solution'):
        title = title + " Solution"
    
    # 格式化标题
    title = format_title(title)
    
    # 从文件名获取日期并设置为中午12点
    post_date = extract_date_from_filename(file_name)
    
    # 更新或创建YAML头部
    new_content = update_or_create_yaml_header(content, title, post_date)
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    if content.startswith('---\n'):
        print(f"Updated YAML header in: {file_path}")
    else:
        print(f"Added YAML header to: {file_path}")

def process_posts_directory(posts_dir):
    # 遍历_posts目录
    processed_count = 0
    skipped_count = 0
    error_count = 0
    
    for file_name in os.listdir(posts_dir):
        if file_name.endswith('.md') or file_name.endswith('.markdown'):
            try:
                file_path = os.path.join(posts_dir, file_name)
                format_post_file(file_path)
                processed_count += 1
            except Exception as e:
                print(f"Error processing {file_name}: {str(e)}")
                error_count += 1
        else:
            skipped_count += 1
    
    print(f"\nSummary:")
    print(f"Processed: {processed_count} files")
    print(f"Skipped: {skipped_count} files (not markdown)")
    print(f"Errors: {error_count} files")

if __name__ == '__main__':
    # 获取脚本所在目录的父目录（即博客根目录）
    blog_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    posts_dir = os.path.join(blog_root, '_posts')
    
    if os.path.exists(posts_dir):
        print(f"Processing files in: {posts_dir}")
        process_posts_directory(posts_dir)
    else:
        print(f"Error: Posts directory not found at {posts_dir}")
