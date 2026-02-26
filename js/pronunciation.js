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
        try {
            const response = await fetch('audio/index.json');
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

        console.log(`🎵 播放音频: ${audioPath}`);
        try {
            await this.playAudio(audioPath);
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
