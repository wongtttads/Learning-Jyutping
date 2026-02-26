#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改进的粤语例词生成器
使用更智能的算法生成有意义的例词
"""

import pandas as pd
import json
import random
from pathlib import Path
from collections import defaultdict

project_root = Path(__file__).parent.parent
data_dir = project_root / "data" / "processed"
output_dir = project_root / "output" / "data"

class CantoneseExampleGenerator:
    def __init__(self):
        self.char_df = None
        self.char_freq = {}
        self.common_words = self.load_common_words()
        self.prefix_suffix_map = self.build_prefix_suffix_map()
        
    def load_common_words(self):
        """加载常见粤语词汇"""
        common_words = {
            '名词': ['人', '家', '工', '手', '口', '心', '力', '气', '水', '火', 
                    '山', '石', '金', '木', '土', '日', '月', '年', '天', '地',
                    '车', '船', '书', '笔', '纸', '钱', '饭', '菜', '酒', '茶'],
            '动词': ['做', '去', '来', '看', '听', '讲', '食', '饮', '买', '卖',
                    '学', '教', '写', '读', '问', '答', '走', '跑', '坐', '睡'],
            '形容词': ['大', '小', '好', '坏', '新', '旧', '多', '少', '快', '慢',
                      '长', '短', '高', '低', '重', '轻', '红', '白', '黑', '蓝'],
            '副词': ['好', '好', '好', '好', '好', '好', '好', '好', '好', '好',
                    '唔', '唔', '唔', '唔', '唔', '唔', '唔', '唔', '唔', '唔'],
            '量词': ['个', '只', '条', '张', '件', '本', '支', '杯', '碗', '盘'],
            '助词': ['嘅', '咗', '紧', '过', '呀', '呢', '吗', '啦', '喔', '咩']
        }
        
        all_words = []
        for category, words in common_words.items():
            all_words.extend(words)
        
        return list(set(all_words))
    
    def build_prefix_suffix_map(self):
        """构建常见前缀后缀映射"""
        return {
            'prefixes': {
                '大': ['小', '中', '老', '新', '好'],
                '小': ['大', '中', '老', '新'],
                '老': ['小', '大', '新'],
                '新': ['老', '旧', '大'],
                '好': ['坏', '差', '大'],
                '坏': ['好', '大'],
                '大': ['小', '中'],
                '小': ['大', '中'],
            },
            'suffixes': {
                '人': ['大', '小', '老', '好', '坏', '男', '女', '中', '外'],
                '家': ['大', '小', '老', '新', '好', '坏'],
                '工': ['做', '打', '学', '教'],
                '手': ['做', '打', '学', '教'],
                '口': ['大', '小', '好', '坏'],
                '心': ['好', '坏', '大', '小'],
                '力': ['大', '小', '好', '坏'],
                '气': ['大', '小', '好', '坏'],
                '水': ['大', '小', '好', '坏'],
                '火': ['大', '小', '好', '坏'],
                '山': ['大', '小', '好', '坏'],
                '石': ['大', '小', '好', '坏'],
                '金': ['大', '小', '好', '坏'],
                '木': ['大', '小', '好', '坏'],
                '土': ['大', '小', '好', '坏'],
                '日': ['大', '小', '好', '坏'],
                '月': ['大', '小', '好', '坏'],
                '年': ['大', '小', '好', '坏'],
                '天': ['大', '小', '好', '坏'],
                '地': ['大', '小', '好', '坏'],
                '车': ['大', '小', '好', '坏'],
                '船': ['大', '小', '好', '坏'],
                '书': ['大', '小', '好', '坏'],
                '笔': ['大', '小', '好', '坏'],
                '纸': ['大', '小', '好', '坏'],
                '钱': ['大', '小', '好', '坏'],
                '饭': ['大', '小', '好', '坏'],
                '菜': ['大', '小', '好', '坏'],
                '酒': ['大', '小', '好', '坏'],
                '茶': ['大', '小', '好', '坏'],
            }
        }
    
    def load_data(self):
        """加载数据"""
        csv_path = data_dir / "jyutping_master.csv"
        self.char_df = pd.read_csv(csv_path)
        
        for _, row in self.char_df.iterrows():
            self.char_freq[row['char']] = row['frequency_rank']
        
        print(f"加载了 {len(self.char_df)} 个字符")
    
    def is_common_char(self, char):
        """判断是否为常见字符"""
        return char in self.common_words
    
    def generate_examples_for_char(self, char):
        """为单个字符生成例词"""
        examples = []
        freq_rank = self.char_freq.get(char, 9999)
        
        if freq_rank <= 500:
            examples = self.generate_high_freq_examples(char)
        elif freq_rank <= 2000:
            examples = self.generate_mid_freq_examples(char)
        else:
            examples = self.generate_low_freq_examples(char)
        
        return examples[:2]
    
    def generate_high_freq_examples(self, char):
        """为高频字生成例词"""
        examples = []
        
        if char in self.prefix_suffix_map['suffixes']:
            prefixes = self.prefix_suffix_map['suffixes'][char]
            for prefix in prefixes:
                if prefix != char:
                    examples.append(prefix + char)
                    if len(examples) >= 2:
                        break
        
        if len(examples) < 2:
            for word in self.common_words:
                if word != char:
                    examples.append(char + word)
                    if len(examples) >= 2:
                        break
        
        return examples
    
    def generate_mid_freq_examples(self, char):
        """为中频字生成例词"""
        examples = []
        
        for word in self.common_words:
            if word != char:
                if random.random() > 0.5:
                    examples.append(char + word)
                else:
                    examples.append(word + char)
                if len(examples) >= 2:
                    break
        
        return examples
    
    def generate_low_freq_examples(self, char):
        """为低频字生成例词"""
        examples = []
        
        for word in ['的', '是', '在', '有', '和', '了', '不', '我', '你', '他']:
            if word != char:
                examples.append(char + word)
                if len(examples) >= 2:
                    break
        
        if len(examples) < 2:
            examples.append(f"{char}字")
            examples.append(f"{char}词")
        
        return examples
    
    def generate_all_examples(self):
        """为所有字符生成例词"""
        example_map = {}
        
        for idx, row in self.char_df.iterrows():
            char = row['char']
            
            if not char or len(char) != 1:
                continue
            
            examples = self.generate_examples_for_char(char)
            example_map[char] = examples
            
            if (idx + 1) % 500 == 0:
                print(f"已处理 {idx + 1} 个字符")
        
        return example_map
    
    def save_examples(self, example_map):
        """保存例词"""
        output_path = output_dir / "example_words_v2.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(example_map, f, ensure_ascii=False, indent=2)
        
        print(f"例词已保存到: {output_path}")
        
        js_output_path = output_dir / "example_words_v2.js"
        with open(js_output_path, 'w', encoding='utf-8') as f:
            f.write("// 改进的粤语例词映射\n")
            f.write("const exampleWordsMapV2 = ")
            json.dump(example_map, f, ensure_ascii=False, indent=2)
            f.write(";\n")
        
        print(f"JavaScript版本已保存到: {js_output_path}")
        
        print("\n示例字符的例词:")
        sample_chars = ['口', '山', '水', '人', '天', '地', '日', '月', '风', '雨']
        for sample in sample_chars:
            if sample in example_map:
                print(f"  {sample}: {example_map[sample]}")

def main():
    print("开始生成改进的粤语例词...")
    
    generator = CantoneseExampleGenerator()
    generator.load_data()
    
    example_map = generator.generate_all_examples()
    generator.save_examples(example_map)
    
    print(f"\n生成了 {len(example_map)} 个字符的例词")
    print("例词生成完成！")

if __name__ == "__main__":
    main()
