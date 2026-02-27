const fs = require('fs');
const path = require('path');

// 多音字例词数据库
const polyphoneExamples = {
    "和": {
        primary: ["和平", "和谐", "和你"],
        secondary: ["暖和", "和面", "和稀泥"]
    },
    "中": {
        primary: ["中国", "中间", "中心"],
        secondary: ["中奖", "中暑", "中毒"]
    },
    "好": {
        primary: ["好人", "好事", "好看"],
        secondary: ["好学", "好强", "好胜"]
    },
    "着": {
        primary: ["看着", "听着", "说着"],
        secondary: ["穿着", "着装", "着陆"]
    },
    "地": {
        primary: ["地方", "地球", "地面"],
        secondary: ["慢慢地", "轻轻地", "悄悄地"]
    },
    "得": {
        primary: ["得到", "得分", "得体"],
        secondary: ["跑得快", "做得好", "说得对"]
    },
    "只": {
        primary: ["只有", "只是", "只要"],
        secondary: ["一只", "只身", "只言片语"]
    },
    "长": {
        primary: ["长度", "长期", "长河"],
        secondary: ["长大", "长高", "成长"]
    },
    "间": {
        primary: ["房间", "时间", "中间"],
        secondary: ["间隔", "间隙", "间断"]
    },
    "便": {
        primary: ["便利", "方便", "便捷"],
        secondary: ["便宜", "便便", "便饭"]
    },
    "发": {
        primary: ["发展", "发生", "发现"],
        secondary: ["头发", "毛发", "发型"]
    },
    "行": {
        primary: ["行动", "行业", "行走"],
        secondary: ["银行", "行列", "行距"]
    },
    "少": {
        primary: ["少数", "少年", "少女"],
        secondary: ["多少", "减少", "缺少"]
    },
    "相": {
        primary: ["相信", "相互", "相处"],
        secondary: ["相貌", "相片", "长相"]
    },
    "重": {
        primary: ["重要", "重量", "重点"],
        secondary: ["重复", "重新", "重叠"]
    },
    "数": {
        primary: ["数字", "数学", "数量"],
        secondary: ["数数", "数不胜数", "数不清"]
    },
    "乐": {
        primary: ["快乐", "乐意", "乐事"],
        secondary: ["音乐", "乐器", "乐章"]
    },
    "空": {
        primary: ["空气", "空间", "空中"],
        secondary: ["空白", "空闲", "空地"]
    },
    "色": {
        primary: ["颜色", "色彩", "色调"],
        secondary: ["色子", "掉色", "褪色"]
    },
    "角": {
        primary: ["角落", "角度", "角色"],
        secondary: ["牛角", "羊角", "角落"]
    },
    "折": {
        primary: ["折断", "折扣", "折叠"],
        secondary: ["折本", "折耗", "折损"]
    },
    "调": {
        primary: ["调查", "调动", "调整"],
        secondary: ["音调", "声调", "语调"]
    },
    "种": {
        primary: ["种子", "种类", "种植"],
        secondary: ["种地", "种花", "种树"]
    },
    "还": {
        primary: ["还有", "还是", "还原"],
        secondary: ["归还", "偿还", "还书"]
    },
    "分": {
        primary: ["分数", "分开", "分手"],
        secondary: ["分量", "分外", "分内"]
    },
    "背": {
        primary: ["背部", "背景", "背后"],
        secondary: ["背包", "背带", "背负"]
    },
    "处": {
        primary: ["处理", "处分", "处罚"],
        secondary: ["到处", "处所", "住处"]
    },
    "当": {
        primary: ["当然", "当时", "当下"],
        secondary: ["上当", "当铺", "当票"]
    },
    "倒": {
        primary: ["倒立", "倒下", "倒霉"],
        secondary: ["倒车", "倒数", "倒转"]
    },
    "都": {
        primary: ["都是", "都会", "首都"],
        secondary: ["都市", "都会", "都城"]
    },
    "度": {
        primary: ["温度", "度数", "度过"],
        secondary: ["揣度", "忖度", "测度"]
    },
    "恶": {
        primary: ["恶劣", "恶毒", "恶习"],
        secondary: ["恶心", "厌恶", "憎恶"]
    },
    "否": {
        primary: ["否定", "否则", "否决"],
        secondary: ["是否", "能否", "与否"]
    },
    "父": {
        primary: ["父亲", "父母", "父子"],
        secondary: ["祖父", "伯父", "叔父"]
    },
    "盖": {
        primary: ["盖子", "盖章", "覆盖"],
        secondary: ["华盖", "盖饭", "盖浇饭"]
    },
    "干": {
        primary: ["干净", "干涉", "干燥"],
        secondary: ["干部", "干练", "干劲"]
    },
    "岗": {
        primary: ["岗位", "岗亭", "岗哨"],
        secondary: ["山岗", "岗峦", "岗子"]
    },
    "港": {
        primary: ["香港", "港口", "港湾"],
        secondary: ["港币", "港商", "港人"]
    },
    "高": {
        primary: ["高兴", "高度", "高分"],
        secondary: ["高见", "高明", "高尚"]
    },
    "告": {
        primary: ["告诉", "告别", "告发"],
        secondary: ["广告", "告急", "告捷"]
    },
    "革": {
        primary: ["革命", "改革", "革新"],
        secondary: ["皮革", "革履", "革职"]
    },
    "格": {
        primary: ["格子", "格式", "格局"],
        secondary: ["格杀", "格物", "格致"]
    },
    "隔": {
        primary: ["隔离", "隔断", "隔阂"],
        secondary: ["隔壁", "隔日", "隔年"]
    },
    "个": {
        primary: ["个人", "个别", "个性"],
        secondary: ["个子", "个别", "个体"]
    },
    "各": {
        primary: ["各个", "各自", "各种"],
        secondary: ["各位", "各界", "各方面"]
    },
    "给": {
        primary: ["给予", "给你", "给我"],
        secondary: ["送给", "交给", "献给"]
    },
    "根": {
        primary: ["根本", "根据", "根源"],
        secondary: ["树根", "草根", "牙根"]
    },
    "更": {
        primary: ["更加", "更好", "更大"],
        secondary: ["更改", "更换", "更新"]
    },
    "工": {
        primary: ["工人", "工作", "工厂"],
        secondary: ["工程", "工地", "工艺"]
    },
    "公": {
        primary: ["公共", "公平", "公开"],
        secondary: ["公园", "公司", "公路"]
    },
    "功": {
        primary: ["功劳", "功绩", "功夫"],
        secondary: ["功能", "功效", "功力"]
    },
    "攻": {
        primary: ["攻击", "攻打", "攻克"],
        secondary: ["攻势", "攻占", "攻心"]
    },
    "供": {
        primary: ["供应", "供给", "供求"],
        secondary: ["供养", "供品", "供认"]
    },
    "共": {
        primary: ["共同", "共有", "共享"],
        secondary: ["总共", "共计", "共存"]
    },
    "构": {
        primary: ["结构", "构造", "构建"],
        secondary: ["构思", "构想", "构图"]
    },
    "购": {
        primary: ["购买", "购物", "采购"],
        secondary: ["购置", "购销", "购办"]
    },
    "够": {
        primary: ["足够", "够格", "够味"],
        secondary: ["够本", "够劲", "够意思"]
    },
    "估": {
        primary: ["估计", "估量", "估价"],
        secondary: ["估摸", "估算", "估测"]
    },
    "古": {
        primary: ["古代", "古老", "古董"],
        secondary: ["古文", "古诗", "古典"]
    },
    "谷": {
        primary: ["山谷", "谷物", "谷底"],
        secondary: ["稻谷", "谷子", "谷粒"]
    },
    "骨": {
        primary: ["骨头", "骨气", "骨架"],
        secondary: ["骨碌", "骨朵", "骨牌"]
    },
    "故": {
        primary: ["故事", "故乡", "故意"],
        secondary: ["故障", "故友", "故土"]
    },
    "固": {
        primary: ["固定", "固执", "固体"],
        secondary: ["稳固", "坚固", "牢固"]
    },
    "顾": {
        primary: ["照顾", "顾客", "顾虑"],
        secondary: ["顾念", "顾惜", "顾全"]
    },
    "瓜": {
        primary: ["西瓜", "南瓜", "黄瓜"],
        secondary: ["瓜分", "瓜葛", "瓜熟蒂落"]
    },
    "刮": {
        primary: ["刮风", "刮脸", "刮擦"],
        secondary: ["刮目", "刮削", "刮地皮"]
    },
    "关": {
        primary: ["关心", "关注", "关于"],
        secondary: ["关门", "关灯", "关卡"]
    },
    "官": {
        primary: ["官员", "官场", "官职"],
        secondary: ["官方", "官府", "官邸"]
    },
    "冠": {
        primary: ["冠军", "冠冕", "皇冠"],
        secondary: ["鸡冠", "树冠", "花冠"]
    },
    "光": {
        primary: ["光明", "光线", "光芒"],
        secondary: ["光荣", "光临", "光顾"]
    },
    "广": {
        primary: ["广大", "广泛", "广阔"],
        secondary: ["广场", "广告", "广播"]
    },
    "归": {
        primary: ["归还", "归来", "归属"],
        secondary: ["归纳", "归顺", "归降"]
    },
    "龟": {
        primary: ["乌龟", "海龟", "龟壳"],
        secondary: ["龟缩", "龟甲", "龟龄"]
    },
    "规": {
        primary: ["规定", "规矩", "规则"],
        secondary: ["规划", "规范", "规劝"]
    },
    "轨": {
        primary: ["轨道", "铁轨", "轨迹"],
        secondary: ["轨范", "轨制", "轨辙"]
    },
    "鬼": {
        primary: ["鬼神", "鬼怪", "鬼魂"],
        secondary: ["鬼祟", "鬼混", "鬼话"]
    },
    "贵": {
        primary: ["贵重", "贵族", "贵姓"],
        secondary: ["宝贵", "珍贵", "可贵"]
    },
    "桂": {
        primary: ["桂花", "桂林", "桂皮"],
        secondary: ["桂冠", "桂树", "桂圆"]
    },
    "滚": {
        primary: ["滚动", "滚开", "滚蛋"],
        secondary: ["滚筒", "滚圆", "滚雪球"]
    },
    "国": {
        primary: ["国家", "国际", "国产"],
        secondary: ["祖国", "祖国", "国民"]
    },
    "果": {
        primary: ["水果", "果实", "果然"],
        secondary: ["结果", "效果", "成果"]
    },
    "过": {
        primary: ["过去", "过来", "过年"],
        secondary: ["过错", "过程", "过渡"]
    }
};

// 读取所有章节的汉字数据
function readAllChapters() {
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

// 筛选多音字
function filterPolyphones(characters) {
    return characters.filter(char => char.secondary_jyutping && char.secondary_jyutping !== '');
}

// 为多音字添加例词
function addExamples(polyphones) {
    return polyphones.map(char => {
        const examples = polyphoneExamples[char.char] || {
            primary: ["暂无例词", "暂无例词", "暂无例词"],
            secondary: ["暂无例词", "暂无例词", "暂无例词"]
        };
        return {
            ...char,
            examples
        };
    });
}

// 按频率排序
function sortByFrequency(polyphones) {
    return polyphones.sort((a, b) => (a.frequency_rank || 99999) - (b.frequency_rank || 99999));
}

// 生成章节数据
function generateChapterData(polyphones) {
    return {
        id: 11,
        title: "多音字专栏",
        start_rank: 1,
        end_rank: polyphones.length,
        char_count: polyphones.length
    };
}

// 主函数
function main() {
    console.log('开始生成多音字章节数据...');
    
    // 读取所有章节数据
    const allCharacters = readAllChapters();
    console.log(`读取到 ${allCharacters.length} 个汉字`);
    
    // 筛选多音字
    const polyphones = filterPolyphones(allCharacters);
    console.log(`筛选出 ${polyphones.length} 个多音字`);
    
    // 添加例词
    const polyphonesWithExamples = addExamples(polyphones);
    
    // 按频率排序
    const sortedPolyphones = sortByFrequency(polyphonesWithExamples);
    
    // 生成章节11的数据文件
    const chapter11Path = path.join(__dirname, 'data', 'chapter_11_characters.json');
    fs.writeFileSync(chapter11Path, JSON.stringify(sortedPolyphones, null, 2));
    console.log(`生成章节11数据文件: ${chapter11Path}`);
    
    // 更新chapters.json文件
    const chaptersPath = path.join(__dirname, 'data', 'chapters.json');
    const chapters = JSON.parse(fs.readFileSync(chaptersPath, 'utf8'));
    
    // 检查是否已存在章节11
    const chapter11Exists = chapters.some(chapter => chapter.id === 11);
    
    if (chapter11Exists) {
        // 更新现有章节11
        chapters.forEach(chapter => {
            if (chapter.id === 11) {
                chapter.char_count = sortedPolyphones.length;
                chapter.end_rank = sortedPolyphones.length;
            }
        });
    } else {
        // 添加新章节11
        const chapter11 = generateChapterData(sortedPolyphones);
        chapters.push(chapter11);
    }
    
    fs.writeFileSync(chaptersPath, JSON.stringify(chapters, null, 2));
    console.log(`更新章节配置文件: ${chaptersPath}`);
    
    console.log('✅ 多音字章节数据生成完成！');
    console.log(`生成的多音字数量: ${sortedPolyphones.length}`);
    console.log(`章节11路径: ${chapter11Path}`);
    
    // 显示前10个多音字
    console.log('\n前10个多音字:');
    sortedPolyphones.slice(0, 10).forEach((char, index) => {
        console.log(`${index + 1}. ${char.char} - ${char.jyutping} / ${char.secondary_jyutping}`);
    });
}

// 执行主函数
main();
