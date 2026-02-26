class UIRenderer {
    constructor() {
        this.chaptersContainer = document.getElementById('chapters-container');
        this.chapterContent = document.getElementById('chapter-content');
        this.charactersGrid = document.getElementById('characters-grid');
        this.chapterTitle = document.getElementById('chapter-title');
        this.backBtn = document.getElementById('back-btn');
    }

    renderChapters(chapters) {
        console.log('🎨 渲染章节列表:', chapters.length, '章');
        
        if (!chapters || chapters.length === 0) {
            this.chaptersContainer.innerHTML = `
                <div class="loading">
                    <i class="fas fa-exclamation-circle"></i>
                    <p>章节数据加载失败</p>
                </div>
            `;
            return;
        }

        const html = chapters.map(chapter => `
            <div class="chapter-card" data-chapter-id="${chapter.id}">
                <div class="chapter-number">第 ${chapter.id} 章</div>
                <div class="chapter-title">${chapter.title}</div>
                <div class="chapter-info">
                    <span><i class="fas fa-font"></i> ${chapter.char_count} 字</span>
                    <span><i class="fas fa-sort-numeric-down"></i> 排名 ${chapter.start_rank}-${chapter.end_rank}</span>
                </div>
            </div>
        `).join('');

        this.chaptersContainer.innerHTML = html;

        this.chaptersContainer.querySelectorAll('.chapter-card').forEach(card => {
            card.addEventListener('click', () => {
                const chapterId = parseInt(card.dataset.chapterId);
                this.onChapterClick(chapterId);
            });
        });
    }

    renderCharacters(characters, chapterTitle) {
        console.log('🎨 渲染汉字列表:', characters.length, '个');
        
        this.chapterTitle.textContent = chapterTitle;

        if (!characters || characters.length === 0) {
            this.charactersGrid.innerHTML = `
                <div class="loading">
                    <i class="fas fa-exclamation-circle"></i>
                    <p>暂无汉字数据</p>
                </div>
            `;
            return;
        }

        const html = characters.map(char => `
            <div class="character-card" data-char="${char.char}" data-pinyin="${char.jyutping}">
                <div class="character-char">${char.char}</div>
                <div class="character-pinyin">${char.jyutping}</div>
                <div class="character-rank">排名: ${char.freq_rank}</div>
                <button class="pronunciation-btn" data-char="${char.char}" data-pinyin="${char.jyutping}">
                    <i class="fas fa-volume-up"></i>
                    <span>朗读</span>
                </button>
            </div>
        `).join('');

        this.charactersGrid.innerHTML = html;

        this.charactersGrid.querySelectorAll('.pronunciation-btn').forEach(btn => {
            btn.addEventListener('click', (event) => {
                event.stopPropagation();
                const char = btn.dataset.char;
                const pinyin = btn.dataset.pinyin;
                this.onPronunciationClick(char, pinyin, btn);
            });
        });
    }

    showChaptersView() {
        this.chaptersContainer.classList.remove('hidden');
        this.chapterContent.classList.add('hidden');
    }

    showChapterView() {
        this.chaptersContainer.classList.add('hidden');
        this.chapterContent.classList.remove('hidden');
    }

    onChapterClick(chapterId) {
        console.log(`📖 点击章节: ${chapterId}`);
        if (typeof this.chapterClickHandler === 'function') {
            this.chapterClickHandler(chapterId);
        }
    }

    onPronunciationClick(char, pinyin, button) {
        console.log(`🔊 点击发音: ${char} (${pinyin})`);
        if (typeof this.pronunciationClickHandler === 'function') {
            this.pronunciationClickHandler(char, pinyin, button);
        }
    }

    setChapterClickHandler(handler) {
        this.chapterClickHandler = handler;
    }

    setPronunciationClickHandler(handler) {
        this.pronunciationClickHandler = handler;
    }

    showLoading() {
        this.chaptersContainer.innerHTML = `
            <div class="loading">
                <i class="fas fa-spinner fa-spin"></i>
                <p>加载中...</p>
            </div>
        `;
    }

    hideLoading() {
        const loading = this.chaptersContainer.querySelector('.loading');
        if (loading) {
            loading.remove();
        }
    }
}

window.uiRenderer = new UIRenderer();
