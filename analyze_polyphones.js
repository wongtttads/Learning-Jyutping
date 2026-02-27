// 分析所有章节的字符，识别可能的多音字
const fs = require('fs');
const path = require('path');

// 读取所有章节的字符数据
function readChapterData() {
  const chapters = [];
  for (let i = 1; i <= 10; i++) {
    const filePath = path.join(__dirname, 'data', `chapter_${i}_characters.json`);
    if (fs.existsSync(filePath)) {
      const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
      chapters.push(...data);
    }
  }
  return chapters;
}

// 分析字符，识别可能的多音字
function analyzePolyphones(characters) {
  // 存储所有字符及其可能的读音
  const charPronunciations = new Map();
  
  characters.forEach(charData => {
    const char = charData.char;
    if (!charPronunciations.has(char)) {
      charPronunciations.set(char, new Set());
    }
    
    // 添加主要读音
    if (charData.jyutping) {
      charPronunciations.get(char).add(charData.jyutping);
    }
    
    // 添加次要读音
    if (charData.secondary_jyutping && charData.secondary_jyutping !== "") {
      charPronunciations.get(char).add(charData.secondary_jyutping);
    }
  });
  
  // 识别多音字（有多个读音的字符）
  const polyphones = [];
  charPronunciations.forEach((pronunciations, char) => {
    if (pronunciations.size > 1) {
      polyphones.push({
        character: char,
        pronunciations: Array.from(pronunciations)
      });
    }
  });
  
  return polyphones;
}

// 读取现有的第11章节数据
function readChapter11Data() {
  const filePath = path.join(__dirname, 'data', 'chapter_11_characters.json');
  if (fs.existsSync(filePath)) {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  }
  return [];
}

// 比较并找出需要补充的多音字
function findMissingPolyphones(identifiedPolyphones, existingPolyphones) {
  const existingChars = new Set(existingPolyphones.map(item => item.char));
  return identifiedPolyphones.filter(polyphone => !existingChars.has(polyphone.character));
}

// 主函数
function main() {
  console.log('开始分析所有章节的字符...');
  
  // 读取所有章节数据
  const allCharacters = readChapterData();
  console.log(`共读取 ${allCharacters.length} 个字符`);
  
  // 识别多音字
  const identifiedPolyphones = analyzePolyphones(allCharacters);
  console.log(`识别出 ${identifiedPolyphones.length} 个多音字`);
  
  // 读取现有的第11章节数据
  const existingPolyphones = readChapter11Data();
  console.log(`第11章节现有 ${existingPolyphones.length} 个多音字`);
  
  // 找出需要补充的多音字
  const missingPolyphones = findMissingPolyphones(identifiedPolyphones, existingPolyphones);
  console.log(`需要补充 ${missingPolyphones.length} 个多音字`);
  
  // 输出结果
  console.log('\n识别出的多音字：');
  identifiedPolyphones.forEach(polyphone => {
    console.log(`${polyphone.character}: ${polyphone.pronunciations.join(', ')}`);
  });
  
  console.log('\n需要补充的多音字：');
  missingPolyphones.forEach(polyphone => {
    console.log(`${polyphone.character}: ${polyphone.pronunciations.join(', ')}`);
  });
  
  // 保存结果到文件
  const result = {
    totalCharacters: allCharacters.length,
    identifiedPolyphones: identifiedPolyphones.length,
    existingPolyphones: existingPolyphones.length,
    missingPolyphones: missingPolyphones.length,
    polyphones: identifiedPolyphones,
    missing: missingPolyphones
  };
  
  fs.writeFileSync(
    path.join(__dirname, 'polyphone_analysis.json'),
    JSON.stringify(result, null, 2),
    'utf8'
  );
  
  console.log('\n分析结果已保存到 polyphone_analysis.json');
}

// 运行主函数
main();
