#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成所有字符的粤语例词 - 改进版本
使用高频字组合和基于规则的例词生成
"""

import pandas as pd
import json
import random
from pathlib import Path
import re

# 路径设置
project_root = Path(__file__).parent.parent
data_dir = project_root / "data" / "processed"
output_dir = project_root / "output" / "data"

# 预定义的高质量例词映射（针对前100个高频字）
HIGH_QUALITY_EXAMPLES = {
    '一': ['一个', '一心'],
    '乙': ['乙级', '甲乙'],
    '二': ['二月', '第二'],
    '十': ['十分', '第十'],
    '丁': ['丁香', '人丁'],
    '厂': ['工厂', '厂长'],
    '七': ['七月', '十七'],
    '卜': ['卜卦', '萝卜'],
    '八': ['八月', '十八'],
    '人': ['人民', '个人'],
    '入': ['入口', '进入'],
    '儿': ['儿子', '儿童'],
    '匕': ['匕首', '匕箸'],
    '几': ['几个', '几乎'],
    '九': ['九月', '十九'],
    '刁': ['刁难', '刁钻'],
    '了': ['了解', '完了'],
    '刀': ['刀子', '刀具'],
    '力': ['力量', '能力'],
    '乃': ['乃至', '乃是'],
    '又': ['又来', '又是'],
    '三': ['三月', '第三'],
    '干': ['干净', '干活'],
    '于': ['于是', '属于'],
    '亏': ['亏本', '吃亏'],
    '工': ['工作', '工人'],
    '土': ['土地', '泥土'],
    '士': ['士兵', '博士'],
    '才': ['才能', '人才'],
    '下': ['下面', '下班'],
    '寸': ['尺寸', '寸金'],
    '大': ['大家', '大学'],
    '丈': ['丈夫', '丈量'],
    '与': ['与其', '参与'],
    '万': ['万一', '千万'],
    '上': ['上面', '上班'],
    '小': ['小学', '小心'],
    '口': ['门口', '口语'],
    '山': ['山水', '爬山'],
    '巾': ['毛巾', '纸巾'],
    '千': ['千万', '千米'],
    '乞': ['乞讨', '乞丐'],
    '川': ['四川', '川菜'],
    '亿': ['亿万', '亿元'],
    '个': ['个人', '个数'],
    '夕': ['除夕', '夕阳'],
    '久': ['很久', '持久'],
    '么': ['什么', '怎么'],
    '勺': ['勺子', '汤勺'],
    '凡': ['凡是', '平凡'],
    # 可以继续添加更多
}

# 常见且组合能力强的字（用于生成组合）
COMMON_CHARS = ['的', '是', '在', '有', '和', '大', '小', '中', '新', '老', '好', '坏', '高', '低', 
                '长', '短', '多', '少', '快', '慢', '重', '轻', '红', '白', '黑', '子', '头', '人', 
                '家', '工', '手', '口', '心', '力', '气', '水', '火', '山', '石', '金', '木', '土',
                '日', '月', '年', '天', '地', '风', '雨', '云', '电', '花', '草', '树', '鸟', '鱼']

# 基于部首的例词模板
RADICAL_TEMPLATES = {
    '口': ['门口', '口语'],  # 口字旁
    '山': ['山水', '爬山'],  # 山字旁
    '水': ['水果', '水杯'],  # 水字旁
    '人': ['人民', '个人'],  # 人字旁
    '手': ['手机', '手表'],  # 提手旁
    '心': ['心情', '心理'],  # 心字底
    '木': ['木材', '树木'],  # 木字旁
    '火': ['火车', '火锅'],  # 火字旁
    '金': ['金钱', '金属'],  # 金字旁
    '土': ['土地', '泥土'],  # 土字旁
    '日': ['日期', '日记'],  # 日字旁
    '月': ['月亮', '月饼'],  # 月字旁
    '女': ['女孩', '女性'],  # 女字旁
    '子': ['子女', '孩子'],  # 子字旁
    '言': ['言论', '语言'],  # 言字旁
    '走': ['走路', '走廊'],  # 走字旁
    '车': ['汽车', '车站'],  # 车字旁
}

def load_characters():
    """加载所有字符数据"""
    csv_path = data_dir / "jyutping_master.csv"
    df = pd.read_csv(csv_path)
    print(f"加载了 {len(df)} 个字符")
    return df

def get_radical_category(char):
    """根据字符的部首或结构返回类别（简化版）"""
    # 这里可以根据需要扩展更精确的部首识别
    # 目前使用简单的规则
    radical_map = {
        '口': '口',
        '山': '山', 
        '水': '水',
        '氵': '水',
        '人': '人',
        '亻': '人',
        '手': '手',
        '扌': '手',
        '心': '心',
        '忄': '心',
        '木': '木',
        '火': '火',
        '灬': '火',
        '金': '金',
        '钅': '金',
        '土': '土',
        '日': '日',
        '月': '月',
        '女': '女',
        '子': '子',
        '言': '言',
        '讠': '言',
        '走': '走',
        '车': '车',
    }
    
    # 简化的部首识别（实际应用中应该使用专门的库）
    # 这里我们只检查字符是否包含某些部首
    for radical, category in radical_map.items():
        if radical in char:
            return category
    
    return None

def generate_example_words_v2(char, freq_rank, all_chars):
    """为单个字符生成两个例词 - 改进版本"""
    
    # 策略1：使用预定义的高质量例词
    if char in HIGH_QUALITY_EXAMPLES:
        return HIGH_QUALITY_EXAMPLES[char]
    
    # 策略2：根据频率等级使用不同策略
    examples = []
    
    # 高频字（前500）
    if freq_rank <= 500:
        # 使用常见字组合
        for common_char in COMMON_CHARS:
            if common_char != char:
                # 尝试两种顺序
                if random.random() > 0.5:
                    candidate = char + common_char
                else:
                    candidate = common_char + char
                
                # 简单的合理性检查：避免重复字符
                if candidate[0] != candidate[1]:
                    examples.append(candidate)
                    if len(examples) >= 2:
                        break
        
        # 如果还不够，使用基于部首的模板
        if len(examples) < 2:
            radical = get_radical_category(char)
            if radical and radical in RADICAL_TEMPLATES:
                # 使用相同部首的模板词，但替换成目标字符
                template_words = RADICAL_TEMPLATES[radical]
                for word in template_words:
                    if char in word:
                        examples.append(word)
                    else:
                        # 替换模板词中的部首字为目标字符
                        new_word = word.replace(radical, char) if radical in word else char + word[-1]
                        examples.append(new_word)
                    if len(examples) >= 2:
                        break
    
    # 中频字（501-2000）
    elif freq_rank <= 2000:
        # 随机组合但避免奇怪的字
        safe_chars = [c for c in COMMON_CHARS if c != char]
        if safe_chars:
            for _ in range(10):
                if len(examples) >= 2:
                    break
                other_char = random.choice(safe_chars)
                if random.random() > 0.5:
                    candidate = char + other_char
                else:
                    candidate = other_char + char
                if candidate not in examples:
                    examples.append(candidate)
    
    # 低频字（2001+）
    else:
        # 使用简单组合
        simple_chars = ['的', '是', '在', '有', '和']
        for other_char in simple_chars:
            if other_char != char:
                examples.append(char + other_char)
                if len(examples) >= 2:
                    break
    
    # 回退机制
    if len(examples) < 2:
        examples.append(f"{char}字")
        if len(examples) < 2:
            examples.append(f"{char}词")
    
    return examples[:2]

def main():
    """主函数"""
    print("开始生成粤语例词（改进版本）...")
    
    # 加载数据
    char_df = load_characters()
    
    # 获取所有字符列表（用于随机选择）
    all_chars = char_df['char'].tolist()
    
    # 生成例词映射
    example_map = {}
    
    for idx, row in char_df.iterrows():
        char = row['char']
        freq_rank = row['frequency_rank']
        
        # 跳过非汉字或空字符
        if not char or len(char) != 1:
            continue
        
        # 生成例词
        examples = generate_example_words_v2(char, freq_rank, all_chars)
        example_map[char] = examples
        
        # 进度显示
        if (idx + 1) % 500 == 0:
            print(f"已处理 {idx + 1} 个字符")
    
    print(f"生成了 {len(example_map)} 个字符的例词")
    
    # 保存为JSON
    output_path = output_dir / "example_words_v2.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(example_map, f, ensure_ascii=False, indent=2)
    
    print(f"例词映射已保存到: {output_path}")
    
    # 生成JavaScript版本
    js_output_path = output_dir / "example_words.js"
    with open(js_output_path, 'w', encoding='utf-8') as f:
        f.write("// 自动生成的粤语例词映射\n")
        f.write("const exampleWordsMap = ")
        json.dump(example_map, f, ensure_ascii=False, indent=2)
        f.write(";\n")
    
    print(f"JavaScript版本已保存到: {js_output_path}")
    
    # 打印一些示例
    print("\n示例字符的例词:")
    sample_chars = ['口', '山', '水', '人', '天', '地', '日', '月', '风', '雨', '火', '木', '金', '土']
    for sample in sample_chars:
        if sample in example_map:
            print(f"  {sample}: {example_map[sample]}")

if __name__ == "__main__":
    main()