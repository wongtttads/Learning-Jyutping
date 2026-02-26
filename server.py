#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
粤语发音服务器 - 提供TTS API
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import subprocess
import os
import threading
import re

app = Flask(__name__, static_folder='.', static_url_path='')

CORS(app, origins=[
    "http://localhost:5001",
    "http://127.0.0.1:5001",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
])

def validate_text(text):
    """验证和清理输入文本"""
    if not text:
        return ""
    
    # 移除可能有害的字符
    text = re.sub(r'[;|&$`<>"\']', '', text)
    
    # 限制长度
    if len(text) > 1000:
        text = text[:1000]
    
    # 只保留中文字符、英文字母、数字和基本标点
    text = re.sub(r'[^\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaffa-zA-Z0-9\s,.!?;:、。，！？；：]', '', text)
    
    return text.strip()

class CantoneseTTS:
    def __init__(self):
        self.is_speaking = False
        self.current_process = None
        self.check_support()
    
    def check_support(self):
        """检查系统支持情况"""
        try:
            # 检查是否在macOS上
            result = subprocess.run(['uname'], capture_output=True, text=True)
            if 'Darwin' not in result.stdout:
                return False
            
            # 检查say命令是否可用
            result = subprocess.run(['say', '-v', '?'], capture_output=True, text=True)
            if 'Sinji' not in result.stdout:
                print("警告: 粤语语音包Sinji未安装")
                return False
            
            return True
        except Exception as e:
            print(f"检查支持失败: {e}")
            return False
    
    def speak(self, text):
        """朗读文本"""
        if not self.check_support():
            return {'success': False, 'error': '系统不支持粤语发音'}
        
        try:
            # 验证和清理文本
            text = validate_text(text)
            
            if not text:
                return {'success': False, 'error': '文本不能为空或包含无效字符'}
            
            # 停止之前的朗读
            self.stop()
            
            # 使用say命令朗读
            self.current_process = subprocess.Popen(
                ['say', '-v', 'Sinji', text],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            self.is_speaking = True
            
            # 在后台等待进程结束
            def wait_for_completion():
                self.current_process.wait()
                self.is_speaking = False
            
            thread = threading.Thread(target=wait_for_completion)
            thread.daemon = True
            thread.start()
            
            return {'success': True, 'message': '正在朗读'}
            
        except Exception as e:
            print(f"朗读错误: {e}")
            return {'success': False, 'error': '朗读失败，请稍后重试'}
    
    def stop(self):
        """停止朗读"""
        try:
            if self.current_process:
                self.current_process.terminate()
                self.current_process = None
            
            # 强制停止所有say进程
            subprocess.run(['killall', 'say'], capture_output=True)
            
            self.is_speaking = False
            return {'success': True, 'message': '已停止'}
            
        except Exception as e:
            print(f"停止朗读错误: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_status(self):
        """获取状态"""
        return {
            'is_speaking': self.is_speaking,
            'supported': self.check_support()
        }

tts = CantoneseTTS()

@app.route('/api/speak', methods=['POST'])
def speak():
    """朗读API"""
    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({'success': False, 'error': '文本不能为空'})
    
    result = tts.speak(text)
    return jsonify(result)

@app.route('/api/stop', methods=['POST'])
def stop():
    """停止朗读API"""
    result = tts.stop()
    return jsonify(result)

@app.route('/api/status', methods=['GET'])
def status():
    """获取状态API"""
    result = tts.get_status()
    return jsonify(result)

@app.route('/api/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'service': 'Cantonese TTS Server',
        'supported': tts.check_support()
    })

@app.errorhandler(Exception)
def handle_exception(e):
    """通用错误处理器"""
    print(f"服务器错误: {e}")
    return jsonify({
        'success': False,
        'error': '服务器内部错误，请稍后重试'
    }), 500

@app.errorhandler(404)
def handle_not_found(e):
    """404错误处理器"""
    return jsonify({
        'success': False,
        'error': '请求的资源不存在'
    }), 404

@app.errorhandler(405)
def handle_method_not_allowed(e):
    """405错误处理器"""
    return jsonify({
        'success': False,
        'error': '不支持的请求方法'
    }), 405

@app.route('/')
def index():
    """欢迎页面"""
    return '''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>粤语拼音学习系统</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #333;
                line-height: 1.6;
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            
            header {
                text-align: center;
                margin-bottom: 50px;
                padding: 40px;
                background: white;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            }
            
            h1 {
                color: #667eea;
                font-size: 3rem;
                margin-bottom: 10px;
            }
            
            .subtitle {
                color: #666;
                font-size: 1.3rem;
            }
            
            .status {
                margin-top: 20px;
                padding: 15px;
                border-radius: 10px;
                background: #f8f9fa;
                display: inline-block;
            }
            
            .status.ok {
                background: #d4edda;
                color: #155724;
            }
            
            .status.error {
                background: #f8d7da;
                color: #721c24;
            }
            
            .cards {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 30px;
                margin-bottom: 50px;
            }
            
            .card {
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            }
            
            .card-icon {
                font-size: 3rem;
                margin-bottom: 20px;
                color: #667eea;
            }
            
            .card h2 {
                color: #333;
                margin-bottom: 15px;
            }
            
            .card p {
                color: #666;
                margin-bottom: 20px;
            }
            
            .card-btn {
                display: inline-block;
                padding: 12px 25px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            
            .card-btn:hover {
                transform: translateY(-3px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }
            
            .info-section {
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            }
            
            .info-section h2 {
                color: #667eea;
                margin-bottom: 20px;
            }
            
            .info-item {
                padding: 15px;
                margin-bottom: 10px;
                background: #f8f9fa;
                border-radius: 8px;
                border-left: 4px solid #667eea;
            }
            
            .info-item strong {
                color: #333;
            }
            
            .info-item code {
                background: #e9ecef;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1><i class="fas fa-language"></i> 粤语拼音学习系统</h1>
                <p class="subtitle">基于《通用规范汉字表》的粤语拼音学习平台</p>
                <div class="status ok">
                    <i class="fas fa-check-circle"></i> 发音服务器运行中
                </div>
            </header>
            
            <div class="cards">
                <div class="card">
                    <div class="card-icon">
                        <i class="fas fa-book-open"></i>
                    </div>
                    <h2>分章节学习</h2>
                    <p>按照频率分成的10个章节，从高频到低频逐步学习汉字和粤语拼音。</p>
                    <a href="output/frequency_chapters.html" class="card-btn">
                        <i class="fas fa-arrow-right"></i> 开始学习
                    </a>
                </div>
                
                <div class="card">
                    <div class="card-icon">
                        <i class="fas fa-expand"></i>
                    </div>
                    <h2>全屏学习</h2>
                    <p>专注模式，减少干扰，专注于汉字和拼音的学习。</p>
                    <a href="output/learning_fullscreen.html" class="card-btn">
                        <i class="fas fa-arrow-right"></i> 全屏模式
                    </a>
                </div>
                
                <div class="card">
                    <div class="card-icon">
                        <i class="fas fa-clipboard-check"></i>
                    </div>
                    <h2>测验系统</h2>
                    <p>通过测验检验学习效果，支持汉字→拼音、拼音→汉字等多种模式。</p>
                    <a href="output/quiz.html" class="card-btn">
                        <i class="fas fa-arrow-right"></i> 开始测验
                    </a>
                </div>
                
                <div class="card">
                    <div class="card-icon">
                        <i class="fas fa-chart-line"></i>
                    </div>
                    <h2>学习进度</h2>
                    <p>查看学习统计、连续学习天数、测验历史和需要复习的汉字。</p>
                    <a href="output/progress.html" class="card-btn">
                        <i class="fas fa-arrow-right"></i> 查看进度
                    </a>
                </div>
            </div>
            
            <div class="info-section">
                <h2><i class="fas fa-info-circle"></i> 使用说明</h2>
                
                <div class="info-item">
                    <strong>发音功能：</strong> 点击汉字卡片可以听到粤语发音（需要macOS系统）
                </div>
                
                <div class="info-item">
                    <strong>API端点：</strong> 
                    <code>POST /api/speak</code> - 朗读文本 | 
                    <code>POST /api/stop</code> - 停止朗读 | 
                    <code>GET /api/status</code> - 获取状态
                </div>
                
                <div class="info-item">
                    <strong>数据文件：</strong> 
                    <code>data/processed/jyutping_master.csv</code> - 主数据文件 | 
                    <code>output/data/chapter_characters.json</code> - 章节数据
                </div>
                
                <div class="info-item">
                    <strong>文档：</strong> 
                    查看 <a href="README.md" style="color: #667eea;">README.md</a> 了解更多详情
                </div>
            </div>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    print("=" * 50)
    print("粤语发音服务器启动中...")
    print("=" * 50)
    
    if tts.check_support():
        print("✅ 系统支持粤语发音")
    else:
        print("❌ 系统不支持粤语发音")
    
    print("\nAPI端点:")
    print("  POST /api/speak  - 朗读文本")
    print("  POST /api/stop   - 停止朗读")
    print("  GET  /api/status - 获取状态")
    print("  GET  /api/health - 健康检查")
    print("\n服务器运行在: http://localhost:5001")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5001, debug=False)
