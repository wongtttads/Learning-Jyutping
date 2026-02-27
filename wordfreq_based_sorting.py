#!/usr/bin/env python3
"""
基于 wordfreq 库的汉字字频排序系统
使用 wordfreq 库获取真实的汉字使用频率
"""

import json
import os
import shutil
import wordfreq
from collections import defaultdict

class WordFreqSorter:
    def __init__(self):
        print("初始化 wordfreq 排序系统...")
        
    def get_character_frequency(self, char):
        """使用 wordfreq 库获取汉字频率"""
        try:
            # 获取汉字的频率，返回值是浮点数（例如 0.045）
            freq = wordfreq.word_frequency(char, 'zh')
            return freq
        except Exception as e:
            print(f"获取 '{char}' 的频率时出错: {e}")
            return 0.0
    
    def sort_characters(self):
        """按 wordfreq 频率排序所有汉字"""
        print("开始按 wordfreq 频率排序汉字...")
        
        # 备份原始数据
        backup_dir = "data/backup_before_wordfreq_sorting"
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            print(f"创建备份目录: {backup_dir}")
        
        for chapter in range(1, 11):
            src_file = f"data/chapter_{chapter}_characters.json"
            dst_file = f"{backup_dir}/chapter_{chapter}_characters.json.backup"
            if os.path.exists(src_file):
                shutil.copy2(src_file, dst_file)
                print(f"  备份: {src_file} -> {dst_file}")
        
        # 收集所有汉字
        all_characters = []
        for chapter in range(1, 11):
            try:
                with open(f'data/chapter_{chapter}_characters.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    all_characters.extend(data)
                    print(f"  第{chapter}章: 加载了{len(data)}个汉字")
            except Exception as e:
                print(f"  第{chapter}章加载失败: {e}")
        
        print(f"总共收集到 {len(all_characters)} 个汉字")
        
        # 计算每个汉字的频率
        print("计算汉字频率...")
        frequency_characters = []
        for char_data in all_characters:
            char = char_data['char']
            freq = self.get_character_frequency(char)
            frequency_characters.append({
                'char_data': char_data,
                'frequency': freq
            })
        
        # 按频率排序（频率越高越常用）
        print("按频率排序...")
        frequency_characters.sort(key=lambda x: x['frequency'], reverse=True)
        
        # 生成排名
        print("生成最终排名...")
        ranked_characters = []
        for i, item in enumerate(frequency_characters, 1):
            char_data = item['char_data'].copy()
            char_data['frequency_rank'] = i  # 更新频率排名
            char_data['wordfreq_score'] = item['frequency']  # 保存 wordfreq 分数
            ranked_characters.append(char_data)
        
        # 按章节重新分组
        print("按章节重新分组...")
        total_chars = len(ranked_characters)
        chars_per_chapter = total_chars // 10
        remainder = total_chars % 10
        
        start_index = 0
        for chapter in range(1, 11):
            # 计算本章汉字数量
            chapter_count = chars_per_chapter
            if chapter <= remainder:
                chapter_count += 1
            
            # 获取本章汉字
            end_index = start_index + chapter_count
            chapter_chars = ranked_characters[start_index:end_index]
            
            # 保存到文件
            output_file = f'data/chapter_{chapter}_characters.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(chapter_chars, f, ensure_ascii=False, indent=2)
            
            print(f"  第{chapter}章: {len(chapter_chars)}个汉字")
            print(f"    第一个字: {chapter_chars[0]['char']} (排名: {chapter_chars[0]['frequency_rank']}, 频率: {chapter_chars[0]['wordfreq_score']:.6f})")
            print(f"    最后一个字: {chapter_chars[-1]['char']} (排名: {chapter_chars[-1]['frequency_rank']}, 频率: {chapter_chars[-1]['wordfreq_score']:.6f})")
            
            # 更新起始索引
            start_index = end_index
        
        # 生成统计报告
        self.generate_statistics_report(ranked_characters)
        
        print("\n" + "=" * 60)
        print("wordfreq 字频排序完成！")
        print("=" * 60)
        print("重要提示:")
        print("1. 原始数据已备份到 data/backup_before_wordfreq_sorting/")
        print("2. 新的字频排名已应用到所有章节数据")
        print("3. 现在汉字将按真实使用频率排序（最常用字在前）")
        print("4. 排序规则: wordfreq 库提供的真实语料库频率")
        print("=" * 60)
    
    def generate_statistics_report(self, ranked_characters):
        """生成统计报告"""
        report = {
            "total_characters": len(ranked_characters),
            "top_100_chars": [],
            "bottom_100_chars": [],
            "chapters_summary": {},
            "frequency_distribution": {}
        }
        
        # 前100个最常用字
        report["top_100_chars"] = [
            {
                "char": c['char'],
                "jyutping": c.get('jyutping', ''),
                "frequency_rank": c['frequency_rank'],
                "wordfreq_score": c.get('wordfreq_score', 0.0)
            }
            for c in ranked_characters[:100]
        ]
        
        # 后100个最不常用字
        report["bottom_100_chars"] = [
            {
                "char": c['char'],
                "jyutping": c.get('jyutping', ''),
                "frequency_rank": c['frequency_rank'],
                "wordfreq_score": c.get('wordfreq_score', 0.0)
            }
            for c in ranked_characters[-100:]
        ]
        
        # 章节统计
        total_chars = len(ranked_characters)
        chars_per_chapter = total_chars // 10
        remainder = total_chars % 10
        
        start_index = 0
        for chapter in range(1, 11):
            chapter_count = chars_per_chapter
            if chapter <= remainder:
                chapter_count += 1
            
            end_index = start_index + chapter_count
            chapter_chars = ranked_characters[start_index:end_index]
            
            report["chapters_summary"][f"chapter_{chapter}"] = {
                "character_count": len(chapter_chars),
                "first_char": chapter_chars[0]['char'],
                "first_char_rank": chapter_chars[0]['frequency_rank'],
                "first_char_score": chapter_chars[0]['wordfreq_score'],
                "last_char": chapter_chars[-1]['char'],
                "last_char_rank": chapter_chars[-1]['frequency_rank'],
                "last_char_score": chapter_chars[-1]['wordfreq_score']
            }
            
            start_index = end_index
        
        # 频率分布统计
        freq_ranges = {
            "very_high": 0,  # 频率 > 0.001
            "high": 0,       # 0.0001-0.001
            "medium": 0,     # 0.00001-0.0001
            "low": 0,        # 0.000001-0.00001
            "very_low": 0    # < 0.000001
        }
        
        for char_data in ranked_characters:
            freq = char_data.get('wordfreq_score', 0.0)
            
            if freq > 0.001:
                freq_ranges["very_high"] += 1
            elif freq > 0.0001:
                freq_ranges["high"] += 1
            elif freq > 0.00001:
                freq_ranges["medium"] += 1
            elif freq > 0.000001:
                freq_ranges["low"] += 1
            else:
                freq_ranges["very_low"] += 1
        
        report["frequency_distribution"] = freq_ranges
        
        # 保存报告
        with open('data/wordfreq_sorting_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n统计报告已保存: data/wordfreq_sorting_report.json")
        
        # 打印简要报告
        print("\n=== wordfreq 字频排序统计报告 ===")
        print(f"总汉字数: {report['total_characters']}")
        
        print("\n频率分布:")
        print(f"  非常高频率 (>0.001): {freq_ranges['very_high']} 字")
        print(f"  高频率 (0.0001-0.001): {freq_ranges['high']} 字")
        print(f"  中频率 (0.00001-0.0001): {freq_ranges['medium']} 字")
        print(f"  低频率 (0.000001-0.00001): {freq_ranges['low']} 字")
        print(f"  非常低频率 (<0.000001): {freq_ranges['very_low']} 字")
        
        print("\n前20个最常用汉字:")
        for i, char_info in enumerate(report['top_100_chars'][:20], 1):
            print(f"  {i:2d}. {char_info['char']} ({char_info['jyutping']}) - 排名: {char_info['frequency_rank']:4d}, 频率: {char_info['wordfreq_score']:.6f}")
        
        print("\n最后20个汉字:")
        for i, char_info in enumerate(report['bottom_100_chars'][-20:], 1):
            idx = report['total_characters'] - 20 + i
            print(f"  {idx:4d}. {char_info['char']} ({char_info['jyutping']}) - 排名: {char_info['frequency_rank']:4d}, 频率: {char_info['wordfreq_score']:.6f}")

def main():
    print("=" * 60)
    print("wordfreq 字频排序系统")
    print("基于 wordfreq 库的真实语料库频率数据")
    print("=" * 60)
    
    sorter = WordFreqSorter()
    sorter.sort_characters()

if __name__ == "__main__":
    main()
