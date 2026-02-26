#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试音频生成脚本 - 生成少量测试音频文件
"""

import pandas as pd
import json
import subprocess
import os
from pathlib import Path

class TestAudioGenerator:
    def __init__(self, test_count=20):
        self.test_count = test_count
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
    
    def load_test_characters(self):
        """加载测试汉字数据"""
        print(f"正在加载前 {self.test_count} 个汉字...")
        
        df = pd.read_csv("data/processed/jyutping_master.csv")
        
        # 取前N个汉字
        test_df = df.head(self.test_count)
        
        test_chars = []
        for _, row in test_df.iterrows():
            test_chars.append({
                'char': row['char'],
                'jyutping': row['jyutping'],
                'tone': row['tone'],
                'frequency_rank': row['frequency_rank']
            })
        
        print(f"✅ 加载了 {len(test_chars)} 个测试汉字:")
        for char_data in test_chars[:10]:
            print(f"   {char_data['char']} ({char_data['jyutping']})")
        if len(test_chars) > 10:
            print(f"   ... 还有 {len(test_chars) - 10} 个")
        
        return test_chars
    
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
    
    def generate_test_audio(self, test_chars):
        """生成测试音频文件"""
        print(f"\n开始生成测试音频文件...")
        print(f"总计: {len(test_chars)} 个")
        
        index_data = []
        success_count = 0
        failed_chars = []
        
        for i, char_data in enumerate(test_chars, 1):
            char = char_data['char']
            jyutping = char_data['jyutping']
            
            # 文件名使用汉字
            filename = f"{char}.mp3"
            output_path = self.single_char_dir / filename
            
            # 检查是否已存在
            if output_path.exists():
                print(f"⏭️  [{i}/{len(test_chars)}] 跳过已存在: {char}")
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
                print(f"✅ [{i}/{len(test_chars)}] 生成成功: {char} ({jyutping})")
                index_data.append({
                    'char': char,
                    'jyutping': jyutping,
                    'audio_path': f"audio/single_chars/{filename}",
                    'type': 'single'
                })
                success_count += 1
            else:
                print(f"❌ [{i}/{len(test_chars)}] 生成失败: {char} ({jyutping})")
                failed_chars.append(char)
        
        print(f"\n✅ 测试音频生成完成:")
        print(f"   成功: {success_count} 个")
        print(f"   失败: {len(failed_chars)} 个")
        
        return index_data, failed_chars
    
    def generate_index_file(self, index_data):
        """生成音频索引文件"""
        print(f"\n生成音频索引文件...")
        
        index_json = {
            'version': '1.0',
            'total_count': len(index_data),
            'single_chars_count': len(index_data),
            'multi_chars_count': 0,
            'single_chars': index_data,
            'multi_chars': []
        }
        
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(index_json, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 索引文件已生成: {self.index_file}")
    
    def generate_all_test_audio(self):
        """生成所有测试音频文件"""
        print("=" * 60)
        print("开始生成测试粤语发音音频文件")
        print("=" * 60)
        
        # 加载测试数据
        test_chars = self.load_test_characters()
        
        # 生成测试音频
        index_data, failed_chars = self.generate_test_audio(test_chars)
        
        # 生成索引文件
        self.generate_index_file(index_data)
        
        # 总结
        print("\n" + "=" * 60)
        print("测试音频生成完成")
        print("=" * 60)
        print(f"总计: {len(index_data)} 个音频文件")
        print(f"成功: {len(index_data) - len(failed_chars)} 个")
        print(f"失败: {len(failed_chars)} 个")
        
        if failed_chars:
            print("\n失败的字符:")
            for char in failed_chars:
                print(f"  - {char}")
        
        print(f"\n音频文件位置: {self.audio_dir}")
        print(f"索引文件位置: {self.index_file}")
        print(f"\n下一步:")
        print("1. 打开 test_audio.html 测试音频播放效果")
        print("2. 如果效果满意，运行完整生成脚本:")
        print("   python scripts/generate_audio_files.py")

def main():
    generator = TestAudioGenerator(test_count=20)
    generator.generate_all_test_audio()

if __name__ == "__main__":
    main()
