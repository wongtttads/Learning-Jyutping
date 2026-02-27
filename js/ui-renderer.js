class UIRenderer {
    constructor() {
        this.chaptersContainer = document.getElementById('chapters-container');
        this.chapterContent = document.getElementById('chapter-content');
        this.charactersGrid = document.getElementById('characters-grid');
        this.chapterTitle = document.getElementById('chapter-title');
        this.backBtn = document.getElementById('back-btn');
        
        // 例词数据库
        this.characterExamples = {
            "的": ["好的", "你的", "我的"],
            "是": ["是的", "就是", "可是"],
            "在": ["现在", "在这里", "在哪里"],
            "了": ["好了", "走了", "吃了"],
            "我": ["我们", "我家", "我的"],
            "和": ["和平", "和谐", "和你"],
            "有": ["有的", "没有", "所有"],
            "不": ["不要", "不是", "不会"],
            "人": ["人们", "人类", "人生"],
            "也": ["也是", "也好", "也许"],
            "你": ["你们", "你的", "你好"],
            "为": ["因为", "为了", "作为"],
            "这": ["这个", "这里", "这样"],
            "他": ["他们", "他的", "其他"],
            "中": ["中国", "中间", "中心"],
            "与": ["参与", "与其", "与你"],
            "年": ["新年", "年份", "年龄"],
            "对": ["对的", "对方", "面对"],
            "就": ["就是", "就好", "就业"],
            "都": ["都是", "都会", "首都"],
            "说": ["说话", "说明", "说法"],
            "上": ["上面", "上海", "上班"],
            "吗": ["好吗", "是吗", "对吗"],
            "会": ["开会", "会议", "会说"],
            "到": ["到达", "到处", "到底"],
            "要": ["需要", "要是", "要求"],
            "来": ["来到", "来去", "来自"],
            "月": ["月亮", "月份", "月光"],
            "被": ["被动", "被子", "被单"],
            "还": ["还有", "还是", "还原"],
            "而": ["而且", "然而", "而已"],
            "个": ["个人", "个别", "个性"],
            "等": ["等待", "等级", "等等"],
            "后": ["后面", "后来", "后天"],
            "但": ["但是", "但愿", "但凡"],
            "于": ["于是", "由于", "关于"],
            "日": ["日子", "日期", "日本"],
            "能": ["能力", "能够", "能量"],
            "将": ["将来", "将军", "将要"],
            "并": ["并且", "并列", "合并"],
            "一": ["一个", "一起", "一旦"],
            "很": ["很多", "很好", "很大"],
            "让": ["让开", "让步", "让座"],
            "从": ["从来", "从此", "从小"],
            "好": ["好人", "好事", "好看"],
            "以": ["以为", "以后", "以前"],
            "大": ["大家", "大小", "大学"],
            "她": ["她们", "她的", "她是"],
            "着": ["看着", "听着", "说着"],
            "多": ["多少", "多个", "多余"],
            "给": ["给予", "给你", "给我"],
            "时": ["时间", "时候", "时期"],
            "把": ["把握", "把手", "把持"],
            "看": ["看见", "看到", "看书"],
            "去": ["去年", "去向", "去世"],
            "又": ["又一次", "又好", "又快"],
            "或": ["或者", "或许", "或是"],
            "过": ["过去", "过来", "过年"],
            "之": ["之后", "之前", "之间"],
            "下": ["下面", "下去", "下午"],
            "新": ["新年", "新闻", "新鲜"],
            "里": ["里面", "里面", "公里"],
            "地": ["地方", "地球", "地面"],
            "及": ["及格", "及时", "及早"],
            "做": ["做事", "做人", "做工"],
            "由": ["由于", "由来", "由他"],
            "用": ["用处", "用途", "用户"],
            "没": ["没有", "没事", "没办法"],
            "更": ["更加", "更好", "更大"],
            "得": ["得到", "得分", "得体"],
            "所": ["所以", "所有", "所在"],
            "想": ["想法", "想念", "想象"],
            "最": ["最好", "最大", "最近"],
            "它": ["它们", "它的", "它是"],
            "那": ["那个", "那里", "那样"],
            "可": ["可以", "可能", "可是"],
            "三": ["三个", "三天", "三年"],
            "吧": ["好吧", "走吧", "来吧"],
            "其": ["其中", "其实", "其他"],
            "该": ["应该", "该当", "该死"],
            "只": ["只有", "只是", "只要"],
            "向": ["方向", "向往", "向前"],
            "前": ["前面", "前进", "前途"],
            "啊": ["好啊", "是啊", "对啊"],
            "出": ["出去", "出来", "出发"],
            "已": ["已经", "已知", "已然"],
            "小": ["小孩", "小心", "小学"],
            "当": ["当然", "当时", "当下"],
            "再": ["再次", "再见", "再试"],
            "们": ["我们", "你们", "他们"],
            "内": ["内部", "内容", "内心"],
            "却": ["却是", "却步", "却不"],
            "才": ["才能", "才华", "才子"],
            "爱": ["爱情", "爱心", "爱人"],
            "第": ["第一", "第二", "第三"],
            "谁": ["谁的", "谁是", "谁知"],
            "号": ["号码", "号召", "号角"],
            "快": ["快乐", "快速", "快递"],
            "事": ["事情", "事实", "事业"],
            "比": ["比较", "比赛", "比例"],
            "跟": ["跟随", "跟上", "跟从"],
            "长": ["长度", "长期", "长期"],
            "请": ["请求", "请客", "请问"],
            "呢": ["好呢", "是呢", "对呢"],
            "高": ["高兴", "高度", "高分"],
            "则": ["规则", "原则", "守则"],
            "钱": ["钱包", "钱财", "金钱"],
            "至": ["至少", "至于", "至今"],
            "万": ["万一", "万岁", "万物"],
            "使": ["使用", "使命", "使者"],
            "点": ["点头", "点击", "点心"],
            "像": ["好像", "相像", "像样"],
            "听": ["听见", "听说", "听力"],
            "起": ["起来", "起床", "起点"],
            "此": ["此时", "此地", "此外"],
            "自": ["自己", "自动", "自由"],
            "两": ["两个", "两天", "两年"],
            "国": ["国家", "国际", "国产"],
            "走": ["走路", "走路", "走开"],
            "如": ["如果", "如何", "如意"],
            "带": ["带动", "带头", "带领"],
            "吃": ["吃饭", "吃水", "吃药"],
            "无": ["无论", "无法", "无穷"],
            "岁": ["岁月", "岁数", "岁末"],
            "话": ["话题", "话语", "话费"],
            "较": ["比较", "较量", "较为"],
            "家": ["家庭", "家人", "家乡"],
            "么": ["什么", "怎么", "多么"],
            "区": ["区域", "地区", "小区"],
            "太": ["太阳", "太多", "太小"],
            "约": ["约会", "约定", "大约"],
            "者": ["作者", "读者", "学者"],
            "开": ["开始", "开车", "开放"],
            "问": ["问题", "问答", "问候"],
            "站": ["站立", "车站", "站点"],
            "成": ["成功", "成长", "成绩"],
            "因": ["因为", "因素", "因果"],
            "写": ["写作", "写字", "写作"],
            "元": ["元素", "元气", "元首"],
            "打": ["打击", "打饭", "打字"],
            "分": ["分数", "分开", "分手"],
            "死": ["死亡", "死活", "死心"],
            "见": ["见面", "见识", "见解"],
            "买": ["买卖", "买家", "买主"],
            "叫": ["叫声", "叫喊", "叫好"],
            "图": ["图片", "图像", "图画"],
            "曾": ["曾经", "未曾", "曾几何时"],
            "即": ["即使", "立即", "即将"],
            "道": ["道路", "道理", "道德"],
            "天": ["天空", "天气", "天使"],
            "总": ["总结", "总是", "总计"],
            "应": ["应该", "应当", "应付"],
            "另": ["另外", "另有", "另行"],
            "正": ["正确", "正直", "正常"],
            "间": ["房间", "时间", "中间"],
            "便": ["便利", "方便", "便宜"],
            "党": ["党派", "党员", "党羽"],
            "发": ["发展", "发生", "发现"],
            "本": ["本来", "本质", "本金"],
            "名": ["名字", "名声", "名誉"],
            "干": ["干净", "干涉", "干燥"],
            "达": ["达到", "达成", "达标"],
            "找": ["找到", "寻找", "查找"],
            "称": ["称呼", "称赞", "称号"],
            "玩": ["玩具", "玩耍", "玩笑"],
            "您": ["您好", "您的", "您是"],
            "进": ["进步", "进入", "进口"],
            "受": ["受到", "受伤", "受益"],
            "县": ["县城", "县长", "县级"],
            "真": ["真实", "真相", "真理"],
            "种": ["种子", "种类", "种植"],
            "女": ["女性", "女人", "女孩"],
            "处": ["处理", "处分", "处罚"],
            "每": ["每天", "每个", "每次"],
            "市": ["市场", "城市", "市区"],
            "各": ["各个", "各自", "各种"],
            "作": ["作业", "作品", "作者"],
            "位": ["位置", "地位", "职位"],
            "次": ["次数", "次要", "次序"],
            "未": ["未来", "未知", "未必"],
            "省": ["省份", "节省", "省心"],
            "网": ["网络", "网站", "网页"],
            "老": ["老师", "老人", "老家"],
            "经": ["经常", "经济", "经验"],
            "外": ["外面", "外国", "外部"],
            "马": ["马上", "马车", "马匹"],
            "副": ["副本", "副业", "副作用"],
            "行": ["行动", "行业", "行走"],
            "美": ["美丽", "美好", "美术"],
            "路": ["路程", "路线", "路灯"],
            "连": ["连接", "连续", "连线"],
            "拿": ["拿到", "拿手", "拿起"],
            "制": ["制度", "制作", "制约"],
            "同": ["同学", "同事", "同样"],
            "仍": ["仍然", "仍旧", "仍是"],
            "军": ["军队", "军人", "军事"],
            "哪": ["哪里", "哪个", "哪些"],
            "先": ["先生", "先进", "先后"],
            "台": ["台湾", "台灯", "台阶"],
            "占": ["占有", "占据", "占领"],
            "杀": ["杀人", "杀气", "杀毒"],
            "二": ["二手", "二月", "二年级"],
            "学": ["学习", "学校", "学问"],
            "住": ["住宿", "住房", "住户"],
            "非": ["非常", "非凡", "非法"],
            "据": ["根据", "依据", "证据"],
            "书": ["书籍", "书本", "书法"],
            "回": ["回答", "回家", "回报"],
            "亦": ["亦然", "亦步亦趋", "亦庄亦谐"],
            "别": ["别人", "别的", "别墅"],
            "心": ["心情", "心理", "心态"],
            "讲": ["讲话", "讲解", "讲述"],
            "条": ["条件", "条理", "条纹"],
            "反": ["反对", "反应", "反驳"],
            "送": ["送礼", "送行", "送货"],
            "啦": ["好啦", "来啦", "走啦"],
            "版": ["版本", "版面", "版权"],
            "性": ["性格", "性别", "性质"],
            "指": ["指导", "指示", "指挥"],
            "法": ["法律", "法规", "方法"],
            "期": ["期限", "期望", "期待"],
            "均": ["平均", "均匀", "均衡"],
            "全": ["全部", "全面", "全体"],
            "变": ["变化", "变形", "变革"],
            "米": ["米饭", "米粉", "米线"],
            "生": ["生活", "生命", "生产"],
            "水": ["水果", "水平", "水分"],
            "共": ["共同", "共有", "共享"],
            "派": ["派遣", "派对", "派别"],
            "车": ["汽车", "车站", "车程"],
            "搞": ["搞定", "搞活", "搞笑"],
            "手": ["手机", "手工", "手段"],
            "原": ["原因", "原始", "原理"],
            "类": ["类别", "类似", "类型"],
            "级": ["级别", "等级", "年级"],
            "些": ["一些", "这些", "那些"],
            "场": ["场地", "场景", "场合"],
            "型": ["型号", "类型", "造型"],
            "按": ["按照", "按时", "按摩"],
            "线": ["线条", "线路", "线索"],
            "跑": ["跑步", "跑车", "跑道"],
            "亿": ["亿万", "亿年", "亿人"],
            "哦": ["好哦", "是哦", "对哦"],
            "靠": ["靠近", "靠山", "可靠"],
            "报": ["报纸", "报告", "报答"],
            "男": ["男性", "男人", "男孩"],
            "若": ["若是", "若果", "若有"],
            "少": ["少数", "少年", "少女"],
            "加": ["加法", "加入", "加强"],
            "队": ["队伍", "队列", "队长"],
            "拉": ["拉力", "拉伸", "拉手"],
            "且": ["而且", "且慢", "且说"],
            "低": ["低头", "低调", "低价"],
            "放": ["放学", "放弃", "放松"],
            "门": ["门口", "门卫", "门第"],
            "拍": ["拍照", "拍打", "拍卖"],
            "系": ["系统", "系列", "系数"],
            "金": ["金色", "金融", "金钱"],
            "西": ["西方", "西边", "西瓜"],
            "完": ["完成", "完美", "完毕"],
            "式": ["形式", "样式", "方式"],
            "穿": ["穿着", "穿衣", "穿越"],
            "笑": ["笑容", "笑话", "笑脸"],
            "近": ["近视", "近来", "近况"],
            "强": ["强大", "强烈", "坚强"],
            "属": ["属于", "属性", "属实"],
            "选": ["选择", "选举", "选拔"],
            "难": ["难题", "难道", "难过"],
            "越": ["越来越", "越级", "越过"],
            "四": ["四个", "四天", "四年"],
            "张": ["张开", "张望", "张贴"],
            "任": ["任务", "任命", "任意"],
            "办": ["办法", "办理", "办公室"],
            "抓": ["抓住", "抓紧", "抓人"],
            "谈": ["谈话", "谈论", "谈判"],
            "转": ["转弯", "转向", "转变"],
            "动": ["动作", "动力", "动机"],
            "黑": ["黑色", "黑暗", "黑客"],
            "卖": ["买卖", "卖家", "卖主"],
            "东": ["东方", "东边", "东京"],
            "仅": ["仅仅", "仅存", "仅有"],
            "狗": ["小狗", "狗肉", "狗年"],
            "字": ["字体", "字母", "字典"],
            "帮": ["帮助", "帮忙", "帮派"],
            "花": ["花朵", "花费", "花园"],
            "黄": ["黄色", "黄金", "黄昏"],
            "部": ["部分", "部门", "部队"],
            "届": ["届时", "届满", "届期"],
            "早": ["早上", "早点", "早期"],
            "相": ["相信", "相互", "相处"],
            "主": ["主人", "主要", "主动"],
            "子": ["子女", "子孙", "子公司"],
            "段": ["段落", "段位", "片段"],
            "关": ["关心", "关注", "关于"],
            "件": ["文件", "事件", "条件"],
            "信": ["信心", "信任", "信件"],
            "提": ["提高", "提升", "提醒"],
            "算": ["计算", "算法", "算术"],
            "五": ["五个", "五天", "五年"],
            "令": ["命令", "令郎", "令爱"],
            "需": ["需要", "需求", "供需"],
            "错": ["错误", "错过", "错觉"],
            "管": ["管理", "管道", "管束"],
            "刚": ["刚才", "刚刚", "刚强"],
            "远": ["远近", "远程", "远方"],
            "王": ["王国", "王子", "王位"],
            "面": ["面对", "面积", "面子"],
            "嘛": ["好嘛", "是嘛", "对嘛"],
            "重": ["重要", "重量", "重点"],
            "倒": ["倒立", "倒下", "倒霉"],
            "城": ["城市", "城墙", "城关"],
            "数": ["数字", "数学", "数量"],
            "神": ["神灵", "神奇", "神圣"],
            "设": ["设计", "设置", "设立"],
            "几": ["几个", "几天", "几年"],
            "员": ["员工", "成员", "会员"],
            "团": ["团队", "团结", "团圆"],
            "权": ["权利", "权力", "权威"],
            "求": ["请求", "要求", "追求"],
            "既": ["既然", "既定", "既而"],
            "入": ["入口", "进入", "入侵"],
            "逼": ["逼迫", "逼人", "逼债"],
            "镇": ["城镇", "镇压", "镇定"],
            "群": ["群众", "群体", "群组"],
            "头": ["头部", "头脑", "头衔"],
            "现": ["现在", "现实", "现象"],
            "乡": ["乡村", "乡镇", "乡愁"],
            "组": ["组织", "组合", "组成"],
            "呀": ["好呀", "是呀", "对呀"],
            "教": ["教育", "教师", "教学"],
            "获": ["获得", "获取", "获胜"],
            "南": ["南方", "南边", "南京"],
            "奖": ["奖励", "奖金", "奖品"],
            "德": ["道德", "品德", "德行"],
            "定": ["决定", "定位", "定居"],
            "读": ["读书", "阅读", "读物"],
            "脸": ["脸色", "脸面", "脸谱"],
            "机": ["机器", "机械", "机会"],
            "集": ["集合", "集体", "集中"],
            "懂": ["懂得", "懂事", "懂行"],
            "电": ["电视", "电脑", "电力"],
            "常": ["常常", "常规", "常态"],
            "假": ["假期", "假设", "假话"],
            "州": ["广州", "苏州", "杭州"],
            "项": ["项目", "项链", "项目"],
            "改": ["改变", "改造", "改进"],
            "活": ["生活", "活动", "活力"],
            "换": ["换取", "换算", "换乘"],
            "特": ["特别", "特殊", "特色"],
            "妈": ["妈妈", "妈咪", "妈眯"],
            "往": ["往来", "往往", "往返"],
            "离": ["离开", "距离", "离别"],
            "坐": ["坐下", "座位", "坐牢"],
            "旧": ["旧物", "旧居", "旧年"],
            "亚": ["亚洲", "亚军", "亚种"],
            "传": ["传说", "传奇", "传统"],
            "梦": ["梦想", "梦境", "梦幻"],
            "喝": ["喝水", "喝酒", "喝茶"],
            "云": ["云彩", "云朵", "云霄"],
            "体": ["体育", "身体", "体检"],
            "卡": ["卡片", "卡通", "卡车"],
            "随": ["随便", "随从", "跟随"],
            "著": ["著名", "著作", "著述"],
            "赢": ["赢得", "赢家", "赢利"],
            "山": ["山水", "山峰", "山脉"],
            "热": ["热闹", "热门", "热情"],
            "度": ["温度", "度数", "度过"],
            "周": ["周围", "周期", "周转"],
            "值": ["价值", "值得", "值钱"],
            "单": ["单独", "单位", "单数"],
            "遭": ["遭遇", "遭受", "遭殃"],
            "文": ["文化", "文明", "文字"],
            "斯": ["斯文", "斯文人", "斯时"],
            "语": ["语言", "语文", "语法"],
            "北": ["北方", "北边", "北京"],
            "双": ["双方", "双倍", "双数"],
            "今": ["今天", "今年", "今后"],
            "久": ["长久", "久远", "久别"],
            "史": ["历史", "史实", "史记"],
            "页": ["页面", "页码", "页数"],
            "明": ["明白", "明确", "明亮"],
            "某": ["某些", "某个", "某人"],
            "科": ["科学", "科技", "科目"],
            "皆": ["皆大欢喜", "比比皆是", "皆可"],
            "六": ["六个", "六天", "六年"],
            "光": ["光明", "光线", "光芒"],
            "半": ["半天", "半年", "半价"],
            "师": ["老师", "师傅", "师兄"],
            "兼": ["兼职", "兼顾", "兼任"],
            "尽": ["尽力", "尽情", "尽责"],
            "除": ["除法", "除去", "除了"],
            "村": ["村庄", "村民", "村长"],
            "案": ["案例", "案件", "案板"],
            "睡": ["睡觉", "睡眠", "睡梦"],
            "李": ["李子", "李树", "李姓"],
            "化": ["化学", "变化", "化解"],
            "包": ["包子", "包装", "包围"],
            "官": ["官员", "官场", "官职"],
            "尔": ["尔等", "尔辈", "尔虞我诈"],
            "救": ["救命", "救援", "救护"],
            "街": ["街道", "街头", "街区"],
            "红": ["红色", "红军", "红糖"],
            "克": ["克服", "克制", "克己"],
            "初": ["初步", "初期", "初心"],
            "卷": ["卷起", "卷发", "卷纸"],
            "块": ["块状", "块头", "块茎"],
            "驻": ["驻守", "驻扎", "驻留"]
        };
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

    // 获取频率级别
    getFrequencyLevel(rank) {
        if (rank <= 100) return '很高';
        if (rank <= 500) return '高';
        if (rank <= 2000) return '中等';
        if (rank <= 5000) return '较低';
        return '低';
    }

    // 获取汉字的例词
    getCharacterExamples(char) {
        return this.characterExamples[char] || ["暂无例词", "暂无例词", "暂无例词"];
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

        // 确保按频率排名排序（从小到大）
        const sortedCharacters = [...characters].sort((a, b) => {
            return (a.frequency_rank || 99999) - (b.frequency_rank || 99999);
        });

        console.log('📊 排序检查 - 前5个字符:');
        sortedCharacters.slice(0, 5).forEach((char, index) => {
            console.log(`   ${index + 1}. ${char.char} - 排名: ${char.frequency_rank}`);
        });

        // 检查是否是多音字章节
        const isPolyphoneChapter = chapterTitle === '多音字专栏';
        
        let html;
        
        if (isPolyphoneChapter) {
            // 使用多音字专用卡片
            html = sortedCharacters.map(char => {
                const frequencyLevel = this.getFrequencyLevel(char.frequency_rank);
                return this.renderPolyphoneCard(char, frequencyLevel);
            }).join('');
        } else {
            // 使用普通卡片
            const displayScheme = window.config ? window.config.displayScheme : 3;
            
            html = sortedCharacters.map(char => {
                const frequencyLevel = this.getFrequencyLevel(char.frequency_rank);
                const examples = this.getCharacterExamples(char.char);
                const hasSecondaryJyutping = char.secondary_jyutping && char.secondary_jyutping !== '';
                
                switch (displayScheme) {
                    case 1: // 方案A - 增加独立粤拼卡片
                        return this.renderSchemeA(char, frequencyLevel, examples, hasSecondaryJyutping);
                    case 2: // 方案B - 卡片内部分区展示
                        return this.renderSchemeB(char, frequencyLevel, examples, hasSecondaryJyutping);
                    case 3: // 方案C - 悬浮显示方案
                        return this.renderSchemeC(char, frequencyLevel, examples, hasSecondaryJyutping);
                    case 4: // 方案D - 标签切换方案
                        return this.renderSchemeD(char, frequencyLevel, examples, hasSecondaryJyutping);
                    default:
                        return this.renderSchemeC(char, frequencyLevel, examples, hasSecondaryJyutping);
                }
            }).join('');
        }

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

    // 方案A - 增加独立粤拼卡片
    renderSchemeA(char, frequencyLevel, examples, hasSecondaryJyutping) {
        const baseCard = `
            <div class="character-card" data-char="${char.char}" data-pinyin="${char.jyutping}">
                <div class="character-char">${char.char}</div>
                <div class="character-pinyin">${char.jyutping}</div>
                <div class="character-rank">排名: ${char.frequency_rank}</div>
                <div class="character-frequency">频率: ${frequencyLevel}</div>
                <button class="pronunciation-btn" data-char="${char.char}" data-pinyin="${char.jyutping}">
                    <i class="fas fa-volume-up"></i>
                    <span>朗读</span>
                </button>
                <div class="character-examples">
                    <div class="examples-title">常用例词:</div>
                    <div class="examples-list">
                        ${examples.map(example => `<span class="example-word">${example}</span>`).join('')}
                    </div>
                </div>
            </div>
        `;
        
        if (hasSecondaryJyutping) {
            return `
                <div class="character-card-group">
                    ${baseCard}
                    <div class="character-card secondary-card" data-char="${char.char}" data-pinyin="${char.secondary_jyutping}">
                        <div class="character-char">${char.char}</div>
                        <div class="character-pinyin secondary-pinyin">${char.secondary_jyutping}</div>
                        <div class="secondary-label">第二发音</div>
                        <button class="pronunciation-btn" data-char="${char.char}" data-pinyin="${char.secondary_jyutping}">
                            <i class="fas fa-volume-up"></i>
                            <span>朗读</span>
                        </button>
                    </div>
                </div>
            `;
        }
        return baseCard;
    }

    // 方案B - 卡片内部分区展示
    renderSchemeB(char, frequencyLevel, examples, hasSecondaryJyutping) {
        let pinyinHtml = `<div class="character-pinyin primary-pinyin">${char.jyutping}</div>`;
        if (hasSecondaryJyutping) {
            pinyinHtml += `<div class="character-pinyin secondary-pinyin">${char.secondary_jyutping}</div>`;
        }
        
        return `
            <div class="character-card" data-char="${char.char}" data-pinyin="${char.jyutping}">
                <div class="character-char">${char.char}</div>
                ${pinyinHtml}
                <div class="character-rank">排名: ${char.frequency_rank}</div>
                <div class="character-frequency">频率: ${frequencyLevel}</div>
                <div class="pronunciation-buttons">
                    <button class="pronunciation-btn primary-btn" data-char="${char.char}" data-pinyin="${char.jyutping}">
                        <i class="fas fa-volume-up"></i>
                        <span>朗读</span>
                    </button>
                    ${hasSecondaryJyutping ? `
                        <button class="pronunciation-btn secondary-btn" data-char="${char.char}" data-pinyin="${char.secondary_jyutping}">
                            <i class="fas fa-volume-up"></i>
                            <span>朗读</span>
                        </button>
                    ` : ''}
                </div>
                <div class="character-examples">
                    <div class="examples-title">常用例词:</div>
                    <div class="examples-list">
                        ${examples.map(example => `<span class="example-word">${example}</span>`).join('')}
                    </div>
                </div>
            </div>
        `;
    }

    // 方案C - 悬浮显示方案
    renderSchemeC(char, frequencyLevel, examples, hasSecondaryJyutping) {
        let pinyinHtml = `<div class="character-pinyin primary-pinyin">${char.jyutping}</div>`;
        if (hasSecondaryJyutping) {
            pinyinHtml += `<div class="character-pinyin secondary-pinyin hidden">${char.secondary_jyutping}</div>`;
        }
        
        return `
            <div class="character-card ${hasSecondaryJyutping ? 'has-secondary' : ''}" data-char="${char.char}" data-pinyin="${char.jyutping}">
                <div class="character-char">${char.char}</div>
                ${pinyinHtml}
                <div class="character-rank">排名: ${char.frequency_rank}</div>
                <div class="character-frequency">频率: ${frequencyLevel}</div>
                <button class="pronunciation-btn" data-char="${char.char}" data-pinyin="${char.jyutping}">
                    <i class="fas fa-volume-up"></i>
                    <span>朗读</span>
                </button>
                ${hasSecondaryJyutping ? `
                    <button class="pronunciation-btn secondary-btn hidden" data-char="${char.char}" data-pinyin="${char.secondary_jyutping}">
                        <i class="fas fa-volume-up"></i>
                        <span>朗读</span>
                    </button>
                    <div class="secondary-hint">悬停查看第二发音</div>
                ` : ''}
                <div class="character-examples">
                    <div class="examples-title">常用例词:</div>
                    <div class="examples-list">
                        ${examples.map(example => `<span class="example-word">${example}</span>`).join('')}
                    </div>
                </div>
            </div>
        `;
    }

    // 方案D - 标签切换方案
    renderSchemeD(char, frequencyLevel, examples, hasSecondaryJyutping) {
        return `
            <div class="character-card" data-char="${char.char}" data-pinyin="${char.jyutping}">
                <div class="character-char">${char.char}</div>
                ${hasSecondaryJyutping ? `
                    <div class="pinyin-tabs">
                        <div class="tab active" data-tab="primary">发音1</div>
                        <div class="tab" data-tab="secondary">发音2</div>
                    </div>
                ` : ''}
                <div class="pinyin-content">
                    <div class="pinyin-panel active" id="primary-${char.char}">
                        <div class="character-pinyin">${char.jyutping}</div>
                        <button class="pronunciation-btn" data-char="${char.char}" data-pinyin="${char.jyutping}">
                            <i class="fas fa-volume-up"></i>
                            <span>朗读</span>
                        </button>
                    </div>
                    ${hasSecondaryJyutping ? `
                        <div class="pinyin-panel" id="secondary-${char.char}">
                            <div class="character-pinyin">${char.secondary_jyutping}</div>
                            <button class="pronunciation-btn" data-char="${char.char}" data-pinyin="${char.secondary_jyutping}">
                                <i class="fas fa-volume-up"></i>
                                <span>朗读</span>
                            </button>
                        </div>
                    ` : ''}
                </div>
                <div class="character-rank">排名: ${char.frequency_rank}</div>
                <div class="character-frequency">频率: ${frequencyLevel}</div>
                <div class="character-examples">
                    <div class="examples-title">常用例词:</div>
                    <div class="examples-list">
                        ${examples.map(example => `<span class="example-word">${example}</span>`).join('')}
                    </div>
                </div>
            </div>
        `;
    }

    // 多音字专用卡片渲染
    renderPolyphoneCard(char, frequencyLevel) {
        const primaryExamples = char.examples?.primary || ["暂无例词", "暂无例词", "暂无例词"];
        const secondaryExamples = char.examples?.secondary || ["暂无例词", "暂无例词", "暂无例词"];
        const primaryDefinition = char.definitions?.primary || "暂无释义";
        const secondaryDefinition = char.definitions?.secondary || "暂无释义";
        
        return `
            <div class="character-card polyphone-card" data-char="${char.char}" data-pinyin="${char.jyutping}">
                <div class="character-char">${char.char}</div>
                <div class="pinyin-tabs">
                    <div class="tab active" data-tab="primary">主要读音</div>
                    <div class="tab" data-tab="secondary">次要读音</div>
                </div>
                <div class="pinyin-content">
                    <div class="pinyin-panel active" id="primary-${char.char}">
                        <div class="character-pinyin primary-pinyin">${char.jyutping}</div>
                        <div class="character-definition">${primaryDefinition}</div>
                        <button class="pronunciation-btn" data-char="${char.char}" data-pinyin="${char.jyutping}">
                            <i class="fas fa-volume-up"></i>
                            <span>朗读</span>
                        </button>
                        <div class="character-examples">
                            <div class="examples-title">典型例词:</div>
                            <div class="examples-list">
                                ${primaryExamples.map(example => `<span class="example-word">${example}</span>`).join('')}
                            </div>
                        </div>
                    </div>
                    <div class="pinyin-panel" id="secondary-${char.char}">
                        <div class="character-pinyin secondary-pinyin">${char.secondary_jyutping}</div>
                        <div class="character-definition">${secondaryDefinition}</div>
                        <button class="pronunciation-btn" data-char="${char.char}" data-pinyin="${char.secondary_jyutping}">
                            <i class="fas fa-volume-up"></i>
                            <span>朗读</span>
                        </button>
                        <div class="character-examples">
                            <div class="examples-title">典型例词:</div>
                            <div class="examples-list">
                                ${secondaryExamples.map(example => `<span class="example-word">${example}</span>`).join('')}
                            </div>
                        </div>
                    </div>
                </div>
                <div class="character-rank">排名: ${char.frequency_rank}</div>
                <div class="character-frequency">频率: ${frequencyLevel}</div>
            </div>
        `;
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
