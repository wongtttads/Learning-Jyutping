#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成所有字符的粤语例词
输入: jyutping_master.csv (所有字符)
输出: example_words.json (字符到例词的映射)
"""

import pandas as pd
import json
import random
from pathlib import Path

# 路径设置
project_root = Path(__file__).parent.parent
data_dir = project_root / "data" / "processed"
output_dir = project_root / "output" / "data"

# 常见的前缀和后缀字（高频且组合能力强）
COMMON_PREFIXES = ['大', '小', '中', '新', '老', '好', '坏', '高', '低', '长', '短', '多', '少', '快', '慢', '重', '轻', '红', '白', '黑']
COMMON_SUFFIXES = ['子', '头', '人', '家', '工', '手', '口', '心', '力', '气', '水', '火', '山', '石', '金', '木', '土', '日', '月', '年']

# 一些常见双字词模板（字符 + 后缀 或 前缀 + 字符）
# 这些模板会针对每个字符进行调整

def load_characters():
    """加载所有字符数据"""
    csv_path = data_dir / "jyutping_master.csv"
    df = pd.read_csv(csv_path)
    print(f"加载了 {len(df)} 个字符")
    return df

def load_canva_characters():
    """从batch_upload_canva.csv加载所有汉字，用于组合"""
    csv_path = data_dir / "batch_upload_canva.csv"
    if not csv_path.exists():
        print("batch_upload_canva.csv 不存在，跳过")
        return []
    
    df = pd.read_csv(csv_path)
    chars = []
    # 提取所有char_*列中的汉字
    for col in df.columns:
        if col.startswith('char_'):
            chars.extend(df[col].dropna().tolist())
    
    # 去重
    chars = list(set(chars))
    print(f"从batch_upload_canva.csv中提取了 {len(chars)} 个唯一汉字")
    return chars

def generate_example_words(char, canva_chars, char_freq_rank):
    """为单个字符生成两个例词"""
    # 如果字符本身在canva_chars中，使用它作为基础
    # 根据频率决定例词质量：高频字获得更好的例词
    
    examples = []
    
    # 策略1：尝试使用常见前缀/后缀组合
    if char_freq_rank <= 1000:  # 高频字
        # 尝试创建有意义的组合
        if char in COMMON_PREFIXES or char in COMMON_SUFFIXES:
            # 如果字符本身是常见前后缀，尝试与其他字组合
            if char in COMMON_PREFIXES:
                # 作为前缀，加一个后缀
                for suffix in COMMON_SUFFIXES:
                    if suffix != char:
                        examples.append(char + suffix)
                        if len(examples) >= 2:
                            break
            else:
                # 作为后缀，加一个前缀
                for prefix in COMMON_PREFIXES:
                    if prefix != char:
                        examples.append(prefix + char)
                        if len(examples) >= 2:
                            break
        
        # 如果还不够，尝试与canva_chars中的字组合
        if len(examples) < 2:
            for other_char in canva_chars:
                if other_char != char:
                    # 随机选择前后位置
                    if random.random() > 0.5:
                        candidate = char + other_char
                    else:
                        candidate = other_char + char
                    
                    if candidate not in examples:
                        examples.append(candidate)
                        if len(examples) >= 2:
                            break
    
    # 策略2：中频字（1001-3000）
    elif char_freq_rank <= 3000:
        # 随机组合
        attempts = 0
        while len(examples) < 2 and attempts < 20:
            if canva_chars:
                other_char = random.choice(canva_chars)
                if other_char != char:
                    candidate = char + other_char if random.random() > 0.5 else other_char + char
                    if candidate not in examples:
                        examples.append(candidate)
            attempts += 1
    
    # 策略3：低频字（3001+）
    else:
        # 使用简单组合或回退
        if canva_chars:
            for other_char in ['的', '是', '在', '有', '和']:  # 常用虚字
                if other_char != char:
                    examples.append(char + other_char)
                    if len(examples) >= 2:
                        break
        
        # 如果还不够，使用回退
        while len(examples) < 2:
            examples.append(f"{char}字")
            if len(examples) < 2:
                examples.append(f"{char}词")
                break
    
    # 确保有两个例词
    if len(examples) < 2:
        examples.extend([f"{char}字", f"{char}词"])
    
    return examples[:2]

def main():
    """主函数"""
    print("开始生成粤语例词...")
    
    # 加载数据
    char_df = load_characters()
    canva_chars = load_canva_characters()
    
    # 生成例词映射
    example_map = {}
    
    for idx, row in char_df.iterrows():
        char = row['char']
        freq_rank = row['frequency_rank']
        
        # 跳过非汉字或空字符
        if not char or len(char) != 1:
            continue
        
        # 生成例词
        examples = generate_example_words(char, canva_chars, freq_rank)
        example_map[char] = examples
        
        # 进度显示
        if (idx + 1) % 500 == 0:
            print(f"已处理 {idx + 1} 个字符")
    
    print(f"生成了 {len(example_map)} 个字符的例词")
    
    # 保存为JSON
    output_path = output_dir / "example_words.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(example_map, f, ensure_ascii=False, indent=2)
    
    print(f"例词映射已保存到: {output_path}")
    
    # 也生成一个JavaScript版本的映射（用于直接嵌入HTML）
    js_output_path = output_dir / "example_words.js"
    with open(js_output_path, 'w', encoding='utf-8') as f:
        f.write("// 自动生成的粤语例词映射\n")
        f.write("const exampleWordsMap = ")
        json.dump(example_map, f, ensure_ascii=False, indent=2)
        f.write(";\n")
    
    print(f"JavaScript版本已保存到: {js_output_path}")
    
    # 打印一些示例
    print("\n示例字符的例词:")
    sample_chars = ['口', '山', '水', '人', '天', '地', '日', '月', '风', '雨']
    for sample in sample_chars:
        if sample in example_map:
            print(f"  {sample}: {example_map[sample]}")

if __name__ == "__main__":
    main()