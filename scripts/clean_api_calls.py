#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理HTML文件中的API调用代码
"""

import re
from pathlib import Path

def clean_api_calls(html_file):
    """清理HTML文件中的API调用代码"""
    print(f"正在清理: {html_file.name}")
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否还有API调用
    if 'localhost:5001' in content:
        print(f"  ⚠️  发现API调用代码，需要清理")
    else:
        print(f"  ✅ 没有API调用代码")
        return False
    
    # 移除API调用相关的代码块
    # 移除fetch调用
    content = re.sub(
        r'\s+try\s+{\s+const response = await fetch\(\'http://localhost:5001/api/speak\',.*?\}\s+catch\s*\(error\)\s*{\s+console\.error\(\'发音错误:\', error\)\;\s+}\s*',
        '',
        content,
        flags=re.DOTALL
    )
    
    # 移除stop API调用
    content = re.sub(
        r'\s+//\s+停止服务器端的朗读\s+fetch\(\'http://localhost:5001/api/stop\',\s+\{\s+method:\s+\'POST\'\s+\}\s+\)\.catch\(console\.error\);',
        '',
        content,
        flags=re.DOTALL
    )
    
    # 移除空的try-catch块（如果有）
    content = re.sub(
        r'\s+try\s+{\s+\}\s+catch\s*\(error\)\s*{\s+console\.error\(\'发音错误:\', error\)\;\s+}\s*',
        '',
        content,
        flags=re.DOTALL
    )
    
    # 保存清理后的内容
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✅ 清理完成")
    return True

def main():
    """清理所有HTML文件"""
    print("=" * 60)
    print("清理HTML文件 - 移除API调用代码")
    print("=" * 60)
    
    # 查找所有HTML文件
    output_dir = Path("output")
    html_files = list(output_dir.glob("*.html"))
    
    print(f"找到 {len(html_files)} 个HTML文件\n")
    
    cleaned_count = 0
    skipped_count = 0
    
    for html_file in html_files:
        if clean_api_calls(html_file):
            cleaned_count += 1
        else:
            skipped_count += 1
    
    print("\n" + "=" * 60)
    print("清理完成")
    print("=" * 60)
    print(f"清理: {cleaned_count} 个")
    print(f"跳过: {skipped_count} 个")
    print(f"\n下一步:")
    print("1. 提交更改到Git")
    print("2. 推送到GitHub")

if __name__ == "__main__":
    main()
