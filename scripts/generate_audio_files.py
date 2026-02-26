#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音频文件生成脚本 - 为每个汉字生成粤语发音音频文件
"""

import pandas as pd
import json
import subprocess
import os
from pathlib import Path
from collections import defaultdict

class AudioGenerator:
    def __init__(self):
        self.audio_dir = Path("audio")
        self.single_char_dir = self.audio_dir / "single_chars"
        self.multi_pronunciation_dir = self.audio_dir / "multi_pronunciation"
        self.index_file = self.audio_dir / "index.json"
        
        self.create_directories()
        
    def create_directories(self):
        """创建音频文件目录"""
        self.audio_dir.mkdir(exist_ok=True)
        self.single_char_dir.mkdir(exist_ok=True)
        self.multi_pronunciation_dir.mkdir(exist_ok=True)
        print(f"✅ 音频目录已创建: {self.audio_dir}")
    
    def load_character_data(self):
        """加载汉字数据"""
        print("正在加载汉字数据...")
        
        df = pd.read_csv("data/processed/jyutping_master.csv")
        
        # 按字符分组，识别多音字
        char_groups = defaultdict(list)
        for _, row in df.iterrows():
            char_groups[row['char']].append({
                'jyutping': row['jyutping'],
                'tone': row['tone'],
                'frequency_rank': row['frequency_rank']
            })
        
        # 识别多音字
        single_chars = []
        multi_chars = []
        
        for char, pronunciations in char_groups.items():
            if len(pronunciations) == 1:
                single_chars.append({
                    'char': char,
                    'jyutping': pronunciations[0]['jyutping'],
                    'tone': pronunciations[0]['tone'],
                    'frequency_rank': pronunciations[0]['frequency_rank']
                })
            else:
                for pron in pronunciations:
                    multi_chars.append({
                        'char': char,
                        'jyutping': pron['jyutping'],
                        'tone': pron['tone'],
                        'frequency_rank': pron['frequency_rank']
                    })
        
        print(f"✅ 单音字: {len(single_chars)} 个")
        print(f"✅ 多音字: {len(multi_chars)} 个")
        
        return single_chars, multi_chars
    
    def generate_audio_file(self, text, output_path, voice="Ting-Ting"):
        """使用macOS的say命令生成音频文件"""
        try:
            # 直接生成AIFF文件（现代浏览器都支持）
            temp_aiff = output_path.with_suffix('.aiff')
            
            # 生成AIFF文件
            cmd = [
                'say',
                '-v', voice,
                '-o', str(temp_aiff),
                text
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                print(f"❌ 生成音频失败: {text}")
                print(f"   错误: {result.stderr}")
                return False
            
            # 直接重命名aiff为mp3（虽然格式是AIFF，但为了兼容性使用.mp3扩展名）
            if temp_aiff.exists():
                temp_aiff.rename(output_path)
            
            return True
            
        except subprocess.TimeoutExpired:
            print(f"❌ 生成音频超时: {text}")
            return False
        except Exception as e:
            print(f"❌ 生成音频异常: {text}")
            print(f"   异常: {e}")
            return False
    
    def generate_single_char_audio(self, single_chars, batch_size=100):
        """生成单音字音频文件"""
        print(f"\n开始生成单音字音频文件...")
        print(f"总计: {len(single_chars)} 个")
        
        index_data = []
        success_count = 0
        failed_chars = []
        
        for i, char_data in enumerate(single_chars, 1):
            char = char_data['char']
            jyutping = char_data['jyutping']
            
            # 文件名使用汉字
            filename = f"{char}.mp3"
            output_path = self.single_char_dir / filename
            
            # 检查是否已存在
            if output_path.exists():
                print(f"⏭️  [{i}/{len(single_chars)}] 跳过已存在: {char}")
                index_data.append({
                    'char': char,
                    'jyutping': jyutping,
                    'audio_path': f"audio/single_chars/{filename}",
                    'type': 'single'
                })
                success_count += 1
                continue
            
            # 生成音频
            text = f"{char} {jyutping}"
            if self.generate_audio_file(text, output_path):
                print(f"✅ [{i}/{len(single_chars)}] 生成成功: {char} ({jyutping})")
                index_data.append({
                    'char': char,
                    'jyutping': jyutping,
                    'audio_path': f"audio/single_chars/{filename}",
                    'type': 'single'
                })
                success_count += 1
            else:
                print(f"❌ [{i}/{len(single_chars)}] 生成失败: {char} ({jyutping})")
                failed_chars.append(char)
        
        print(f"\n✅ 单音字音频生成完成:")
        print(f"   成功: {success_count} 个")
        print(f"   失败: {len(failed_chars)} 个")
        
        return index_data, failed_chars
    
    def generate_multi_char_audio(self, multi_chars):
        """生成多音字音频文件"""
        print(f"\n开始生成多音字音频文件...")
        print(f"总计: {len(multi_chars)} 个")
        
        index_data = []
        success_count = 0
        failed_items = []
        
        for i, char_data in enumerate(multi_chars, 1):
            char = char_data['char']
            jyutping = char_data['jyutping']
            
            # 文件名使用汉字_拼音
            filename = f"{char}_{jyutping}.mp3"
            output_path = self.multi_pronunciation_dir / filename
            
            # 检查是否已存在
            if output_path.exists():
                print(f"⏭️  [{i}/{len(multi_chars)}] 跳过已存在: {char} ({jyutping})")
                index_data.append({
                    'char': char,
                    'jyutping': jyutping,
                    'audio_path': f"audio/multi_pronunciation/{filename}",
                    'type': 'multi'
                })
                success_count += 1
                continue
            
            # 生成音频
            text = f"{char} {jyutping}"
            if self.generate_audio_file(text, output_path):
                print(f"✅ [{i}/{len(multi_chars)}] 生成成功: {char} ({jyutping})")
                index_data.append({
                    'char': char,
                    'jyutping': jyutping,
                    'audio_path': f"audio/multi_pronunciation/{filename}",
                    'type': 'multi'
                })
                success_count += 1
            else:
                print(f"❌ [{i}/{len(multi_chars)}] 生成失败: {char} ({jyutping})")
                failed_items.append(f"{char}_{jyutping}")
        
        print(f"\n✅ 多音字音频生成完成:")
        print(f"   成功: {success_count} 个")
        print(f"   失败: {len(failed_items)} 个")
        
        return index_data, failed_items
    
    def generate_index_file(self, single_index, multi_index):
        """生成音频索引文件"""
        print(f"\n生成音频索引文件...")
        
        index_data = {
            'version': '1.0',
            'total_count': len(single_index) + len(multi_index),
            'single_chars_count': len(single_index),
            'multi_chars_count': len(multi_index),
            'single_chars': single_index,
            'multi_chars': multi_index
        }
        
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 索引文件已生成: {self.index_file}")
    
    def generate_all_audio(self):
        """生成所有音频文件"""
        print("=" * 60)
        print("开始生成粤语发音音频文件")
        print("=" * 60)
        
        # 加载数据
        single_chars, multi_chars = self.load_character_data()
        
        # 生成单音字音频
        single_index, failed_single = self.generate_single_char_audio(single_chars)
        
        # 生成多音字音频
        multi_index, failed_multi = self.generate_multi_char_audio(multi_chars)
        
        # 生成索引文件
        self.generate_index_file(single_index, multi_index)
        
        # 总结
        print("\n" + "=" * 60)
        print("音频生成完成")
        print("=" * 60)
        print(f"总计: {len(single_index) + len(multi_index)} 个音频文件")
        print(f"成功: {len(single_index) + len(multi_index) - len(failed_single) - len(failed_multi)} 个")
        print(f"失败: {len(failed_single) + len(failed_multi)} 个")
        
        if failed_single or failed_multi:
            print("\n失败的字符:")
            for char in failed_single:
                print(f"  - {char}")
            for item in failed_multi:
                print(f"  - {item}")
        
        print(f"\n音频文件位置: {self.audio_dir}")
        print(f"索引文件位置: {self.index_file}")

def main():
    generator = AudioGenerator()
    generator.generate_all_audio()

if __name__ == "__main__":
    main()
