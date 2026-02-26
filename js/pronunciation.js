class PronunciationSystem {
    constructor() {
        this.isSpeaking = false;
        this.currentAudio = null;
        this.audioIndex = null;
    }

    async init() {
        console.log('🔊 发音系统初始化...');
        await this.loadAudioIndex();
    }

    async loadAudioIndex() {
        // 根据当前页面位置确定正确的路径
        const currentPath = window.location.pathname;
        const indexPath = currentPath.includes('/output/') ? '../audio/index.json' : 'audio/index.json';
        
        console.log('📂 尝试加载音频索引:', indexPath);
        
        try {
            const response = await fetch(indexPath);
            if (!response.ok) {
                throw new Error('音频索引加载失败');
            }
            this.audioIndex = await response.json();
            console.log(`✅ 音频索引加载成功: ${this.audioIndex.total_count} 个`);
        } catch (error) {
            console.error('❌ 音频索引加载错误:', error);
            this.audioIndex = null;
        }
    }

    findAudioPath(char, jyutping) {
        if (!this.audioIndex) {
            console.log(`⚠️ 音频索引未加载: ${char} (${jyutping})`);
            return null;
        }

        console.log(`🔍 查找音频: ${char} (${jyutping})`);
        console.log(`  单音字数量: ${this.audioIndex.single_chars?.length || 0}`);
        console.log(`  多音字数量: ${this.audioIndex.multi_chars?.length || 0}`);

        const multiChar = this.audioIndex.multi_chars?.find(
            item => item.char === char && item.jyutping === jyutping
        );

        if (multiChar) {
            console.log(`✅ 找到多音字音频: ${multiChar.audio_path}`);
            return multiChar.audio_path;
        }

        const singleChar = this.audioIndex.single_chars?.find(
            item => item.char === char
        );

        if (singleChar) {
            console.log(`✅ 找到单音字音频: ${singleChar.audio_path}`);
            return singleChar.audio_path;
        }

        console.log(`❌ 未找到音频: ${char} (${jyutping})`);
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
        console.log(`🎵 创建音频对象: ${audioPath}`);
        
        return new Promise((resolve, reject) => {
            if (this.currentAudio) {
                console.log('⏹️ 停止当前音频');
                this.currentAudio.pause();
                this.currentAudio.currentTime = 0;
            }

            // 检查文件扩展名，如果是.mp3但实际是AIFF-C格式，需要特殊处理
            const isAiffFile = audioPath.toLowerCase().endsWith('.mp3');
            console.log(`📁 文件扩展名检查: ${audioPath}, 可能是AIFF-C格式: ${isAiffFile}`);
            
            this.currentAudio = new Audio(audioPath);
            
            // 如果是AIFF-C格式，尝试设置正确的MIME类型
            if (isAiffFile) {
                console.log('⚠️ 检测到可能是AIFF-C格式的MP3文件，尝试设置MIME类型');
                // 注意：HTML5 Audio元素不支持直接设置MIME类型
                // 但我们可以尝试其他方法
            }
            
            console.log(`🔊 音频对象创建完成`);
            
            this.currentAudio.onended = () => {
                console.log('✅ 音频播放完成');
                this.isSpeaking = false;
                resolve(true);
            };

            this.currentAudio.onerror = (error) => {
                console.error('❌ 音频播放错误:', error);
                console.error('  错误类型:', error.type);
                console.error('  错误目标:', error.target);
                
                // 如果是格式错误，尝试使用Web Speech API作为备选
                if (error.type === 'media' || error.type === 'decode') {
                    console.log('⚠️ 检测到媒体格式错误，尝试备选方案');
                    this.isSpeaking = false;
                    reject(new Error('MEDIA_FORMAT_ERROR'));
                } else {
                    this.isSpeaking = false;
                    reject(error);
                }
            };

            this.currentAudio.oncanplay = () => {
                console.log('▶️ 音频可以播放了');
            };

            this.currentAudio.oncanplaythrough = () => {
                console.log('📊 音频可以完整播放');
            };

            this.currentAudio.onloadstart = () => {
                console.log('📥 开始加载音频');
            };

            this.currentAudio.onprogress = (event) => {
                if (event.lengthComputable) {
                    const percent = (event.loaded / event.total) * 100;
                    console.log(`📈 音频加载进度: ${percent.toFixed(1)}%`);
                }
            };

            console.log('▶️ 尝试播放音频...');
            this.currentAudio.play().then(() => {
                console.log('✅ 音频播放开始');
            }).catch(error => {
                console.error('❌ 音频播放失败:', error);
                console.error('  错误名称:', error.name);
                console.error('  错误消息:', error.message);
                
                // 如果是NotAllowedError，说明需要用户交互
                if (error.name === 'NotAllowedError') {
                    console.log('⚠️ 浏览器阻止自动播放，需要用户交互');
                    this.isSpeaking = false;
                    reject(new Error('AUTOPLAY_BLOCKED'));
                } else {
                    this.isSpeaking = false;
                    reject(error);
                }
            });

            this.isSpeaking = true;
        });
    }

    async speak(char, jyutping) {
        console.log(`🔊 发音请求: ${char} (${jyutping})`);

        if (this.isSpeaking) {
            console.log('⏳ 正在播放中，先停止');
            this.stop();
        }

        const audioPath = this.findAudioPath(char, jyutping);

        if (!audioPath) {
            console.warn(`⚠️ 未找到音频: ${char} (${jyutping})`);
            return this.speakWithWebSpeech(char, jyutping);
        }

        const resolvedPath = this.resolveAudioPath(audioPath);
        console.log(`🎵 播放音频: ${resolvedPath}`);
        try {
            await this.playAudio(resolvedPath);
            return true;
        } catch (error) {
            console.error('❌ 发音失败:', error);
            
            // 根据错误类型选择备选方案
            if (error.message === 'MEDIA_FORMAT_ERROR' || error.message === 'AUTOPLAY_BLOCKED') {
                console.log('🔄 使用Web Speech API作为备选方案');
                return this.speakWithWebSpeech(char, jyutping);
            }
            
            return false;
        }
    }

    async speakWithWebSpeech(char, jyutping) {
        console.log(`🗣️ 使用Web Speech API: ${char} (${jyutping})`);
        
        if (!('speechSynthesis' in window)) {
            console.error('❌ Web Speech API不可用');
            return false;
        }

        return new Promise((resolve) => {
            // 停止当前任何语音
            speechSynthesis.cancel();
            
            const utterance = new SpeechSynthesisUtterance(`${char} ${jyutping}`);
            utterance.lang = 'zh-CN'; // 使用中文语音
            utterance.rate = 0.8; // 稍微慢一点
            
            utterance.onend = () => {
                console.log('✅ Web Speech API发音完成');
                this.isSpeaking = false;
                resolve(true);
            };
            
            utterance.onerror = (error) => {
                console.error('❌ Web Speech API错误:', error);
                this.isSpeaking = false;
                resolve(false);
            };
            
            this.isSpeaking = true;
            speechSynthesis.speak(utterance);
            console.log('▶️ Web Speech API开始发音');
        });
    }

    stop() {
        if (this.currentAudio) {
            this.currentAudio.pause();
            this.currentAudio.currentTime = 0;
            this.currentAudio = null;
        }
        this.isSpeaking = false;
        console.log('⏹️ 停止播放');
    }

    isAvailable() {
        return this.audioIndex !== null;
    }
}

window.pronunciationSystem = new PronunciationSystem();
