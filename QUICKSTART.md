# 快速使用指南

## 一、首次使用

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 生成学习数据
```bash
python scripts/build_master_db.py
python scripts/generate_char_data.py
python scripts/generate_example_words_v3.py
```

### 3. 启动发音服务器
```bash
python server.py
```
或者使用启动脚本：
```bash
./start.sh
```

服务器将在 `http://localhost:5000` 启动。

## 二、开始学习

### 方式1：使用启动脚本（推荐）
```bash
./start.sh
```
这个脚本会自动：
- 检查并安装依赖
- 生成数据（如果需要）
- 验证数据质量（可选）
- 启动发音服务器

### 方式2：手动启动
1. 启动发音服务器：`python server.py`
2. 在浏览器中打开学习页面：
   - 分章节学习：`output/frequency_chapters.html`
   - 全屏学习：`output/learning_fullscreen.html`
   - 测验系统：`output/quiz.html`
   - 进度统计：`output/progress.html`

## 三、学习流程建议

### 第一步：浏览学习
1. 打开 `output/frequency_chapters.html`
2. 从第一章开始，逐个学习汉字
3. 点击汉字卡片听发音
4. 查看例词帮助记忆

### 第二步：测验巩固
1. 打开 `output/quiz.html`
2. 选择要测试的章节
3. 设置题目数量（建议从5题开始）
4. 选择测验类型：
   - 汉字→拼音：适合初学者
   - 拼音→汉字：适合进阶学习
   - 混合模式：全面测试
5. 查看结果和错题回顾

### 第三步：查看进度
1. 打开 `output/progress.html`
2. 查看学习统计
3. 检查需要复习的汉字
4. 导出学习数据备份

## 四、常见问题

### Q: 发音功能不工作？
A: 请确保：
1. 发音服务器已启动（`python server.py`）
2. 使用的是macOS系统
3. 已安装粤语语音包（Sinji）
   - 检查方法：在终端运行 `say -v '?' | grep Sinji`
   - 如果没有，请在系统设置 > 声音 > 文本转语音中添加

### Q: 数据文件不存在？
A: 运行数据生成脚本：
```bash
python scripts/build_master_db.py
python scripts/generate_char_data.py
python scripts/generate_example_words_v3.py
```

### Q: 如何重置学习进度？
A: 打开 `output/progress.html`，点击"重置进度"按钮。

### Q: 如何导出学习数据？
A: 打开 `output/progress.html`，点击"导出进度"按钮。

### Q: 测验分数很低怎么办？
A: 建议：
1. 先回到学习页面复习
2. 专注于错题
3. 减少题目数量，逐步增加
4. 多听发音练习

## 五、学习技巧

### 1. 分阶段学习
- 第一阶段：学习高频字（第1-3章）
- 第二阶段：学习中频字（第4-7章）
- 第三阶段：学习低频字（第8-10章）

### 2. 多感官学习
- 看：观察汉字和拼音
- 听：点击发音听读音
- 说：跟着发音练习
- 写：可以手写汉字加深记忆

### 3. 定期复习
- 使用进度统计页面查看需要复习的汉字
- 每天坚持学习，保持连续学习天数
- 利用测验系统检验学习效果

### 4. 结合例词
- 通过例词理解汉字用法
- 注意多音字的不同发音
- 学习常用词组

## 六、快捷键提示

在学习页面：
- 点击汉字卡片：听发音
- 滚动页面：浏览更多汉字

在测验页面：
- 点击选项：选择答案
- 点击"下一题"：继续测验

## 七、数据管理

### 验证数据质量
```bash
python scripts/validate_data.py
```

### 重新生成数据
```bash
python scripts/build_master_db.py
python scripts/generate_char_data.py
python scripts/generate_example_words_v3.py
```

### 备份学习进度
在进度统计页面点击"导出进度"按钮。

## 八、系统要求

- Python 3.7+
- macOS系统（发音功能需要）
- 现代浏览器（Chrome、Firefox、Safari等）
- 粤语语音包（Sinji）

## 九、获取帮助

如有问题，请查看：
1. README.md - 完整项目文档
2. issue页面 - 提交问题
3. 数据验证报告 - 检查数据质量

---

**祝你学习愉快！** 🎉
