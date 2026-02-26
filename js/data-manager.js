class DataManager {
    constructor() {
        this.chapters = null;
        this.characters = null;
        this.audioIndex = null;
        this.initialized = false;
    }

    async init() {
        console.log('📚 数据管理器初始化...');
        await this.loadChapters();
        await this.loadAudioIndex();
        this.initialized = true;
        console.log('✅ 数据管理器初始化完成');
    }

    async loadChapters() {
        try {
            const response = await fetch('data/chapters.json');
            if (!response.ok) {
                throw new Error('章节数据加载失败');
            }
            this.chapters = await response.json();
            console.log(`✅ 章节数据加载成功: ${this.chapters.length} 章`);
        } catch (error) {
            console.error('❌ 章节数据加载错误:', error);
            this.generateDefaultChapters();
        }
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

    generateDefaultChapters() {
        const totalChars = 8105;
        const charsPerChapter = Math.ceil(totalChars / 10);
        
        this.chapters = [];
        for (let i = 1; i <= 10; i++) {
            const startRank = (i - 1) * charsPerChapter + 1;
            const endRank = Math.min(i * charsPerChapter, totalChars);
            const charCount = endRank - startRank + 1;
            
            this.chapters.push({
                id: i,
                title: `第 ${i} 章`,
                start_rank: startRank,
                end_rank: endRank,
                char_count: charCount
            });
        }
        console.log('⚠️ 使用默认章节数据');
    }

    getChapter(id) {
        return this.chapters?.find(chapter => chapter.id === id);
    }

    getAllChapters() {
        return this.chapters || [];
    }

    async getChapterCharacters(chapterId) {
        try {
            const response = await fetch(`data/chapter_${chapterId}_characters.json`);
            if (!response.ok) {
                throw new Error(`第${chapterId}章汉字数据加载失败`);
            }
            const data = await response.json();
            this.characters = Array.isArray(data) ? data : (data.characters || []);
            console.log(`✅ 第${chapterId}章汉字数据加载成功: ${this.characters.length} 个`);
            return this.characters;
        } catch (error) {
            console.error(`❌ 第${chapterId}章汉字数据加载错误:`, error);
            return [];
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

    getStats() {
        return {
            totalChapters: this.chapters?.length || 10,
            totalCharacters: this.audioIndex?.total_count || 7990,
            totalAudioFiles: this.audioIndex?.total_count || 7990
        };
    }
}

window.dataManager = new DataManager();
