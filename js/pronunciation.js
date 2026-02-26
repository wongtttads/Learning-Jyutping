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
            return null;
        }

        const multiChar = this.audioIndex.multi_chars?.find(
            item => item.char === char && item.jyutping === jyutping
        );

        if (multiChar) {
            return multiChar.audio_path;
        }

        const singleChar = this.audioIndex.single_chars?.find(
            item => item.char === char
        );

        if (singleChar) {
            return singleChar.audio_path;
        }

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
        return new Promise((resolve, reject) => {
            if (this.currentAudio) {
                this.currentAudio.pause();
                this.currentAudio.currentTime = 0;
            }

            this.currentAudio = new Audio(audioPath);
            
            this.currentAudio.onended = () => {
                this.isSpeaking = false;
                resolve(true);
            };

            this.currentAudio.onerror = (error) => {
                console.error('❌ 音频播放错误:', error);
                this.isSpeaking = false;
                reject(error);
            };

            this.currentAudio.oncanplay = () => {
                console.log('▶️ 开始播放音频');
            };

            this.currentAudio.play().catch(error => {
                console.error('❌ 音频播放失败:', error);
                this.isSpeaking = false;
                reject(error);
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
            return false;
        }

        const resolvedPath = this.resolveAudioPath(audioPath);
        console.log(`🎵 播放音频: ${resolvedPath}`);
        try {
            await this.playAudio(resolvedPath);
            return true;
        } catch (error) {
            console.error('❌ 发音失败:', error);
            return false;
        }
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
