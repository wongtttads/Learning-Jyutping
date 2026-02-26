# 粤语拼音学习系统

一个基于《通用规范汉字表》的粤语拼音学习系统，提供完整的汉字拼音数据、发音功能、学习测验和进度跟踪。

## 功能特性

### 📚 数据处理
- 基于《通用规范汉字表》三个级别（约8000字）
- 自动转换为粤语拼音（Jyutping）
- 拆分声母、韵母、声调
- 按频率分章节组织学习内容
- 智能生成例词

### 🔊 发音功能
- 基于macOS系统语音合成
- 使用粤语语音包（Sinji）
- 支持汉字和拼音朗读
- RESTful API接口

### 🎯 学习功能
- 分章节浏览学习
- 全屏学习模式
- 汉字卡片展示
- 例词参考
- 点击发音

### 📝 测验系统
- 汉字→拼音测验
- 拼音→汉字测验
- 混合模式测验
- 自定义题目数量
- 实时反馈
- 错题回顾

### 📊 进度跟踪
- 学习统计
- 连续学习天数
- 章节进度
- 测验历史
- 智能复习提醒
- 数据导入导出

## 项目结构

```
常用词粤语拼音/
├── data/
│   └── processed/
│       ├── jyutping_master.csv          # 主数据文件
│       └── batch_upload_canva.csv        # 批量上传数据
├── output/
│   ├── data/
│   │   ├── chapter_characters.json       # 章节字符数据
│   │   ├── chapter_1_characters.json     # 各章节数据
│   │   └── example_words.json            # 例词映射
│   ├── frequency_chapters.html           # 分章节学习页面
│   ├── learning_fullscreen.html          # 全屏学习页面
│   ├── quiz.html                          # 测验页面
│   └── progress.html                     # 进度统计页面
├── scripts/
│   ├── build_master_db.py                # 构建主数据库
│   ├── generate_char_data.py             # 生成章节数据
│   ├── generate_example_words.py          # 生成例词（旧版）
│   ├── generate_example_words_v2.py       # 生成例词（新版）
│   ├── generate_example_words_v3.py       # 生成例词（改进版）
│   ├── pronunciation.js                  # 发音功能（前端）
│   ├── progress_tracker.js               # 进度跟踪
│   └── test_tts.html                      # TTS测试页面
├── server.py                              # 发音服务器
├── requirements.txt                       # Python依赖
└── README.md                              # 项目文档
```

## 快速开始

### 环境要求

- Python 3.7+
- macOS系统（发音功能需要）
- 现代浏览器（Chrome、Firefox、Safari等）

### 安装依赖

```bash
pip install -r requirements.txt
```

### 数据处理

1. 构建主数据库（下载汉字表并转换拼音）：

```bash
python scripts/build_master_db.py
```

2. 生成章节数据：

```bash
python scripts/generate_char_data.py
```

3. 生成例词（推荐使用改进版）：

```bash
python scripts/generate_example_words_v3.py
```

### 启动发音服务器

```bash
python server.py
```

服务器将在 `http://localhost:5001` 启动。

### 使用学习系统

1. 打开 `output/frequency_chapters.html` 开始学习
2. 打开 `output/quiz.html` 进行测验
3. 打开 `output/progress.html` 查看进度

## API文档

### 发音服务器API

#### 健康检查
```
GET /api/health
```

返回服务器状态和支持情况。

#### 朗读文本
```
POST /api/speak
Content-Type: application/json

{
  "text": "一 jat1"
}
```

朗读指定的文本。

#### 停止朗读
```
POST /api/stop
```

停止当前的朗读。

#### 获取状态
```
GET /api/status
```

获取当前朗读状态。

## 使用说明

### 学习模式

1. **分章节学习**：按照频率分成的10个章节，从高频到低频逐步学习
2. **全屏学习**：专注模式，减少干扰
3. **发音练习**：点击汉字卡片听发音

### 测验模式

1. 选择章节和题目数量
2. 选择测验类型：
   - 汉字→拼音：根据汉字选择正确的拼音
   - 拼音→汉字：根据拼音选择正确的汉字
   - 混合模式：随机混合两种类型
3. 查看结果和错题回顾

### 进度管理

1. 自动记录学习进度
2. 查看学习统计
3. 智能复习提醒
4. 导出/导入学习数据

## 技术栈

- **后端**：Python + Flask
- **前端**：HTML5 + CSS3 + JavaScript
- **数据处理**：Pandas + ToJyutping
- **发音**：macOS say命令 + Sinji语音包
- **存储**：LocalStorage（前端进度）

## 注意事项

1. **发音功能**：需要macOS系统并安装粤语语音包（Sinji）
   - 检查语音包：`say -v '?' | grep Sinji`
   - 如果没有安装，请在系统设置中添加

2. **数据来源**：汉字表来自GitHub开源项目，可能存在个别字拼音不准确

3. **多音字处理**：当前只取第一个拼音候选，后续版本会改进

4. **浏览器兼容性**：建议使用现代浏览器以获得最佳体验

## 开发计划

- [ ] 支持多音字
- [ ] 添加更多发音选项
- [ ] 集成真实语料库提升例词质量
- [ ] 添加词组学习模式
- [ ] 支持离线使用
- [ ] 添加用户账户系统
- [ ] 移动端优化

## 贡献指南

欢迎提交Issue和Pull Request！

## 许可证

MIT License

## 致谢

- [通用规范汉字表](https://github.com/shengdoushi/common-standard-chinese-characters-table)
- [ToJyutping](https://github.com/jyutping/to-jyutping) - 粤语拼音转换库
- Font Awesome - 图标库

## 联系方式

如有问题或建议，欢迎通过Issue联系。

---

**祝学习愉快！** 🎉
