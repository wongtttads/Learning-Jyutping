#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重新生成失败的音频文件
"""

import pandas as pd
import subprocess
from pathlib import Path

def regenerate_failed_chars():
    """重新生成失败的音频文件"""
    
    failed_chars = [
        '假', '衅', '囟', '汆', '刖', '夙', '旮', 
        '钽', '钼', '钿', '铀', '铂'
    ]
    
    print("=" * 60)
    print("重新生成失败的音频文件")
    print("=" * 60)
    print(f"需要重新生成的字符: {len(failed_chars)} 个\n")
    
    # 加载数据获取拼音
    df = pd.read_csv("data/processed/jyutping_master.csv")
    
    audio_dir = Path("audio/single_chars")
    success_count = 0
    still_failed = []
    
    for i, char in enumerate(failed_chars, 1):
        # 查找该字符的拼音
        char_data = df[df['char'] == char]
        
        if char_data.empty:
            print(f"⚠️  [{i}/{len(failed_chars)}] 未找到数据: {char}")
            still_failed.append(char)
            continue
        
        jyutping = char_data.iloc[0]['jyutping']
        filename = f"{char}.mp3"
        output_path = audio_dir / filename
        
        # 删除已存在的文件（如果有的话）
        if output_path.exists():
            output_path.unlink()
        
        # 生成音频
        try:
            temp_aiff = output_path.with_suffix('.aiff')
            
            cmd = [
                'say',
                '-v', 'Ting-Ting',
                '-o', str(temp_aiff),
                f"{char} {jyutping}"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                print(f"❌ [{i}/{len(failed_chars)}] 生成失败: {char} ({jyutping})")
                print(f"   错误: {result.stderr}")
                still_failed.append(char)
                continue
            
            # 重命名aiff为mp3
            if temp_aiff.exists():
                temp_aiff.rename(output_path)
                print(f"✅ [{i}/{len(failed_chars)}] 生成成功: {char} ({jyutping})")
                success_count += 1
            else:
                print(f"❌ [{i}/{len(failed_chars)}] 生成失败: {char} ({jyutping})")
                print(f"   原因: AIFF文件未生成")
                still_failed.append(char)
                
        except subprocess.TimeoutExpired:
            print(f"❌ [{i}/{len(failed_chars)}] 生成超时: {char} ({jyutping})")
            still_failed.append(char)
        except Exception as e:
            print(f"❌ [{i}/{len(failed_chars)}] 生成异常: {char} ({jyutping})")
            print(f"   异常: {e}")
            still_failed.append(char)
    
    print("\n" + "=" * 60)
    print("重新生成完成")
    print("=" * 60)
    print(f"成功: {success_count} 个")
    print(f"仍然失败: {len(still_failed)} 个")
    
    if still_failed:
        print("\n仍然失败的字符:")
        for char in still_failed:
            print(f"  - {char}")

if __name__ == "__main__":
    regenerate_failed_chars()
