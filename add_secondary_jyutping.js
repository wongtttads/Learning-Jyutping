const fs = require('fs');
const path = require('path');

// 常见多音字的双重粤拼
const multiPronunciationChars = {
    "行": ["haang4", "hong4"],
    "好": ["hou2", "hou3"],
    "中": ["zung1", "zung3"],
    "长": ["coeng4", "zoeng2"],
    "乐": ["lok6", "ngok6"],
    "发": ["faat3", "faat1"],
    "相": ["soeng1", "seong3"],
    "少": ["siu2", "siu3"],
    "重": ["cung4", "cung5"],
    "间": ["gaan1", "gaan3"],
    "便": ["bin6", "pin4"],
    "行": ["haang4", "hong4"],
    "数": ["sou3", "suk6"],
    "只": ["zi2", "zek3"],
    "着": ["zoek6", "zyu3"],
    "地": ["dei6", "di6"],
    "得": ["dak1", "dak6"],
    "和": ["wo4", "wo6"]
};

// 为每个汉字添加secondary_jyutping字段
function addSecondaryJyutping() {
    const dataDir = path.join(__dirname, 'data');
    const chapterFiles = fs.readdirSync(dataDir).filter(file => file.startsWith('chapter_') && file.endsWith('_characters.json'));
    
    console.log('开始添加secondary_jyutping字段...');
    
    chapterFiles.forEach(chapterFile => {
        const filePath = path.join(dataDir, chapterFile);
        try {
            const content = fs.readFileSync(filePath, 'utf8');
            const characters = JSON.parse(content);
            
            if (Array.isArray(characters)) {
                const updatedCharacters = characters.map(char => {
                    // 如果是多音字，添加secondary_jyutping
                    if (multiPronunciationChars[char.char]) {
                        const pronunciations = multiPronunciationChars[char.char];
                        // 确保primary pronunciation是第一个，secondary是第二个
                        if (char.jyutping === pronunciations[0]) {
                            return {
                                ...char,
                                secondary_jyutping: pronunciations[1]
                            };
                        } else if (char.jyutping === pronunciations[1]) {
                            return {
                                ...char,
                                secondary_jyutping: pronunciations[0]
                            };
                        } else {
                            // 如果当前发音不在预期列表中，添加第一个作为secondary
                            return {
                                ...char,
                                secondary_jyutping: pronunciations[0]
                            };
                        }
                    } else {
                        // 对于非多音字，暂时设为空
                        return {
                            ...char,
                            secondary_jyutping: ""
                        };
                    }
                });
                
                // 写回文件
                fs.writeFileSync(filePath, JSON.stringify(updatedCharacters, null, 2), 'utf8');
                console.log(`已更新文件: ${chapterFile}`);
            }
        } catch (error) {
            console.log(`错误处理文件: ${chapterFile}`);
            console.log(error.message);
        }
    });
    
    console.log('\n添加secondary_jyutping字段完成');
}

// 运行脚本
addSecondaryJyutping();
