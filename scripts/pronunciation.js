
// 粤语发音功能
class CantonesePronunciation {
    constructor() {
        this.isSpeaking = false;
        this.supported = true;
        this.apiBaseUrl = 'http://localhost:5001/api';
        this.init();
    }
    
    init() {
        console.log('粤语发音功能初始化完成');
        this.checkServerStatus();
    }
    
    async checkServerStatus() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`);
            const data = await response.json();
            console.log('服务器状态:', data);
            this.supported = data.supported;
        } catch (error) {
            console.warn('无法连接到发音服务器:', error);
            this.supported = false;
        }
    }
    
    async speak(char, jyutping) {
        if (this.isSpeaking) {
            console.log('正在朗读中，忽略重复调用');
            return false;
        }
        
        try {
            const text = `${char} ${jyutping}`;
            this.showSpeakingStatus(char, jyutping);
            
            const response = await fetch(`${this.apiBaseUrl}/speak`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.isSpeaking = true;
                
                // 3秒后自动重置状态
                setTimeout(() => {
                    this.isSpeaking = false;
                }, 3000);
                
                return true;
            } else {
                throw new Error(result.error || '发音失败');
            }
            
        } catch (error) {
            console.error('发音错误:', error);
            this.showFallbackMessage(char, jyutping);
            this.hideSpeakingStatus();
            this.isSpeaking = false;
            return false;
        }
    }
    
    async stop() {
        try {
            await fetch(`${this.apiBaseUrl}/stop`, {
                method: 'POST'
            });
            
            this.isSpeaking = false;
            this.hideSpeakingStatus();
            return true;
            
        } catch (error) {
            console.error('停止发音错误:', error);
            return false;
        }
    }
    
    // 显示朗读状态
    showSpeakingStatus(char, jyutping) {
        // 创建状态提示
        const statusDiv = document.createElement('div');
        statusDiv.id = 'pronunciation-status';
        statusDiv.innerHTML = `
            <div style="
                position: fixed;
                top: 20px;
                right: 20px;
                background: #4CAF50;
                color: white;
                padding: 15px 20px;
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                z-index: 1000;
                display: flex;
                align-items: center;
                gap: 10px;
                animation: slideIn 0.3s ease;
            ">
                <i class="fas fa-volume-up" style="font-size: 1.2rem;"></i>
                <div>
                    <div style="font-weight: bold;">正在朗读</div>
                    <div style="font-size: 0.9rem; opacity: 0.9;">${char} ${jyutping}</div>
                </div>
                <button onclick="window.cantonesePronunciation.stop()" 
                        style="
                            background: rgba(255,255,255,0.2);
                            border: none;
                            color: white;
                            padding: 5px 10px;
                            border-radius: 5px;
                            cursor: pointer;
                            margin-left: 10px;
                        ">
                    停止
                </button>
            </div>
        `;
        
        // 添加CSS动画
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        
        document.head.appendChild(style);
        document.body.appendChild(statusDiv);
    }
    
    // 隐藏朗读状态
    hideSpeakingStatus() {
        const statusDiv = document.getElementById('pronunciation-status');
        if (statusDiv) {
            statusDiv.remove();
        }
    }
    
    // 显示备选方案消息
    showFallbackMessage(char, jyutping) {
        alert(`汉字: ${char}\n粤拼: ${jyutping}\n\n发音功能需要macOS系统支持。\n请手动朗读或使用其他粤语发音工具。`);
    }
}

// 创建全局发音实例
window.cantonesePronunciation = new CantonesePronunciation();

// 点击汉字卡片时的处理函数
function speakCharacter(char, jyutping) {
    return window.cantonesePronunciation.speak(char, jyutping);
}
