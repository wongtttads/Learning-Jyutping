class CantonesePronunciation {
    constructor() {
        this.isSpeaking = false;
        this.supported = true;
        this.audioIndex = null;
        this.audioCache = new Map();
        this.init();
    }
    
    async init() {
        console.log('粤语发音功能初始化（预录制音频优先）...');
        await this.loadAudioIndex();
    }
    
    async loadAudioIndex() {
        try {
            const response = await fetch('audio/index.json');
            if (response.ok) {
                this.audioIndex = await response.json();
                console.log('✅ 音频索引加载成功');
                console.log(`   单音字: ${this.audioIndex.single_chars_count} 个`);
                console.log(`   多音字: ${this.audioIndex.multi_chars_count} 个`);
                console.log(`   总计: ${this.audioIndex.total_count} 个`);
                this.supported = true;
            } else {
                console.log('⚠️ 音频索引加载失败，使用Web Speech API');
                this.supported = false;
            }
        } catch (error) {
            console.log('⚠️ 音频索引加载异常，使用Web Speech API');
            console.log('   错误:', error.message);
            this.supported = false;
        }
    }
    
    findAudioPath(char, jyutping) {
        if (!this.audioIndex) {
            console.log('⚠️ 音频索引未加载');
            return null;
        }
        
        // 先查找多音字
        const multiChar = this.audioIndex.multi_chars.find(
            item => item.char === char && item.jyutping === jyutping
        );
        
        if (multiChar) {
            return this.resolveAudioPath(multiChar.audio_path);
        }
        
        // 再查找单音字
        const singleChar = this.audioIndex.single_chars.find(
            item => item.char === char
        );
        
        if (singleChar) {
            return this.resolveAudioPath(singleChar.audio_path);
        }
        
        console.log(`⚠️ 未找到音频: ${char} (${jyutping})`);
        return null;
    }
    
    resolveAudioPath(audioPath) {
        // 根据当前页面位置调整音频路径
        const currentPath = window.location.pathname;
        
        // 如果在output目录下，需要返回上级目录
        if (currentPath.includes('/output/')) {
            return '../' + audioPath;
        }
        
        // 如果在根目录或其他位置，使用相对路径
        return audioPath;
    }
    
    async playAudio(audioPath) {
        return new Promise(async (resolve, reject) => {
            const audio = new Audio(audioPath);
            
            audio.onended = () => {
                this.isSpeaking = false;
                this.hideSpeakingStatus();
                resolve(true);
            };
            
            audio.onerror = (error) => {
                console.error('音频播放错误:', error);
                this.isSpeaking = false;
                this.hideSpeakingStatus();
                reject(error);
            };
            
            try {
                await audio.play();
            } catch (error) {
                console.error('音频播放失败:', error);
                this.isSpeaking = false;
                this.hideSpeakingStatus();
                reject(error);
            }
        });
    }
    
    async speakWithWebSpeech(text) {
        if (!('speechSynthesis' in window)) {
            throw new Error('浏览器不支持Web Speech API');
        }
        
        return new Promise((resolve, reject) => {
            try {
                speechSynthesis.cancel();
                
                const utterance = new SpeechSynthesisUtterance(text);
                
                utterance.lang = 'zh-HK';
                utterance.rate = 0.8;
                utterance.pitch = 1.0;
                
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
    
    async speak(char, jyutping) {
        console.log(`🔊 发音请求: ${char} (${jyutping})`);
        
        if (this.isSpeaking) {
            console.log('正在朗读中，忽略重复调用');
            return false;
        }
        
        this.isSpeaking = true;
        
        try {
            this.showSpeakingStatus(char, jyutping);
            
            // 优先使用预录制音频
            const audioPath = this.findAudioPath(char, jyutping);
            
            if (audioPath) {
                console.log('🎵 使用预录制音频:', audioPath);
                const result = await this.playAudio(audioPath);
                return result;
            } else {
                console.log('⚠️ 未找到预录制音频，使用Web Speech API');
                const text = `${char} ${jyutping}`;
                const result = await this.speakWithWebSpeech(text);
                return result;
            }
            
        } catch (error) {
            console.error('❌ 发音错误:', error);
            this.showFallbackMessage(char, jyutping);
            this.hideSpeakingStatus();
            this.isSpeaking = false;
            return false;
        }
    }
    
    stop() {
        if ('speechSynthesis' in window) {
            speechSynthesis.cancel();
        }
        this.isSpeaking = false;
        this.hideSpeakingStatus();
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
