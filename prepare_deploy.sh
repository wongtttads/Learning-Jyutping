#!/bin/bash

echo "=========================================="
echo "  粤语拼音学习系统 - 部署准备脚本"
echo "=========================================="
echo ""

# 检查当前目录
if [ ! -f "server.py" ]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    exit 1
fi

echo "✅ 检测到项目根目录"
echo ""

# 询问部署平台
echo "请选择部署平台:"
echo "1) GitHub Pages (推荐，完全免费)"
echo "2) Vercel (支持Serverless函数)"
echo "3) Netlify (支持Serverless函数)"
echo "4) 本地测试"
echo ""
read -p "请输入选项 (1-4): " platform

case $platform in
    1)
        echo "准备GitHub Pages部署..."
        deploy_dir="_site"
        ;;
    2)
        echo "准备Vercel部署..."
        deploy_dir=".vercel_build"
        ;;
    3)
        echo "准备Netlify部署..."
        deploy_dir=".netlify_build"
        ;;
    4)
        echo "准备本地测试部署..."
        deploy_dir="dist"
        ;;
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac

echo ""

# 创建部署目录
echo "创建部署目录: $deploy_dir"
rm -rf "$deploy_dir"
mkdir -p "$deploy_dir"

# 复制必要的文件
echo "复制文件..."

# 复制输出文件
cp -r output/* "$deploy_dir/"

# 复制数据文件
mkdir -p "$deploy_dir/data/processed"
cp -r data/processed/* "$deploy_dir/data/processed/" 2>/dev/null || true

# 复制脚本文件
mkdir -p "$deploy_dir/scripts"
cp -r scripts/* "$deploy_dir/scripts/"

# 使用增强版发音脚本
echo "使用增强版发音脚本..."
cp scripts/pronunciation_enhanced.js "$deploy_dir/scripts/pronunciation.js"

# 更新HTML文件中的发音API地址
echo "更新HTML文件..."
if [ "$platform" = "1" ] || [ "$platform" = "4" ]; then
    # GitHub Pages或本地测试：使用Web Speech API
    echo "配置为Web Speech API模式..."
    
    # 更新quiz.html
    if [ -f "$deploy_dir/quiz.html" ]; then
        sed -i '' 's|http://localhost:5001/api|/api|g' "$deploy_dir/quiz.html" 2>/dev/null || \
        sed -i 's|http://localhost:5001/api|/api|g' "$deploy_dir/quiz.html"
    fi
    
    # 创建API模拟文件
    mkdir -p "$deploy_dir/api"
    cat > "$deploy_dir/api/health" << 'EOF'
{
  "status": "ok",
  "service": "Cantonese TTS (Web Speech API Mode)",
  "supported": false,
  "use_web_speech": true,
  "message": "使用浏览器原生的Web Speech API进行发音"
}
EOF
    
    # 创建索引文件
    cat > "$deploy_dir/index.html" << 'EOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>粤语拼音学习系统</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .card { border: 1px solid #ccc; border-radius: 10px; padding: 20px; margin: 20px 0; }
        .btn { display: inline-block; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }
    </style>
</head>
<body>
    <h1><i class="fas fa-language"></i> 粤语拼音学习系统</h1>
    <p>基于《通用规范汉字表》的粤语拼音学习平台</p>
    
    <div class="card">
        <h2><i class="fas fa-book-open"></i> 分章节学习</h2>
        <p>按照频率分成的10个章节，从高频到低频逐步学习汉字和粤语拼音。</p>
        <a href="frequency_chapters.html" class="btn">开始学习</a>
    </div>
    
    <div class="card">
        <h2><i class="fas fa-expand"></i> 全屏学习</h2>
        <p>专注模式，减少干扰，专注于汉字和拼音的学习。</p>
        <a href="learning_fullscreen.html" class="btn">全屏模式</a>
    </div>
    
    <div class="card">
        <h2><i class="fas fa-clipboard-check"></i> 测验系统</h2>
        <p>通过测验检验学习效果，支持汉字→拼音、拼音→汉字等多种模式。</p>
        <a href="quiz.html" class="btn">开始测验</a>
    </div>
    
    <div class="card">
        <h2><i class="fas fa-chart-line"></i> 学习进度</h2>
        <p>查看学习统计、连续学习天数、测验历史和需要复习的汉字。</p>
        <a href="progress.html" class="btn">查看进度</a>
    </div>
    
    <div class="card" style="background: #f8f9fa;">
        <h3><i class="fas fa-info-circle"></i> 发音功能说明</h3>
        <p>本站使用浏览器原生的Web Speech API进行发音。</p>
        <p><strong>支持情况：</strong></p>
        <ul>
            <li>✅ Chrome 33+、Edge、Safari 7+、Firefox 49+</li>
            <li>⚠️ 粤语支持取决于浏览器和操作系统</li>
            <li>📱 在移动设备上可能有限制</li>
        </ul>
    </div>
</body>
</html>
EOF
    
    # 创建.nojekyll文件（用于GitHub Pages）
    touch "$deploy_dir/.nojekyll"
    
elif [ "$platform" = "2" ]; then
    # Vercel：配置Vercel部署
    echo "配置Vercel部署..."
    cp vercel.json "$deploy_dir/"
    
elif [ "$platform" = "3" ]; then
    # Netlify：配置Netlify部署
    echo "配置Netlify部署..."
    cp netlify.toml "$deploy_dir/"
    cp -r netlify "$deploy_dir/"
fi

# 生成数据文件（如果需要）
echo "生成数据文件..."
cd "$deploy_dir" || exit 1

# 检查是否已有数据文件
if [ ! -f "data/processed/jyutping_master.csv" ]; then
    echo "数据文件不存在，尝试生成..."
    
    # 尝试运行数据生成脚本
    if command -v python3 &> /dev/null; then
        echo "使用Python生成数据..."
        cd ..
        python3 scripts/build_master_db.py
        python3 scripts/generate_char_data.py
        python3 scripts/generate_example_words_v3.py
        cd "$deploy_dir" || exit 1
    else
        echo "⚠️  Python3未安装，跳过数据生成"
        echo "⚠️  请确保data/processed/jyutping_master.csv已存在"
    fi
else
    echo "✅ 数据文件已存在"
fi

echo ""
echo "=========================================="
echo "  部署准备完成！"
echo "=========================================="
echo ""
echo "部署目录: $deploy_dir"
echo ""

case $platform in
    1)
        echo "GitHub Pages部署说明:"
        echo "1. 将 $deploy_dir 目录内容推送到GitHub仓库"
        echo "2. 在仓库设置中启用GitHub Pages"
        echo "3. 选择部署分支和目录"
        echo ""
        echo "快速命令:"
        echo "  git add $deploy_dir"
        echo "  git commit -m '部署粤语拼音学习系统'"
        echo "  git push"
        ;;
    2)
        echo "Vercel部署说明:"
        echo "1. 安装Vercel CLI: npm i -g vercel"
        echo "2. 运行: vercel"
        echo "3. 按照提示完成部署"
        ;;
    3)
        echo "Netlify部署说明:"
        echo "1. 将代码推送到GitHub/GitLab仓库"
        echo "2. 登录Netlify，选择'New site from Git'"
        echo "3. 选择仓库，构建设置会自动读取netlify.toml"
        ;;
    4)
        echo "本地测试说明:"
        echo "1. 启动本地服务器:"
        echo "   cd $deploy_dir"
        echo "   python3 -m http.server 8000"
        echo "2. 在浏览器中打开: http://localhost:8000"
        ;;
esac

echo ""
echo "✅ 准备完成！"