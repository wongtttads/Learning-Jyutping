// 验证第11章节多音字数据的完整性
const fs = require('fs');
const path = require('path');

// 读取第11章节数据
function readChapter11Data() {
  const filePath = path.join(__dirname, 'data', 'chapter_11_characters.json');
  if (fs.existsSync(filePath)) {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  }
  return [];
}

// 验证每个多音字的数据完整性
function verifyPolyphoneData(polyphones) {
  const issues = [];
  
  polyphones.forEach((polyphone, index) => {
    console.log(`\n验证第 ${index + 1} 个多音字: ${polyphone.char}`);
    
    // 检查基本信息
    if (!polyphone.char) {
      issues.push(`${polyphone.char || '未知字符'}: 缺少字符`);
    }
    
    if (!polyphone.jyutping) {
      issues.push(`${polyphone.char}: 缺少主要读音`);
    }
    
    if (!polyphone.secondary_jyutping) {
      issues.push(`${polyphone.char}: 缺少次要读音`);
    }
    
    // 检查示例
    if (!polyphone.examples) {
      issues.push(`${polyphone.char}: 缺少示例`);
    } else {
      if (!polyphone.examples.primary || polyphone.examples.primary.length < 3) {
        issues.push(`${polyphone.char}: 主要读音示例不足3个`);
      }
      
      if (!polyphone.examples.secondary || polyphone.examples.secondary.length < 3) {
        issues.push(`${polyphone.char}: 次要读音示例不足3个`);
      }
    }
    
    // 检查释义
    if (!polyphone.definitions) {
      issues.push(`${polyphone.char}: 缺少释义`);
    } else {
      if (!polyphone.definitions.primary) {
        issues.push(`${polyphone.char}: 缺少主要读音释义`);
      } else if (polyphone.definitions.primary.length > 20) {
        issues.push(`${polyphone.char}: 主要读音释义超过20字`);
      }
      
      if (!polyphone.definitions.secondary) {
        issues.push(`${polyphone.char}: 缺少次要读音释义`);
      } else if (polyphone.definitions.secondary.length > 20) {
        issues.push(`${polyphone.char}: 次要读音释义超过20字`);
      }
    }
  });
  
  return issues;
}

// 主函数
function main() {
  console.log('开始验证第11章节多音字数据的完整性...');
  
  const polyphones = readChapter11Data();
  console.log(`共验证 ${polyphones.length} 个多音字`);
  
  const issues = verifyPolyphoneData(polyphones);
  
  if (issues.length === 0) {
    console.log('\n✅ 所有多音字数据完整，符合要求！');
  } else {
    console.log('\n❌ 发现以下问题：');
    issues.forEach(issue => {
      console.log(`- ${issue}`);
    });
  }
  
  // 保存验证结果
  const result = {
    totalPolyphones: polyphones.length,
    issues: issues,
    hasIssues: issues.length > 0
  };
  
  fs.writeFileSync(
    path.join(__dirname, 'polyphone_verification.json'),
    JSON.stringify(result, null, 2),
    'utf8'
  );
  
  console.log('\n验证结果已保存到 polyphone_verification.json');
}

// 运行主函数
main();
