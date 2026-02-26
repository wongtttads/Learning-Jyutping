class CantonesePronunciation {
    constructor() {
        this.isSpeaking = false;
        this.supported = true;
        this.init();
    }
    
    init() {
        console.log('粤语发音功能初始化...');
        this.checkSupport();
    }
    
    checkSupport() {
        if ('speechSynthesis' in window) {
            console.log('✅ 浏览器支持Web Speech API');
            
            const voices = speechSynthesis.getVoices();
            console.log('可用语音数量:', voices.length);
            
            // 查找粤语语音
            const cantoneseVoice = voices.find(voice => 
                voice.lang.includes('zh-HK') || 
                voice.lang.includes('yue') ||
                voice.lang.includes('zh-CN') ||
                voice.name.toLowerCase().includes('cantonese')
            );
            
            if (cantoneseVoice) {
                console.log('✅ 使用语音:', cantoneseVoice.name, cantoneseVoice.lang);
                this.voice = cantoneseVoice;
                this.supported = true;
            } else {
                console.log('⚠️ 未找到粤语语音，使用默认语音');
                this.voice = voices[0] || null;
                this.supported = true;
            }
        } else {
            console.log('❌ 浏览器不支持Web Speech API');
            this.supported = false;
        }
    }
    
    async speak(char, jyutping) {
        if (this.isSpeaking) {
            console.log('正在朗读中，忽略重复调用');
            return false;
        }
        
        if (!this.supported) {
            console.warn('发音功能不支持');
            this.showFallbackMessage(char, jyutping);
            return false;
        }
        
        try {
            const text = `${char} ${jyutping}`;
            this.showSpeakingStatus(char, jyutping);
            
            return this.speakWithWebSpeech(text);
            
        } catch (error) {
            console.error('发音错误:', error);
            this.showFallbackMessage(char, jyutping);
            this.hideSpeakingStatus();
            this.isSpeaking = false;
            return false;
        }
    }
    
    speakWithWebSpeech(text) {
        return new Promise((resolve, reject) => {
            try {
                speechSynthesis.cancel();
                
                const utterance = new SpeechSynthesisUtterance(text);
                
                utterance.lang = 'zh-HK';
                utterance.rate = 0.8;
                utterance.pitch = 1.0;
                
                if (this.voice) {
                    utterance.voice = this.voice;
                }
                
                utterance.onstart = () => {
                    console.log('开始朗读:', text);
                    this.isSpeaking = true;
                };
                
                utterance.onend = () => {
                    console.log('朗读完成');
                    this.isSpeaking = false;
                    this.hideSpeakingStatus();
                    resolve(true);
                };
                
                utterance.onerror = (event) => {
                    console.error('朗读错误:', event.error);
                    this.isSpeaking = false;
                    this.hideSpeakingStatus();
                    reject(event.error);
                };
                
                speechSynthesis.speak(utterance);
            } catch (error) {
                console.error('Web Speech API错误:', error);
                this.isSpeaking = false;
                this.hideSpeakingStatus();
                reject(error);
            }
        });
    }
    
    stop() {
        if ('speechSynthesis' in window) {
            speechSynthesis.cancel();
            this.isSpeaking = false;
            this.hideSpeakingStatus();
        }
    }
    
    showSpeakingStatus(char, jyutping) {
        const existingStatus = document.getElementById('pronunciation-status');
        if (existingStatus) {
            existingStatus.remove();
        }
        
        const statusDiv = document.createElement('div');
        statusDiv.id = 'pronunciation-status';
        statusDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #4CAF50;
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            z-index: 10000;
            font-family: Arial, sans-serif;
            font-size: 14px;
            animation: slideIn 0.3s ease;
        `;
        
        statusDiv.innerHTML = `
            <div style="display: flex; align-items: center; gap: 10px;">
                <i class="fas fa-volume-up" style="font-size: 18px;"></i>
                <span>正在朗读: ${char} (${jyutping})</span>
            </div>
        `;
        
        document.body.appendChild(statusDiv);
        
        setTimeout(() => {
            statusDiv.style.opacity = '0';
            setTimeout(() => statusDiv.remove(), 300);
        }, 2000);
    }
    
    hideSpeakingStatus() {
        const statusDiv = document.getElementById('pronunciation-status');
        if (statusDiv) {
            statusDiv.remove();
        }
    }
    
    showFallbackMessage(char, jyutping) {
        const existingMessage = document.getElementById('pronunciation-fallback');
        if (existingMessage) {
            existingMessage.remove();
        }
        
        const messageDiv = document.createElement('div');
        messageDiv.id = 'pronunciation-fallback';
        messageDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #ff9800;
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            z-index: 10000;
            font-family: Arial, sans-serif;
            font-size: 14px;
            max-width: 300px;
        `;
        
        messageDiv.innerHTML = `
            <div style="display: flex; flex-direction: column; gap: 8px;">
                <strong>发音功能不可用</strong>
                <div style="font-size: 12px;">
                    <div>汉字: ${char}</div>
                    <div>拼音: ${jyutping}</div>
                </div>
            </div>
        `;
        
        document.body.appendChild(messageDiv);
        
        setTimeout(() => {
            messageDiv.style.opacity = '0';
            setTimeout(() => messageDiv.remove(), 300);
        }, 3000);
    }
}

const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(100px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
`;
document.head.appendChild(style);

window.cantonesePronunciation = new CantonesePronunciation();

function speakCharacter(char, jyutping) {
    return window.cantonesePronunciation.speak(char, jyutping);
}