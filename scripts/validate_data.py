#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据质量验证测试
"""

import pandas as pd
import json
from pathlib import Path
import re

project_root = Path(__file__).parent.parent
data_dir = project_root / "data" / "processed"
output_dir = project_root / "output" / "data"

class DataQualityValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.stats = {}
        
        # 定义有效的Unicode范围
        self.valid_unicode_ranges = [
            (0x4E00, 0x9FFF),   # 基本汉字
            (0x3400, 0x4DBF),   # 扩展A
            (0x20000, 0x2A6DF),  # 扩展B
            (0x2A700, 0x2B73F),  # 扩展C
            (0x2B740, 0x2B81F),  # 扩展D
            (0x2B820, 0x2CEAF),  # 扩展E
            (0xF900, 0xFAFF),    # 兼容汉字
            (0x2F800, 0x2FA1F),  # 兼容补充
        ]
    
    def is_valid_chinese_char(self, char):
        """检查字符是否为有效的中文字符"""
        if not isinstance(char, str) or len(char) != 1:
            return False
        code = ord(char)
        for start, end in self.valid_unicode_ranges:
            if start <= code <= end:
                return True
        return False
    
    def validate_master_db(self):
        """验证主数据库"""
        print("=" * 60)
        print("验证主数据库 (jyutping_master.csv)")
        print("=" * 60)
        
        csv_path = data_dir / "jyutping_master.csv"
        
        if not csv_path.exists():
            self.errors.append("主数据库文件不存在")
            return False
        
        df = pd.read_csv(csv_path)
        
        print(f"总记录数: {len(df)}")
        self.stats['total_records'] = len(df)
        
        # 检查必填字段
        required_fields = ['char', 'jyutping', 'onset', 'final', 'tone', 'level', 'frequency_rank']
        for field in required_fields:
            if field not in df.columns:
                self.errors.append(f"缺少必填字段: {field}")
            else:
                null_count = df[field].isnull().sum()
                if null_count > 0:
                    self.warnings.append(f"字段 {field} 有 {null_count} 个空值")
        
        # 检查字符有效性
        invalid_chars = df[~df['char'].apply(self.is_valid_chinese_char)]
        if len(invalid_chars) > 0:
            self.errors.append(f"发现 {len(invalid_chars)} 个无效字符")
        
        # 检查拼音格式
        invalid_jyutping = df[df['jyutping'].notna() & ~df['jyutping'].apply(self._is_valid_jyutping)]
        if len(invalid_jyutping) > 0:
            self.warnings.append(f"发现 {len(invalid_jyutping)} 个拼音格式可能不正确")
        
        # 检查声调范围
        invalid_tones = df[df['tone'].notna() & ~df['tone'].apply(lambda x: x in [1, 2, 3, 4, 5, 6])]
        if len(invalid_tones) > 0:
            self.errors.append(f"发现 {len(invalid_tones)} 个无效声调")
        
        # 检查级别
        invalid_levels = df[~df['level'].isin([1, 2, 3])]
        if len(invalid_levels) > 0:
            self.errors.append(f"发现 {len(invalid_levels)} 个无效级别")
        
        # 检查重复字符
        duplicate_chars = df[df.duplicated(subset=['char'], keep=False)]
        if len(duplicate_chars) > 0:
            self.warnings.append(f"发现 {len(duplicate_chars)} 个重复字符")
        
        # 统计各级别数量
        level_counts = df['level'].value_counts().sort_index()
        print("\n各级别字符数量:")
        for level, count in level_counts.items():
            print(f"  级别 {level}: {count} 个字符")
        
        self.stats['level_counts'] = level_counts.to_dict()
        
        # 检查缺失拼音
        missing_jyutping = df[df['jyutping'].isna()]
        if len(missing_jyutping) > 0:
            self.warnings.append(f"有 {len(missing_jyutping)} 个字符缺失拼音")
        
        return len(self.errors) == 0
    
    def _is_valid_jyutping(self, jp):
        """检查拼音格式是否有效"""
        if not isinstance(jp, str):
            return False
        
        pattern = r'^[a-z]+[1-6]$'
        return bool(re.match(pattern, jp))
    
    def validate_chapter_data(self):
        """验证章节数据"""
        print("\n" + "=" * 60)
        print("验证章节数据 (chapter_characters.json)")
        print("=" * 60)
        
        json_path = output_dir / "chapter_characters.json"
        
        if not json_path.exists():
            self.errors.append("章节数据文件不存在")
            return False
        
        with open(json_path, 'r', encoding='utf-8') as f:
            chapter_data = json.load(f)
        
        print(f"章节数量: {len(chapter_data)}")
        self.stats['chapter_count'] = len(chapter_data)
        
        total_chars = 0
        for chapter_id, chars in chapter_data.items():
            print(f"\n章节 {chapter_id}: {len(chars)} 个字符")
            total_chars += len(chars)
            
            # 检查每个字符的数据结构
            for i, char_data in enumerate(chars):
                if not isinstance(char_data, dict):
                    self.errors.append(f"章节 {chapter_id} 第 {i+1} 个字符数据格式错误")
                    continue
                
                required_fields = ['char', 'jyutping', 'tone', 'frequency_rank']
                for field in required_fields:
                    if field not in char_data:
                        self.errors.append(f"章节 {chapter_id} 第 {i+1} 个字符缺少字段: {field}")
        
        print(f"\n总字符数: {total_chars}")
        self.stats['total_chars_in_chapters'] = total_chars
        
        # 检查各章节文件
        for chapter_id in range(1, 11):
            chapter_file = output_dir / f"chapter_{chapter_id}_characters.json"
            if chapter_file.exists():
                with open(chapter_file, 'r', encoding='utf-8') as f:
                    chapter_chars = json.load(f)
                    print(f"章节 {chapter_id} 文件: {len(chapter_chars)} 个字符")
            else:
                self.warnings.append(f"章节 {chapter_id} 文件不存在")
        
        return len(self.errors) == 0
    
    def validate_example_words(self):
        """验证例词数据"""
        print("\n" + "=" * 60)
        print("验证例词数据 (example_words.json)")
        print("=" * 60)
        
        json_path = output_dir / "example_words.json"
        
        if not json_path.exists():
            self.errors.append("例词数据文件不存在")
            return False
        
        with open(json_path, 'r', encoding='utf-8') as f:
            example_words = json.load(f)
        
        print(f"例词映射数量: {len(example_words)}")
        self.stats['example_words_count'] = len(example_words)
        
        # 检查每个字符的例词
        invalid_examples = 0
        for char, examples in example_words.items():
            if not isinstance(examples, list) or len(examples) != 2:
                self.errors.append(f"字符 {char} 的例词格式错误")
                invalid_examples += 1
                continue
            
            for example in examples:
                if not isinstance(example, str) or len(example) < 2:
                    self.warnings.append(f"字符 {char} 的例词 '{example}' 可能无效")
        
        if invalid_examples > 0:
            print(f"发现 {invalid_examples} 个字符的例词格式错误")
        else:
            print("所有例词格式正确")
        
        # 显示一些示例
        print("\n示例字符的例词:")
        sample_chars = ['一', '二', '三', '口', '山', '水']
        for char in sample_chars:
            if char in example_words:
                print(f"  {char}: {example_words[char]}")
        
        return len(self.errors) == 0
    
    def validate_consistency(self):
        """验证数据一致性"""
        print("\n" + "=" * 60)
        print("验证数据一致性")
        print("=" * 60)
        
        # 加载主数据库
        csv_path = data_dir / "jyutping_master.csv"
        df = pd.read_csv(csv_path)
        
        # 加载章节数据
        json_path = output_dir / "chapter_characters.json"
        with open(json_path, 'r', encoding='utf-8') as f:
            chapter_data = json.load(f)
        
        # 检查字符数量一致性
        master_chars = set(df['char'].dropna().tolist())
        chapter_chars = set()
        
        for chars in chapter_data.values():
            for char_data in chars:
                chapter_chars.add(char_data['char'])
        
        print(f"主数据库字符数: {len(master_chars)}")
        print(f"章节数据字符数: {len(chapter_chars)}")
        
        # 检查差异
        only_in_master = master_chars - chapter_chars
        only_in_chapters = chapter_chars - master_chars
        
        if only_in_master:
            self.warnings.append(f"只在主数据库中的字符: {len(only_in_master)} 个")
        
        if only_in_chapters:
            self.warnings.append(f"只在章节数据中的字符: {len(only_in_chapters)} 个")
        
        # 检查拼音一致性
        inconsistent = 0
        for char in master_chars & chapter_chars:
            master_row = df[df['char'] == char].iloc[0]
            master_jp = master_row['jyutping']
            
            for chars in chapter_data.values():
                for char_data in chars:
                    if char_data['char'] == char:
                        chapter_jp = char_data['jyutping']
                        if master_jp != chapter_jp:
                            self.errors.append(f"字符 {char} 的拼音不一致: 主数据库={master_jp}, 章节数据={chapter_jp}")
                            inconsistent += 1
        
        if inconsistent > 0:
            print(f"发现 {inconsistent} 个字符的拼音不一致")
        else:
            print("所有字符的拼音一致")
        
        return len(self.errors) == 0
    
    def generate_report(self):
        """生成验证报告"""
        print("\n" + "=" * 60)
        print("验证报告")
        print("=" * 60)
        
        print(f"\n错误数: {len(self.errors)}")
        print(f"警告数: {len(self.warnings)}")
        
        if self.errors:
            print("\n错误列表:")
            for i, error in enumerate(self.errors, 1):
                print(f"  {i}. {error}")
        
        if self.warnings:
            print("\n警告列表:")
            for i, warning in enumerate(self.warnings, 1):
                print(f"  {i}. {warning}")
        
        print("\n统计信息:")
        for key, value in self.stats.items():
            print(f"  {key}: {value}")
        
        # 总体评估
        print("\n" + "=" * 60)
        if len(self.errors) == 0:
            print("✅ 数据质量验证通过！")
        else:
            print("❌ 数据质量验证失败，请修复错误")
        
        if len(self.warnings) > 0:
            print(f"⚠️  发现 {len(self.warnings)} 个警告，建议检查")
        
        print("=" * 60)
        
        return len(self.errors) == 0

def main():
    print("开始数据质量验证...")
    print()
    
    validator = DataQualityValidator()
    
    # 执行验证
    validator.validate_master_db()
    validator.validate_chapter_data()
    validator.validate_example_words()
    validator.validate_consistency()
    
    # 生成报告
    success = validator.generate_report()
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
