#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据清理脚本 - 清理无效字符和修复拼音问题
"""

import pandas as pd
import json
import re
from pathlib import Path

# 定义有效的Unicode范围
VALID_UNICODE_RANGES = [
    (0x4E00, 0x9FFF),   # 基本汉字
    (0x3400, 0x4DBF),   # 扩展A
    (0x20000, 0x2A6DF),  # 扩展B
    (0x2A700, 0x2B73F),  # 扩展C
    (0x2B740, 0x2B81F),  # 扩展D
    (0x2B820, 0x2CEAF),  # 扩展E
    (0xF900, 0xFAFF),    # 兼容汉字
    (0x2F800, 0x2FA1F),  # 兼容补充
]

def is_valid_chinese_char(char):
    """检查字符是否为有效的中文字符"""
    code = ord(char)
    for start, end in VALID_UNICODE_RANGES:
        if start <= code <= end:
            return True
    return False

def clean_master_db():
    """清理主数据库"""
    print("=" * 60)
    print("清理主数据库")
    print("=" * 60)
    
    input_file = Path("data/processed/jyutping_master.csv")
    output_file = Path("data/processed/jyutping_master_cleaned.csv")
    
    # 读取数据
    df = pd.read_csv(input_file)
    print(f"原始记录数: {len(df)}")
    
    # 过滤无效字符
    df['is_valid_char'] = df['char'].apply(is_valid_chinese_char)
    invalid_chars = df[~df['is_valid_char']]
    print(f"发现 {len(invalid_chars)} 个无效字符")
    
    if len(invalid_chars) > 0:
        print("\n无效字符示例:")
        print(invalid_chars[['char', 'jyutping']].head(10).to_string(index=False))
    
    # 移除无效字符
    df_cleaned = df[df['is_valid_char']].copy()
    
    # 过滤拼音为nan的记录
    df_cleaned = df_cleaned[df_cleaned['jyutping'] != 'nan']
    print(f"移除拼音为nan的记录后: {len(df_cleaned)}")
    
    # 过滤拼音为空的记录
    df_cleaned = df_cleaned[df_cleaned['jyutping'].notna()]
    df_cleaned = df_cleaned[df_cleaned['jyutping'] != '']
    print(f"移除拼音为空的记录后: {len(df_cleaned)}")
    
    # 移除临时列
    df_cleaned = df_cleaned.drop('is_valid_char', axis=1)
    
    # 保存清理后的数据
    df_cleaned.to_csv(output_file, index=False, encoding='utf-8')
    print(f"\n清理后的数据已保存到: {output_file}")
    print(f"清理后记录数: {len(df_cleaned)}")
    print(f"移除的记录数: {len(df) - len(df_cleaned)}")
    
    return df_cleaned

def clean_chapter_data(df_cleaned):
    """清理章节数据"""
    print("\n" + "=" * 60)
    print("清理章节数据")
    print("=" * 60)
    
    chapter_file = Path("output/data/chapter_characters.json")
    output_file = Path("output/data/chapter_characters_cleaned.json")
    
    # 读取章节数据
    with open(chapter_file, 'r', encoding='utf-8') as f:
        chapter_data = json.load(f)
    
    print(f"原始章节数据: {len(chapter_data)} 个章节")
    
    # 创建有效字符集合
    valid_chars = set(df_cleaned['char'].tolist())
    print(f"有效字符数: {len(valid_chars)}")
    
    # 清理每个章节
    cleaned_chapter_data = {}
    total_removed = 0
    
    for chapter_id, chars in chapter_data.items():
        cleaned_chars = []
        removed_count = 0
        
        for char_data in chars:
            char = char_data['char']
            
            # 检查字符是否有效
            if char not in valid_chars:
                removed_count += 1
                continue
            
            # 检查拼音是否有效
            if char_data.get('jyutping') == 'nan' or not char_data.get('jyutping'):
                removed_count += 1
                continue
            
            cleaned_chars.append(char_data)
        
        cleaned_chapter_data[chapter_id] = cleaned_chars
        total_removed += removed_count
        
        print(f"章节 {chapter_id}: 原始 {len(chars)} 个, 清理后 {len(cleaned_chars)} 个, 移除 {removed_count} 个")
    
    # 保存清理后的章节数据
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_chapter_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n清理后的章节数据已保存到: {output_file}")
    print(f"总共移除 {total_removed} 个无效字符")
    
    return cleaned_chapter_data

def validate_cleaned_data():
    """验证清理后的数据"""
    print("\n" + "=" * 60)
    print("验证清理后的数据")
    print("=" * 60)
    
    # 验证主数据库
    master_file = Path("data/processed/jyutping_master_cleaned.csv")
    df = pd.read_csv(master_file)
    
    print(f"主数据库记录数: {len(df)}")
    print(f"拼音为空的记录数: {df['jyutping'].isna().sum()}")
    print(f"拼音为nan的记录数: {(df['jyutping'] == 'nan').sum()}")
    
    # 验证章节数据
    chapter_file = Path("output/data/chapter_characters_cleaned.json")
    with open(chapter_file, 'r', encoding='utf-8') as f:
        chapter_data = json.load(f)
    
    print(f"\n章节数据:")
    total_chars = 0
    for chapter_id, chars in chapter_data.items():
        invalid_count = sum(1 for c in chars if c.get('jyutping') == 'nan' or not c.get('jyutping'))
        print(f"  章节 {chapter_id}: {len(chars)} 个字符, 无效拼音: {invalid_count}")
        total_chars += len(chars)
    
    print(f"总字符数: {total_chars}")

def main():
    print("开始数据清理...")
    print()
    
    # 清理主数据库
    df_cleaned = clean_master_db()
    
    # 清理章节数据
    clean_chapter_data(df_cleaned)
    
    # 验证清理后的数据
    validate_cleaned_data()
    
    print("\n" + "=" * 60)
    print("数据清理完成！")
    print("=" * 60)
    print("\n下一步:")
    print("1. 检查清理后的数据文件")
    print("2. 如果满意，替换原始文件:")
    print("   mv data/processed/jyutping_master_cleaned.csv data/processed/jyutping_master.csv")
    print("   mv output/data/chapter_characters_cleaned.json output/data/chapter_characters.json")
    print("3. 重新运行验证脚本确认数据质量")

if __name__ == "__main__":
    main()