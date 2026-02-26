class App {
    constructor() {
        this.currentChapter = null;
        this.currentCharacters = [];
        this.init();
    }

    async init() {
        console.log('🚀 应用初始化...');
        
        try {
            await window.dataManager.init();
            await window.pronunciationSystem.init();
            
            this.setupEventListeners();
            this.loadChapters();
            
            console.log('✅ 应用初始化完成');
        } catch (error) {
            console.error('❌ 应用初始化失败:', error);
            this.showError('应用初始化失败，请刷新页面重试');
        }
    }

    setupEventListeners() {
        window.uiRenderer.setChapterClickHandler((chapterId) => {
            this.loadChapter(chapterId);
        });

        window.uiRenderer.setPronunciationClickHandler((char, pinyin, button) => {
            this.playPronunciation(char, pinyin, button);
        });

        document.getElementById('back-btn').addEventListener('click', () => {
            this.backToChapters();
        });
    }

    async loadChapters() {
        window.uiRenderer.showLoading();
        
        try {
            const chapters = window.dataManager.getAllChapters();
            window.uiRenderer.renderChapters(chapters);
            window.uiRenderer.showChaptersView();
            window.uiRenderer.hideLoading();
        } catch (error) {
            console.error('❌ 章节加载失败:', error);
            window.uiRenderer.hideLoading();
            this.showError('章节数据加载失败');
        }
    }

    async loadChapter(chapterId) {
        console.log(`📖 加载章节: ${chapterId}`);
        
        window.uiRenderer.showLoading();
        
        try {
            const chapter = window.dataManager.getChapter(chapterId);
            if (!chapter) {
                throw new Error(`章节 ${chapterId} 不存在`);
            }

            console.log(`📊 章节信息: ${chapter.title}, 字符数: ${chapter.char_count}`);
            
            const characters = await window.dataManager.getChapterCharacters(chapterId);
            console.log(`📋 加载到的字符数: ${characters.length}`);
            
            if (characters.length > 0) {
                console.log(`📝 前3个字符:`, characters.slice(0, 3));
            }

            this.currentChapter = chapter;
            this.currentCharacters = characters;

            window.uiRenderer.renderCharacters(characters, chapter.title);
            window.uiRenderer.showChapterView();
            window.uiRenderer.hideLoading();
        } catch (error) {
            console.error('❌ 章节加载失败:', error);
            window.uiRenderer.hideLoading();
            this.showError('章节内容加载失败');
        }
    }

    async playPronunciation(char, pinyin, button) {
        try {
            button.classList.add('playing');
            const success = await window.pronunciationSystem.speak(char, pinyin);
            
            if (success) {
                setTimeout(() => {
                    button.classList.remove('playing');
                }, 500);
            } else {
                button.classList.remove('playing');
                this.showError('发音失败，请稍后重试');
            }
        } catch (error) {
            console.error('❌ 发音播放失败:', error);
            button.classList.remove('playing');
            this.showError('发音失败');
        }
    }

    backToChapters() {
        console.log('🔙 返回章节列表');
        this.currentChapter = null;
        this.currentCharacters = [];
        
        // 重新加载章节列表
        this.loadChapters();
    }

    showError(message) {
        const existingError = document.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }

        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.innerHTML = `
            <i class="fas fa-exclamation-triangle"></i>
            <span>${message}</span>
        `;
        
        document.body.appendChild(errorDiv);
        
        setTimeout(() => {
            errorDiv.style.animation = 'fadeOut 0.3s ease forwards';
            setTimeout(() => errorDiv.remove(), 300);
        }, 3000);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new App();
});
