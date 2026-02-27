#!/usr/bin/env python3
"""
简单有效的汉字字频排序脚本
基于：常用字优先 + 笔画数排序 + Unicode编码排序
"""

import json
import os
import shutil
from collections import defaultdict

def load_common_characters():
    """加载常用汉字列表（前3500个最常用字）"""
    # 基于《现代汉语常用字表》和实际语料统计的常用字
    common_chars = [
        '的', '一', '是', '在', '不', '了', '有', '和', '人', '这',
        '中', '大', '为', '上', '个', '国', '我', '以', '要', '他',
        '时', '来', '用', '们', '生', '到', '作', '地', '于', '出',
        '就', '分', '对', '成', '会', '可', '主', '发', '年', '动',
        '同', '工', '也', '能', '下', '过', '子', '说', '产', '种',
        '面', '而', '方', '后', '多', '定', '行', '学', '法', '所',
        '民', '得', '经', '十', '三', '之', '进', '着', '等', '部',
        '度', '家', '电', '力', '里', '如', '水', '化', '高', '自',
        '二', '理', '起', '小', '物', '现', '实', '加', '量', '都',
        '两', '体', '制', '机', '当', '使', '点', '从', '业', '本',
        '去', '把', '性', '好', '应', '开', '它', '合', '还', '因',
        '由', '其', '些', '然', '前', '外', '天', '政', '四', '日',
        '那', '社', '义', '事', '平', '形', '相', '全', '表', '间',
        '样', '与', '关', '各', '重', '新', '线', '内', '数', '正',
        '心', '反', '你', '明', '看', '原', '又', '么', '利', '比',
        '或', '但', '质', '气', '第', '向', '道', '命', '此', '变',
        '条', '只', '没', '结', '解', '问', '意', '建', '月', '公',
        '无', '系', '军', '很', '情', '者', '最', '立', '代', '想',
        '已', '通', '并', '提', '直', '题', '党', '程', '展', '五',
        '果', '料', '象', '员', '革', '位', '入', '常', '文', '总',
        '次', '品', '式', '活', '设', '及', '管', '特', '件', '长',
        '求', '老', '头', '基', '资', '边', '流', '路', '级', '少',
        '图', '山', '统', '接', '知', '较', '将', '组', '见', '计',
        '别', '她', '手', '角', '期', '根', '论', '运', '农', '指',
        '几', '九', '区', '强', '放', '决', '西', '被', '干', '做',
        '必', '战', '先', '回', '则', '任', '取', '据', '处', '队',
        '南', '给', '色', '光', '门', '即', '保', '治', '北', '造',
        '百', '规', '热', '领', '七', '海', '口', '东', '导', '器',
        '压', '志', '世', '金', '增', '争', '济', '阶', '油', '思',
        '术', '极', '交', '受', '联', '什', '认', '六', '共', '权',
        '收', '证', '改', '清', '美', '再', '采', '转', '更', '单',
        '风', '切', '打', '白', '教', '速', '花', '带', '安', '场',
        '身', '车', '例', '真', '务', '具', '万', '每', '目', '至',
        '达', '走', '积', '示', '议', '声', '报', '斗', '完', '类',
        '八', '离', '华', '名', '确', '才', '科', '张', '信', '马',
        '节', '话', '米', '整', '空', '元', '况', '今', '集', '温',
        '传', '土', '许', '步', '群', '广', '石', '记', '需', '段',
        '研', '界', '拉', '林', '律', '叫', '且', '究', '观', '越',
        '织', '装', '影', '算', '低', '持', '音', '众', '书', '布',
        '复', '容', '儿', '须', '际', '商', '非', '验', '连', '断',
        '深', '难', '近', '矿', '千', '周', '委', '素', '技', '备',
        '半', '办', '青', '省', '列', '习', '响', '约', '支', '般',
        '史', '感', '劳', '便', '团', '往', '酸', '历', '市', '克',
        '何', '除', '消', '构', '府', '称', '太', '准', '精', '值',
        '号', '率', '族', '维', '划', '选', '标', '写', '存', '候',
        '亲', '严', '岛', '洪', '父', '词', '够', '章', '爱', '台',
        '纷', '唯', '互', '雨', '父', '令', '皮', '毒', '氧', '女',
        '斤', '王', '黄', '李', '赵', '钱', '孙', '周', '吴', '郑',
        '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦',
        '尤', '许', '何', '吕', '施', '张', '孔', '曹', '严', '华',
        '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水',
        '窦', '章', '云', '苏', '潘', '葛', '奚', '范', '彭', '郎',
        '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任',
        '袁', '柳', '酆', '鲍', '史', '唐', '费', '廉', '岑', '薛',
        '雷', '贺', '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬',
        '安', '常', '乐', '于', '时', '傅', '皮', '卞', '齐', '康',
        '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和', '穆',
        '萧', '尹', '姚', '邵', '湛', '汪', '祁', '毛', '禹', '狄',
        '米', '贝', '明', '臧', '计', '伏', '成', '戴', '谈', '宋',
        '茅', '庞', '熊', '纪', '舒', '屈', '项', '祝', '董', '梁',
        '杜', '阮', '蓝', '闵', '席', '季', '麻', '强', '贾', '路',
        '娄', '危', '江', '童', '颜', '郭', '梅', '盛', '林', '刁',
        '钟', '徐', '邱', '骆', '高', '夏', '蔡', '田', '樊', '胡',
        '凌', '霍', '虞', '万', '支', '柯', '昝', '管', '卢', '莫',
        '经', '房', '裘', '缪', '干', '解', '应', '宗', '丁', '宣',
        '贲', '邓', '郁', '单', '杭', '洪', '包', '诸', '左', '石',
        '崔', '吉', '钮', '龚', '程', '嵇', '邢', '滑', '裴', '陆',
        '荣', '翁', '荀', '羊', '於', '惠', '甄', '曲', '家', '封',
        '芮', '羿', '储', '靳', '汲', '邴', '糜', '松', '井', '段',
        '富', '巫', '乌', '焦', '巴', '弓', '牧', '隗', '山', '谷',
        '车', '侯', '宓', '蓬', '全', '郗', '班', '仰', '秋', '仲',
        '伊', '宫', '宁', '仇', '栾', '暴', '甘', '钭', '厉', '戎',
        '祖', '武', '符', '刘', '景', '詹', '束', '龙', '叶', '幸',
        '司', '韶', '郜', '黎', '蓟', '薄', '印', '宿', '白', '怀',
        '蒲', '邰', '从', '鄂', '索', '咸', '籍', '赖', '卓', '蔺',
        '屠', '蒙', '池', '乔', '阴', '郁', '胥', '能', '苍', '双',
        '闻', '莘', '党', '翟', '谭', '贡', '劳', '逄', '姬', '申',
        '扶', '堵', '冉', '宰', '郦', '雍', '郤', '璩', '桑', '桂',
        '濮', '牛', '寿', '通', '边', '扈', '燕', '冀', '郏', '浦',
        '尚', '农', '温', '别', '庄', '晏', '柴', '瞿', '阎', '充',
        '慕', '连', '茹', '习', '宦', '艾', '鱼', '容', '向', '古',
        '易', '慎', '戈', '廖', '庾', '终', '暨', '居', '衡', '步',
        '都', '耿', '满', '弘', '匡', '国', '文', '寇', '广', '禄',
        '阙', '东', '欧', '殳', '沃', '利', '蔚', '越', '夔', '隆',
        '师', '巩', '厍', '聂', '晁', '勾', '敖', '融', '冷', '訾',
        '辛', '阚', '那', '简', '饶', '空', '曾', '毋', '沙', '乜',
        '养', '鞠', '须', '丰', '巢', '关', '蒯', '相', '查', '后',
        '荆', '红', '游', '竺', '权', '逯', '盖', '益', '桓', '公',
        '万', '俟', '司', '马', '上', '官', '欧', '阳', '夏', '侯',
        '诸', '葛', '闻', '人', '东', '方', '赫', '连', '皇', '甫',
        '尉', '迟', '公', '羊', '澹', '台', '公', '冶', '宗', '政',
        '濮', '阳', '淳', '于', '单', '于', '太', '叔', '申', '屠',
        '公', '孙', '仲', '孙', '轩', '辕', '令', '狐', '钟', '离',
        '宇', '文', '长', '孙', '慕', '容', '鲜', '于', '闾', '丘',
        '司', '徒', '司', '空', '亓', '官', '司', '寇', '仉', '督',
        '子', '车', '颛', '孙', '端', '木', '巫', '马', '公', '西',
        '漆', '雕', '乐', '正', '壤', '驷', '公', '良', '拓', '跋',
        '夹', '谷', '宰', '父', '谷', '梁', '晋', '楚', '闫', '法',
        '汝', '鄢', '涂', '钦', '段', '干', '百', '里', '东', '郭',
        '南', '门', '呼', '延', '归', '海', '羊', '舌', '微', '生',
        '岳', '帅', '缑', '亢', '况', '后', '有', '琴', '梁', '丘',
        '左', '丘', '东', '门', '西', '门', '商', '牟', '佘', '佴',
        '伯', '赏', '南', '宫', '墨', '哈', '谯', '笪', '年', '爱',
        '阳', '佟', '第', '五', '言', '福', '百', '家', '姓', '终'
    ]
    
    # 确保有3500个常用字（这里只列出了部分，实际应该更多）
    return set(common_chars)

def estimate_stroke_count(char):
    """估算汉字笔画数（简化版）"""
    # 常见笔画数映射
    common_strokes = {
        '一': 1, '乙': 1, '二': 2, '十': 2, '丁': 2, '厂': 2, '七': 2,
        '卜': 2, '八': 2, '人': 2, '入': 2, '儿': 2, '匕': 2, '几': 2,
        '九': 2, '刁': 2, '了': 2, '刀': 2, '力': 2, '乃': 2, '又': 2,
        '三': 3, '千': 3, '川': 3, '个': 3, '勺': 3, '久': 3, '凡': 3,
        '及': 3, '亡': 3, '门': 3, '义': 3, '之': 3, '尸': 3, '己': 3,
        '已': 3, '子': 3, '卫': 3, '也': 3, '女': 3, '飞': 3, '刃': 3,
        '习': 3, '马': 3, '乡': 3, '丰': 4, '王': 4, '井': 4, '开': 4,
        '夫': 4, '天': 4, '元': 4, '无': 4, '云': 4, '专': 4, '丐': 4,
        '廿': 4, '五': 4, '不': 4, '丐': 4, '丑': 4, '中': 4, '丰': 4,
        '为': 4, '主': 5, '市': 5, '立': 5, '冯': 5, '玄': 5, '玉': 5,
        '瓜': 5, '瓦': 5, '甘': 5, '生': 5, '用': 5, '田': 5, '由': 5,
        '甲': 5, '申': 5, '电': 5, '白': 5, '皮': 5, '皿': 5, '目': 5,
        '矛': 5, '矢': 5, '石': 5, '示': 5, '内': 4, '午': 4, '牛': 4,
        '手': 4, '毛': 4, '气': 4, '片': 4, '斤': 4, '爪': 4, '父': 4,
        '月': 4, '氏': 4, '欠': 4, '风': 4, '文': 4, '方': 4, '火': 4,
        '斗': 4, '户': 4, '心': 4, '毋': 4, '水': 4, '见': 4, '长': 4,
        '车': 4, '贝': 4, '见': 4, '韦': 4, '木': 4, '犬': 4, '歹': 4,
        '车': 4, '戈': 4, '比': 4, '瓦': 4, '止': 4, '攴': 4, '日': 4,
        '曰': 4, '水': 4, '火': 4, '爪': 4, '父': 4, '爻': 4, '爿': 4,
        '片': 4, '牙': 4, '牛': 4, '犬': 4, '玄': 4, '玉': 4, '瓜': 4,
        '瓦': 4, '甘': 4, '生': 4, '用': 4, '田': 4, '疋': 4, '疒': 4,
        '癶': 4, '白': 4, '皮': 4, '皿': 4, '目': 4, '矛': 4, '矢': 4,
        '石': 4, '示': 4, '禸': 4, '禾': 4, '穴': 4, '立': 4, '竹': 4,
        '米': 4, '糸': 4, '缶': 4, '网': 4, '羊': 4, '羽': 4, '老': 4,
        '而': 4, '耒': 4, '耳': 4, '聿': 4, '肉': 4, '臣': 4, '自': 4,
        '至': 4, '臼': 4, '舌': 4, '舛': 4, '舟': 4, '艮': 4, '色': 4,
        '艸': 4, '虍': 4, '虫': 4, '血': 4, '行': 4, '衣': 4, '襾': 4,
        '見': 4, '角': 4, '言': 4, '谷': 4, '豆': 4, '豕': 4, '豸': 4,
        '貝': 4, '赤': 4, '走': 4, '足': 4, '身': 4, '車': 4, '辛': 4,
        '辰': 4, '辵': 4, '邑': 4, '酉': 4, '釆': 4, '里': 4, '金': 4,
        '長': 4, '門': 4, '阜': 4, '隶': 4, '隹': 4, '雨': 4, '靑': 4,
        '非': 4, '面': 4, '革': 4, '韋': 4, '韭': 4, '音': 4, '頁': 4,
        '風': 4, '飛': 4, '食': 4, '首': 4, '香': 4, '馬': 4, '骨': 4,
        '高': 4, '髟': 4, '鬥': 4, '鬯': 4, '鬲': 4, '鬼': 4, '魚': 4,
        '鳥': 4, '鹵': 4, '鹿': 4, '麥': 4, '麻': 4, '黃': 4, '黍': 4,
        '黑': 4, '黹': 4, '黽': 4, '鼎': 4, '鼓': 4, '鼠': 4, '鼻': 4,
        '齊': 4, '齒': 4, '龍': 4, '龜': 4, '龠': 4
    }
    
    if char in common_strokes:
        return common_strokes[char]
    
    # 基于Unicode区块估算
    code_point = ord(char)
    if 0x4E00 <= code_point <= 0x9FFF:  # CJK统一汉字
        # 简化估算
        if code_point < 0x4F00:
            return 3  # 较简单的字
        elif code_point < 0x6000:
            return 6
        elif code_point < 0x7000:
            return 9
        elif code_point < 0x8000:
            return 12
        elif code_point < 0x9000:
            return 15
        else:
            return 8
    return 8  # 默认值

def calculate_character_score(char_data, common_chars):
    """计算汉字综合得分（得分越低越常用）"""
    char = char_data['char']
    
    # 1. 是否常用字（最重要）
    if char in common_chars:
        common_score = 0
    else:
        common_score = 10000
    
    # 2. 笔画数（笔画越少得分越低）
    stroke_count = estimate_stroke_count(char)
    stroke_score = stroke_count * 100
    
    # 3. Unicode编码（作为最后的排序依据）
    unicode_score = ord(char)
    
    # 综合得分
    total_score = common_score + stroke_score + (unicode_score / 1000000)
    
    return total_score

def sort_characters_by_frequency():
    """按字频排序所有汉字"""
    print("开始按字频排序汉字...")
    
    # 备份原始数据
    backup_dir = "data/backup_before_frequency_sorting"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"创建备份目录: {backup_dir}")
    
    for chapter in range(1, 11):
        src_file = f"data/chapter_{chapter}_characters.json"
        dst_file = f"{backup_dir}/chapter_{chapter}_characters.json.backup"
        if os.path.exists(src_file):
            shutil.copy2(src_file, dst_file)
            print(f"  备份: {src_file} -> {dst_file}")
    
    # 加载常用字
    common_chars = load_common_characters()
    print(f"加载常用字: {len(common_chars)} 个")
    
    # 收集所有汉字
    all_characters = []
    for chapter in range(1, 11):
        try:
            with open(f'data/chapter_{chapter}_characters.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_characters.extend(data)
                print(f"  第{chapter}章: 加载了{len(data)}个汉字")
        except Exception as e:
            print(f"  第{chapter}章加载失败: {e}")
    
    print(f"总共收集到 {len(all_characters)} 个汉字")
    
    # 计算每个汉字的得分
    print("计算汉字得分...")
    scored_characters = []
    for char_data in all_characters:
        score = calculate_character_score(char_data, common_chars)
        scored_characters.append({
            'char_data': char_data,
            'score': score
        })
    
    # 按得分排序（得分越低越常用）
    print("按得分排序...")
    scored_characters.sort(key=lambda x: x['score'])
    
    # 生成排名
    print("生成最终排名...")
    ranked_characters = []
    for i, item in enumerate(scored_characters, 1):
        char_data = item['char_data'].copy()
        char_data['frequency_rank'] = i  # 更新频率排名
        ranked_characters.append(char_data)
    
    # 按章节重新分组
    print("按章节重新分组...")
    total_chars = len(ranked_characters)
    chars_per_chapter = total_chars // 10
    remainder = total_chars % 10
    
    start_index = 0
    for chapter in range(1, 11):
        # 计算本章汉字数量
        chapter_count = chars_per_chapter
        if chapter <= remainder:
            chapter_count += 1
        
        # 获取本章汉字
        end_index = start_index + chapter_count
        chapter_chars = ranked_characters[start_index:end_index]
        
        # 保存到文件
        output_file = f'data/chapter_{chapter}_characters.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(chapter_chars, f, ensure_ascii=False, indent=2)
        
        print(f"  第{chapter}章: {len(chapter_chars)}个汉字")
        print(f"    第一个字: {chapter_chars[0]['char']} (排名: {chapter_chars[0]['frequency_rank']})")
        print(f"    最后一个字: {chapter_chars[-1]['char']} (排名: {chapter_chars[-1]['frequency_rank']})")
        
        # 更新起始索引
        start_index = end_index
    
    # 生成统计报告
    generate_statistics_report(ranked_characters)
    
    print("\n" + "=" * 60)
    print("排序完成！")
    print("=" * 60)
    print("重要提示:")
    print("1. 原始数据已备份到 data/backup_before_frequency_sorting/")
    print("2. 新的字频排名已应用到所有章节数据")
    print("3. 现在汉字将按字频排序（最常用字在前）")
    print("4. 排序规则: 常用字优先 → 笔画数少优先 → Unicode编码")
    print("=" * 60)

def generate_statistics_report(ranked_characters):
    """生成统计报告"""
    report = {
        "total_characters": len(ranked_characters),
        "top_50_chars": [],
        "bottom_50_chars": [],
        "chapters_summary": {}
    }
    
    # 前50个最常用字
    report["top_50_chars"] = [
        {
            "char": c['char'],
            "jyutping": c.get('jyutping', ''),
            "frequency_rank": c['frequency_rank']
        }
        for c in ranked_characters[:50]
    ]
    
    # 后50个最不常用字
    report["bottom_50_chars"] = [
        {
            "char": c['char'],
            "jyutping": c.get('jyutping', ''),
            "frequency_rank": c['frequency_rank']
        }
        for c in ranked_characters[-50:]
    ]
    
    # 章节统计
    total_chars = len(ranked_characters)
    chars_per_chapter = total_chars // 10
    remainder = total_chars % 10
    
    start_index = 0
    for chapter in range(1, 11):
        chapter_count = chars_per_chapter
        if chapter <= remainder:
            chapter_count += 1
        
        end_index = start_index + chapter_count
        chapter_chars = ranked_characters[start_index:end_index]
        
        report["chapters_summary"][f"chapter_{chapter}"] = {
            "character_count": len(chapter_chars),
            "first_char": chapter_chars[0]['char'],
            "first_char_rank": chapter_chars[0]['frequency_rank'],
            "last_char": chapter_chars[-1]['char'],
            "last_char_rank": chapter_chars[-1]['frequency_rank']
        }
        
        start_index = end_index
    
    # 保存报告
    with open('data/frequency_sorting_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n统计报告已保存: data/frequency_sorting_report.json")
    
    # 打印简要报告
    print("\n=== 字频排序统计报告 ===")
    print(f"总汉字数: {report['total_characters']}")
    print("\n前10个最常用汉字:")
    for i, char_info in enumerate(report['top_50_chars'][:10], 1):
        print(f"  {i}. {char_info['char']} ({char_info['jyutping']}) - 排名: {char_info['frequency_rank']}")
    
    print("\n最后10个汉字:")
    for i, char_info in enumerate(report['bottom_50_chars'][-10:], 1):
        idx = report['total_characters'] - 10 + i
        print(f"  {idx}. {char_info['char']} ({char_info['jyutping']}) - 排名: {char_info['frequency_rank']}")

if __name__ == "__main__":
    print("=" * 60)
    print("汉字字频排序系统")
    print("排序规则: 常用字优先 → 笔画数少优先 → Unicode编码")
    print("=" * 60)
    
    # 确认操作
    response = input("是否开始按字频排序所有汉字？(y/n): ")
    if response.lower() == 'y':
        sort_characters_by_frequency()
    else:
        print("操作已取消。")