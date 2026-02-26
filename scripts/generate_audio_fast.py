#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速音频文件生成脚本 - 使用并行处理加速生成
"""

import pandas as pd
import json
import subprocess
import os
from pathlib import Path
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing

class FastAudioGenerator:
    def __init__(self, max_workers=None):
        self.audio_dir = Path("audio")
        self.single_char_dir = self.audio_dir / "single_chars"
        self.multi_pronunciation_dir = self.audio_dir / "multi_pronunciation"
        self.index_file = self.audio_dir / "index.json"
        
        # 根据CPU核心数设置并发数，默认使用CPU核心数的75%
        if max_workers is None:
            cpu_count = multiprocessing.cpu_count()
            self.max_workers = max(1, int(cpu_count * 0.75))
        else:
            self.max_workers = max_workers
            
        print(f"🚀 使用 {self.max_workers} 个并发进程")
        
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
        print(f"✅ 总计: {len(single_chars) + len(multi_chars)} 个")
        
        return single_chars, multi_chars
    
    @staticmethod
    def generate_audio_file_task(char_data, output_dir, voice="Ting-Ting"):
        """单个音频文件生成任务（静态方法，用于多进程）"""
        try:
            char = char_data['char']
            jyutping = char_data['jyutping']
            
            # 文件名使用汉字
            filename = f"{char}.mp3"
            output_path = Path(output_dir) / filename
            
            # 检查是否已存在
            if output_path.exists():
                return {
                    'success': True,
                    'char': char,
                    'jyutping': jyutping,
                    'audio_path': f"audio/single_chars/{filename}",
                    'type': 'single',
                    'skipped': True
                }
            
            # 直接生成AIFF文件
            temp_aiff = output_path.with_suffix('.aiff')
            
            # 生成AIFF文件
            cmd = [
                'say',
                '-v', voice,
                '-o', str(temp_aiff),
                f"{char} {jyutping}"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                return {
                    'success': False,
                    'char': char,
                    'jyutping': jyutping,
                    'error': result.stderr
                }
            
            # 重命名aiff为mp3
            if temp_aiff.exists():
                temp_aiff.rename(output_path)
            
            return {
                'success': True,
                'char': char,
                'jyutping': jyutping,
                'audio_path': f"audio/single_chars/{filename}",
                'type': 'single',
                'skipped': False
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'char': char,
                'jyutping': jyutping,
                'error': 'Timeout'
            }
        except Exception as e:
            return {
                'success': False,
                'char': char,
                'jyutping': jyutping,
                'error': str(e)
            }
    
    def generate_single_char_audio(self, single_chars):
        """并行生成单音字音频文件"""
        print(f"\n开始并行生成单音字音频文件...")
        print(f"总计: {len(single_chars)} 个")
        print(f"并发数: {self.max_workers}")
        
        index_data = []
        success_count = 0
        skipped_count = 0
        failed_chars = []
        
        # 使用进程池并行生成
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交所有任务
            future_to_char = {
                executor.submit(
                    self.generate_audio_file_task, 
                    char_data, 
                    str(self.single_char_dir)
                ): char_data for char_data in single_chars
            }
            
            # 处理完成的任务
            completed = 0
            for future in as_completed(future_to_char):
                completed += 1
                result = future.result()
                
                if result['success']:
                    if result.get('skipped'):
                        skipped_count += 1
                        print(f"⏭️  [{completed}/{len(single_chars)}] 跳过已存在: {result['char']}")
                    else:
                        success_count += 1
                        print(f"✅ [{completed}/{len(single_chars)}] 生成成功: {result['char']} ({result['jyutping']})")
                    index_data.append({
                        'char': result['char'],
                        'jyutping': result['jyutping'],
                        'audio_path': result['audio_path'],
                        'type': result['type']
                    })
                else:
                    print(f"❌ [{completed}/{len(single_chars)}] 生成失败: {result['char']} ({result['jyutping']})")
                    print(f"   错误: {result.get('error', 'Unknown')}")
                    failed_chars.append(result['char'])
        
        print(f"\n✅ 单音字音频生成完成:")
        print(f"   成功: {success_count} 个")
        print(f"   跳过: {skipped_count} 个")
        print(f"   失败: {len(failed_chars)} 个")
        
        return index_data, failed_chars
    
    @staticmethod
    def generate_multi_audio_task(char_data, output_dir, voice="Ting-Ting"):
        """单个多音字音频文件生成任务（静态方法，用于多进程）"""
        try:
            char = char_data['char']
            jyutping = char_data['jyutping']
            
            # 文件名使用汉字_拼音
            filename = f"{char}_{jyutping}.mp3"
            output_path = Path(output_dir) / filename
            
            # 检查是否已存在
            if output_path.exists():
                return {
                    'success': True,
                    'char': char,
                    'jyutping': jyutping,
                    'audio_path': f"audio/multi_pronunciation/{filename}",
                    'type': 'multi',
                    'skipped': True
                }
            
            # 直接生成AIFF文件
            temp_aiff = output_path.with_suffix('.aiff')
            
            # 生成AIFF文件
            cmd = [
                'say',
                '-v', voice,
                '-o', str(temp_aiff),
                f"{char} {jyutping}"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                return {
                    'success': False,
                    'char': char,
                    'jyutping': jyutping,
                    'error': result.stderr
                }
            
            # 重命名aiff为mp3
            if temp_aiff.exists():
                temp_aiff.rename(output_path)
            
            return {
                'success': True,
                'char': char,
                'jyutping': jyutping,
                'audio_path': f"audio/multi_pronunciation/{filename}",
                'type': 'multi',
                'skipped': False
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'char': char,
                'jyutping': jyutping,
                'error': 'Timeout'
            }
        except Exception as e:
            return {
                'success': False,
                'char': char,
                'jyutping': jyutping,
                'error': str(e)
            }
    
    def generate_multi_char_audio(self, multi_chars):
        """并行生成多音字音频文件"""
        print(f"\n开始并行生成多音字音频文件...")
        print(f"总计: {len(multi_chars)} 个")
        print(f"并发数: {self.max_workers}")
        
        index_data = []
        success_count = 0
        skipped_count = 0
        failed_items = []
        
        # 使用进程池并行生成
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交所有任务
            future_to_char = {
                executor.submit(
                    self.generate_multi_audio_task, 
                    char_data, 
                    str(self.multi_pronunciation_dir)
                ): char_data for char_data in multi_chars
            }
            
            # 处理完成的任务
            completed = 0
            for future in as_completed(future_to_char):
                completed += 1
                result = future.result()
                
                if result['success']:
                    if result.get('skipped'):
                        skipped_count += 1
                        print(f"⏭️  [{completed}/{len(multi_chars)}] 跳过已存在: {result['char']} ({result['jyutping']})")
                    else:
                        success_count += 1
                        print(f"✅ [{completed}/{len(multi_chars)}] 生成成功: {result['char']} ({result['jyutping']})")
                    index_data.append({
                        'char': result['char'],
                        'jyutping': result['jyutping'],
                        'audio_path': result['audio_path'],
                        'type': result['type']
                    })
                else:
                    print(f"❌ [{completed}/{len(multi_chars)}] 生成失败: {result['char']} ({result['jyutping']})")
                    print(f"   错误: {result.get('error', 'Unknown')}")
                    failed_items.append(f"{result['char']}_{result['jyutping']}")
        
        print(f"\n✅ 多音字音频生成完成:")
        print(f"   成功: {success_count} 个")
        print(f"   跳过: {skipped_count} 个")
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
        print("开始快速生成粤语发音音频文件（并行处理）")
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
        print(f"\n下一步:")
        print("1. 打开 test_audio.html 测试音频播放效果")
        print("2. 如果效果满意，更新项目中的发音脚本引用")

def main():
    import time
    start_time = time.time()
    
    # 创建生成器（自动根据CPU核心数设置并发数）
    generator = FastAudioGenerator()
    
    # 生成所有音频
    generator.generate_all_audio()
    
    # 计算耗时
    elapsed_time = time.time() - start_time
    hours = int(elapsed_time // 3600)
    minutes = int((elapsed_time % 3600) // 60)
    seconds = int(elapsed_time % 60)
    
    print(f"\n⏱️  总耗时: {hours}小时{minutes}分{seconds}秒")

if __name__ == "__main__":
    main()
