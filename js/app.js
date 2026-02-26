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

            const characters = await window.dataManager.getChapterCharacters(chapterId);
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
        window.uiRenderer.showChaptersView();
    }

    showError(message) {
        const existingError = document.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }

        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.style.cssText = `
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: #f44336;
            color: white;
            padding: 15px 30px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
            z-index: 10000;
            font-family: Arial, sans-serif;
            font-size: 14px;
            animation: slideDown 0.3s ease;
        `;
        errorDiv.innerHTML = `
            <div style="display: flex; align-items: center; gap: 10px;">
                <i class="fas fa-exclamation-triangle"></i>
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(errorDiv);
        
        setTimeout(() => {
            errorDiv.style.opacity = '0';
            setTimeout(() => errorDiv.remove(), 300);
        }, 3000);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new App();
});
