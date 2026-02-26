#!/bin/bash

echo "=========================================="
echo "  粤语拼音学习系统 - 启动脚本"
echo "=========================================="
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python3"
    exit 1
fi

echo "✅ Python3 已安装"

# 检查是否安装了依赖
echo ""
echo "检查依赖..."

if ! python3 -c "import flask" 2>/dev/null; then
    echo "⚠️  Flask 未安装，正在安装..."
    pip3 install flask flask-cors
fi

if ! python3 -c "import pandas" 2>/dev/null; then
    echo "⚠️  Pandas 未安装，正在安装..."
    pip3 install pandas
fi

if ! python3 -c "import ToJyutping" 2>/dev/null; then
    echo "⚠️  ToJyutping 未安装，正在安装..."
    pip3 install ToJyutping
fi

echo "✅ 依赖检查完成"
echo ""

# 检查数据文件是否存在
if [ ! -f "data/processed/jyutping_master.csv" ]; then
    echo "⚠️  主数据文件不存在，是否需要生成数据？(y/n)"
    read -r response
    if [ "$response" = "y" ]; then
        echo "正在生成数据..."
        python3 scripts/build_master_db.py
        python3 scripts/generate_char_data.py
        python3 scripts/generate_example_words_v3.py
    fi
fi

# 检查是否需要验证数据
echo ""
echo "是否需要验证数据质量？(y/n)"
read -r validate_response
if [ "$validate_response" = "y" ]; then
    python3 scripts/validate_data.py
fi

echo ""
echo "=========================================="
echo "  启动发音服务器..."
echo "=========================================="
echo ""
echo "服务器将在 http://localhost:5001 启动"
echo "按 Ctrl+C 停止服务器"
echo ""

# 启动服务器
python3 server.py
