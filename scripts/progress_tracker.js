class ProgressTracker {
    constructor() {
        this.storageKey = 'cantonese_learning_progress';
        this.progress = this.loadProgress();
        this.init();
    }
    
    init() {
        console.log('进度跟踪系统初始化完成');
        console.log('当前进度:', this.progress);
    }
    
    loadProgress() {
        try {
            const saved = localStorage.getItem(this.storageKey);
            if (saved) {
                return JSON.parse(saved);
            }
        } catch (error) {
            console.error('加载进度失败:', error);
        }
        
        return this.getDefaultProgress();
    }
    
    getDefaultProgress() {
        return {
            lastStudyDate: null,
            totalStudyTime: 0,
            charactersLearned: {},
            quizResults: [],
            chapterProgress: {},
            streakDays: 0,
            lastStudyStreakDate: null
        };
    }
    
    saveProgress() {
        try {
            localStorage.setItem(this.storageKey, JSON.stringify(this.progress));
            console.log('进度已保存');
        } catch (error) {
            console.error('保存进度失败:', error);
        }
    }
    
    markCharacterLearned(char, chapter) {
        const today = new Date().toDateString();
        
        if (!this.progress.charactersLearned[char]) {
            this.progress.charactersLearned[char] = {
                firstLearned: today,
                lastReviewed: today,
                reviewCount: 1,
                chapter: chapter
            };
        } else {
            this.progress.charactersLearned[char].lastReviewed = today;
            this.progress.charactersLearned[char].reviewCount++;
        }
        
        this.updateChapterProgress(chapter);
        this.updateStudyStreak();
        this.saveProgress();
    }
    
    updateChapterProgress(chapter) {
        if (!this.progress.chapterProgress[chapter]) {
            this.progress.chapterProgress[chapter] = {
                totalCharacters: 0,
                learnedCharacters: 0,
                lastStudyDate: null
            };
        }
        
        this.progress.chapterProgress[chapter].lastStudyDate = new Date().toDateString();
    }
    
    updateStudyStreak() {
        const today = new Date().toDateString();
        const lastDate = this.progress.lastStudyStreakDate;
        
        if (lastDate) {
            const lastDateObj = new Date(lastDate);
            const todayObj = new Date(today);
            const diffDays = Math.floor((todayObj - lastDateObj) / (1000 * 60 * 60 * 24));
            
            if (diffDays === 1) {
                this.progress.streakDays++;
            } else if (diffDays > 1) {
                this.progress.streakDays = 1;
            }
        } else {
            this.progress.streakDays = 1;
        }
        
        this.progress.lastStudyStreakDate = today;
    }
    
    recordQuizResult(quizData) {
        const result = {
            date: new Date().toISOString(),
            chapter: quizData.chapter,
            questionCount: quizData.total,
            correctCount: quizData.correct,
            wrongCount: quizData.wrong,
            percentage: Math.round((quizData.correct / quizData.total) * 100),
            wrongAnswers: quizData.wrongAnswers || []
        };
        
        this.progress.quizResults.push(result);
        
        if (this.progress.quizResults.length > 100) {
            this.progress.quizResults = this.progress.quizResults.slice(-100);
        }
        
        this.saveProgress();
    }
    
    getChapterProgress(chapter) {
        return this.progress.chapterProgress[chapter] || {
            totalCharacters: 0,
            learnedCharacters: 0,
            lastStudyDate: null
        };
    }
    
    getCharacterProgress(char) {
        return this.progress.charactersLearned[char] || null;
    }
    
    getRecentQuizResults(limit = 10) {
        return this.progress.quizResults.slice(-limit).reverse();
    }
    
    getStatistics() {
        const totalCharacters = Object.keys(this.progress.charactersLearned).length;
        const totalReviews = Object.values(this.progress.charactersLearned)
            .reduce((sum, char) => sum + char.reviewCount, 0);
        
        const recentQuizzes = this.getRecentQuizResults(10);
        const avgScore = recentQuizzes.length > 0
            ? Math.round(recentQuizzes.reduce((sum, q) => sum + q.percentage, 0) / recentQuizzes.length)
            : 0;
        
        return {
            totalCharacters,
            totalReviews,
            streakDays: this.progress.streakDays,
            totalQuizzes: this.progress.quizResults.length,
            avgScore,
            lastStudyDate: this.progress.lastStudyStreakDate
        };
    }
    
    getCharactersNeedingReview() {
        const today = new Date();
        const charactersToReview = [];
        
        for (const [char, data] of Object.entries(this.progress.charactersLearned)) {
            const lastReviewed = new Date(data.lastReviewed);
            const daysSinceReview = Math.floor((today - lastReviewed) / (1000 * 60 * 60 * 24));
            
            const reviewInterval = this.getReviewInterval(data.reviewCount);
            
            if (daysSinceReview >= reviewInterval) {
                charactersToReview.push({
                    char,
                    daysSinceReview,
                    reviewCount: data.reviewCount,
                    chapter: data.chapter
                });
            }
        }
        
        return charactersToReview.sort((a, b) => b.daysSinceReview - a.daysSinceReview);
    }
    
    getReviewInterval(reviewCount) {
        const intervals = [1, 3, 7, 14, 30, 60, 90];
        const index = Math.min(reviewCount - 1, intervals.length - 1);
        return intervals[index];
    }
    
    exportProgress() {
        const dataStr = JSON.stringify(this.progress, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = `cantonese_progress_${new Date().toISOString().split('T')[0]}.json`;
        link.click();
        
        URL.revokeObjectURL(url);
    }
    
    importProgress(jsonData) {
        try {
            const imported = JSON.parse(jsonData);
            this.progress = imported;
            this.saveProgress();
            console.log('进度导入成功');
            return true;
        } catch (error) {
            console.error('进度导入失败:', error);
            return false;
        }
    }
    
    resetProgress() {
        if (confirm('确定要重置所有学习进度吗？此操作不可撤销。')) {
            this.progress = this.getDefaultProgress();
            this.saveProgress();
            console.log('进度已重置');
            return true;
        }
        return false;
    }
}

window.progressTracker = new ProgressTracker();
