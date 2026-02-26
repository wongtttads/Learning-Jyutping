#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新HTML文件 - 使用预录制音频发音功能
"""

import re
from pathlib import Path

def update_html_file(html_file):
    """更新单个HTML文件"""
    print(f"正在更新: {html_file.name}")
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经有pronunciation_audio.js引用
    if 'pronunciation_audio.js' in content:
        print(f"  ⏭️  已更新，跳过")
        return False
    
    # 替换发音脚本引用
    content = re.sub(
        r'<script src="scripts/pronunciation\.js"></script>',
        '<script src="scripts/pronunciation_audio.js"></script>',
        content
    )
    
    # 移除localhost:5001的API调用（如果有）
    content = re.sub(
        r"const response = await fetch\('http://localhost:5001/api/speak',.*?\}\);",
        '',
        content,
        flags=re.DOTALL
    )
    
    # 移除stop API调用（如果有）
    content = re.sub(
        r"fetch\('http://localhost:5001/api/stop',.*?\}\.catch\(console\.error\);",
        '',
        content,
        flags=re.DOTALL
    )
    
    # 保存更新后的内容
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✅ 更新完成")
    return True

def main():
    """更新所有HTML文件"""
    print("=" * 60)
    print("更新HTML文件 - 使用预录制音频发音功能")
    print("=" * 60)
    
    # 查找所有HTML文件
    output_dir = Path("output")
    html_files = list(output_dir.glob("*.html"))
    
    print(f"找到 {len(html_files)} 个HTML文件\n")
    
    updated_count = 0
    skipped_count = 0
    
    for html_file in html_files:
        if update_html_file(html_file):
            updated_count += 1
        else:
            skipped_count += 1
    
    print("\n" + "=" * 60)
    print("更新完成")
    print("=" * 60)
    print(f"更新: {updated_count} 个")
    print(f"跳过: {skipped_count} 个")
    print(f"\n下一步:")
    print("1. 测试发音功能")
    print("2. 更新部署配置")

if __name__ == "__main__":
    main()
