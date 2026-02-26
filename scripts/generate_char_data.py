#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成字符数据文件，按章节分割
"""

import pandas as pd
import json
import math
from pathlib import Path

def load_data():
    """加载数据文件"""
    data_dir = Path(__file__).parent.parent / "data" / "processed"
    
    # 加载主数据
    main_df = pd.read_csv(data_dir / "jyutping_master.csv")
    print(f"加载主数据: {len(main_df)} 行")
    
    return main_df

def create_chapter_characters(df, num_chapters=10):
    """创建章节字符数据"""
    total_chars = len(df)
    chars_per_chapter = math.ceil(total_chars / num_chapters)
    chapter_characters = {}
    
    for i in range(num_chapters):
        start_idx = i * chars_per_chapter
        end_idx = min((i + 1) * chars_per_chapter, total_chars)
        if start_idx >= total_chars:
            break
        
        chapter_chars = df.iloc[start_idx:end_idx]
        chapter_id = i + 1
        
        # 转换为列表格式
        chars_list = []
        for _, row in chapter_chars.iterrows():
            # 处理可能的NaN值
            tone = row['tone']
            if pd.isna(tone):
                tone = 1  # 默认值
            
            frequency_rank = row['frequency_rank']
            if pd.isna(frequency_rank):
                frequency_rank = 9999  # 默认值
            
            chars_list.append({
                "char": row['char'],
                "jyutping": row['jyutping'],
                "tone": int(tone),
                "frequency_rank": int(frequency_rank)
            })
        
        chapter_characters[chapter_id] = chars_list
        print(f"章节 {chapter_id}: {len(chars_list)} 个字符")
    
    return chapter_characters

def save_chapter_data(chapter_characters):
    """保存章节数据到JSON文件"""
    output_dir = Path(__file__).parent.parent / "output" / "data"
    output_dir.mkdir(exist_ok=True)
    
    # 保存为单个JSON文件
    output_file = output_dir / "chapter_characters.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(chapter_characters, f, ensure_ascii=False, indent=2)
    
    print(f"字符数据已保存到: {output_file}")
    
    # 同时保存为按章节分割的文件
    for chapter_id, chars in chapter_characters.items():
        chapter_file = output_dir / f"chapter_{chapter_id}_characters.json"
        with open(chapter_file, 'w', encoding='utf-8') as f:
            json.dump(chars, f, ensure_ascii=False, indent=2)
    
    print(f"已生成 {len(chapter_characters)} 个章节的字符数据文件")

def main():
    """主函数"""
    print("开始生成字符数据...")
    
    # 加载数据
    df = load_data()
    
    # 创建章节字符数据
    chapter_characters = create_chapter_characters(df)
    
    # 保存数据
    save_chapter_data(chapter_characters)
    
    print("字符数据生成完成！")

if __name__ == "__main__":
    main()