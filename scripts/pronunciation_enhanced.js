class CantonesePronunciation {
    constructor() {
        this.isSpeaking = false;
        this.supported = true;
        this.apiBaseUrl = 'http://localhost:5001/api';
        this.useWebSpeech = false;
        this.init();
    }
    
    init() {
        console.log('粤语发音功能初始化...');
        this.checkSupport();
    }
    
    async checkSupport() {
        // 首先检查Web Speech API支持
        if ('speechSynthesis' in window) {
            console.log('✅ 浏览器支持Web Speech API');
            
            // 检查是否有粤语语音
            const voices = speechSynthesis.getVoices();
            const cantoneseVoice = voices.find(voice => 
                voice.lang.includes('zh-HK') || 
                voice.lang.includes('yue') ||
                voice.name.toLowerCase().includes('cantonese')
            );
            
            if (cantoneseVoice) {
                console.log('✅ 找到粤语语音:', cantoneseVoice.name);
                this.useWebSpeech = true;
                this.supported = true;
            } else {
                console.log('⚠️ 未找到粤语语音，尝试使用默认语音');
                this.useWebSpeech = true;
                this.supported = true;
            }
        } else {
            console.log('❌ 浏览器不支持Web Speech API');
            this.useWebSpeech = false;
        }
        
        // 如果支持Web Speech API，就不需要检查服务器
        if (this.useWebSpeech) {
            console.log('使用Web Speech API模式');
            return;
        }
        
        // 检查服务器支持
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
            
            if (this.useWebSpeech) {
                return this.speakWithWebSpeech(text);
            } else {
                return await this.speakWithServer(text);
            }
            
        } catch (error) {
            console.error('发音错误:', error);
            this.showFallbackMessage(char, jyutping);
            this.hideSpeakingStatus();
            this.isSpeaking = false;
            return false;
        }
    }
    
    speakWithWebSpeech(text) {
        try {
            // 停止当前任何语音
            speechSynthesis.cancel();
            
            // 创建语音实例
            const utterance = new SpeechSynthesisUtterance(text);
            
            // 设置语音参数
            utterance.lang = 'zh-HK'; // 粤语（香港）
            utterance.rate = 0.8; // 稍慢速度
            
            // 尝试找到粤语语音
            const voices = speechSynthesis.getVoices();
            const cantoneseVoice = voices.find(voice => 
                voice.lang.includes('zh-HK') || 
                voice.lang.includes('yue') ||
                voice.name.toLowerCase().includes('cantonese')
            );
            
            if (cantoneseVoice) {
                utterance.voice = cantoneseVoice;
            }
            
            utterance.onstart = () => {
                this.isSpeaking = true;
            };
            
            utterance.onend = () => {
                this.isSpeaking = false;
                this.hideSpeakingStatus();
            };
            
            utterance.onerror = (event) => {
                console.error('Web Speech API错误:', event.error);
                this.isSpeaking = false;
                this.hideSpeakingStatus();
            };
            
            // 开始朗读
            speechSynthesis.speak(utterance);
            
            // 设置超时，防止语音卡住
            setTimeout(() => {
                if (this.isSpeaking) {
                    this.isSpeaking = false;
                    this.hideSpeakingStatus();
                }
            }, 5000);
            
            return true;
            
        } catch (error) {
            console.error('Web Speech API调用错误:', error);
            return false;
        }
    }
    
    async speakWithServer(text) {
        try {
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
            console.error('服务器发音错误:', error);
            return false;
        }
    }
    
    async stop() {
        try {
            if (this.useWebSpeech) {
                speechSynthesis.cancel();
            } else {
                await fetch(`${this.apiBaseUrl}/stop`, {
                    method: 'POST'
                });
            }
            
            this.isSpeaking = false;
            this.hideSpeakingStatus();
            return true;
            
        } catch (error) {
            console.error('停止发音错误:', error);
            return false;
        }
    }
    
    showSpeakingStatus(char, jyutping) {
        // 可以显示一个状态提示，但这里暂时不实现
        console.log(`正在朗读: ${char} ${jyutping}`);
    }
    
    hideSpeakingStatus() {
        // 隐藏状态提示
        console.log('朗读完成');
    }
    
    showFallbackMessage(char, jyutping) {
        // 显示备选消息
        console.log(`无法朗读 ${char} ${jyutping}，请检查浏览器或系统设置`);
        
        // 可以在这里添加UI提示
        const message = `发音功能不可用\n汉字: ${char}\n拼音: ${jyutping}`;
        alert(message);
    }
}

// 全局实例
window.cantonesePronunciation = new CantonesePronunciation();

// 为了方便，也提供一个全局函数
function speakCharacter(char, jyutping) {
    return window.cantonesePronunciation.speak(char, jyutping);
}

function stopSpeaking() {
    return window.cantonesePronunciation.stop();
}