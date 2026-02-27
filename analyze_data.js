const fs = require('fs');
const path = require('path');

// 分析数据结构，检查是否存在双重粤拼标注
function analyzeData() {
    const dataDir = path.join(__dirname, 'data');
    const chapterFiles = fs.readdirSync(dataDir).filter(file => file.startsWith('chapter_') && file.endsWith('_characters.json'));
    
    console.log('开始分析数据结构...');
    console.log(`找到 ${chapterFiles.length} 个章节文件`);
    
    let totalCharacters = 0;
    let charactersWithDualJyutping = 0;
    let sampleCharacters = [];
    let errorFiles = [];
    
    chapterFiles.forEach(chapterFile => {
        const filePath = path.join(dataDir, chapterFile);
        try {
            const content = fs.readFileSync(filePath, 'utf8');
            const characters = JSON.parse(content);
            
            if (Array.isArray(characters)) {
                totalCharacters += characters.length;
                
                characters.forEach(char => {
                    // 检查是否存在双重粤拼标注
                    if (char.secondary_jyutping || char.jyutping2) {
                        charactersWithDualJyutping++;
                        sampleCharacters.push({
                            char: char.char,
                            primary_jyutping: char.jyutping,
                            secondary_jyutping: char.secondary_jyutping || char.jyutping2
                        });
                    }
                });
            }
        } catch (error) {
            console.log(`错误文件: ${chapterFile}`);
            errorFiles.push(chapterFile);
        }
    });
    
    console.log(`\n分析结果：`);
    console.log(`总汉字数：${totalCharacters}`);
    console.log(`存在双重粤拼标注的汉字数：${charactersWithDualJyutping}`);
    
    if (errorFiles.length > 0) {
        console.log(`\n错误文件：`);
        errorFiles.forEach(file => console.log(file));
    }
    
    if (charactersWithDualJyutping > 0) {
        console.log(`\n典型案例：`);
        sampleCharacters.slice(0, 10).forEach(item => {
            console.log(`${item.char}: ${item.primary_jyutping} / ${item.secondary_jyutping}`);
        });
    } else {
        console.log('\n未发现双重粤拼标注，需要添加secondary_jyutping字段');
    }
    
    return {
        totalCharacters,
        charactersWithDualJyutping,
        sampleCharacters,
        errorFiles
    };
}

// 运行分析
analyzeData();
