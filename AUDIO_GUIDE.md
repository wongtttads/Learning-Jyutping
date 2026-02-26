# 预录制发音功能使用指南

## 概述

预录制发音功能为每个汉字生成独立的粤语发音音频文件，确保发音质量一致且准确。

## 系统要求

- macOS系统（使用macOS的`say`命令生成音频）
- Python 3.7+
- 必要的Python依赖：pandas

## 文件结构

```
audio/
├── single_chars/           # 单音字发音文件
│   ├── 一.mp3
│   ├── 乙.mp3
│   └── ...
├── multi_pronunciation/    # 多音字发音文件
│   ├── 行_hang4.mp3
│   ├── 行_hong4.mp3
│   └── ...
└── index.json             # 音频索引文件
```

## 生成音频文件

### 步骤1：安装依赖

```bash
pip install pandas
```

### 步骤2：运行音频生成脚本

```bash
python scripts/generate_audio_files.py
```

### 步骤3：等待生成完成

脚本会自动为所有汉字生成音频文件，包括：
- 单音字：约7000个
- 多音字：约1000个

生成过程可能需要较长时间，请耐心等待。

## 使用预录制发音

### 方法1：在HTML文件中引用

在HTML文件的`<head>`部分添加：

```html
<script src="scripts/pronunciation_audio.js"></script>
```

### 方法2：替换现有发音脚本

将现有的`pronunciation.js`替换为`pronunciation_audio.js`：

```bash
cp scripts/pronunciation_audio.js scripts/pronunciation.js
```

### 方法3：在GitHub Actions中配置

在`.github/workflows/deploy.yml`中更新部署配置：

```yaml
# 更新发音脚本以使用预录制音频
cp scripts/pronunciation_audio.js _site/scripts/pronunciation.js

# 复制音频文件
cp -r audio _site/
```

## 工作原理

### 发音优先级

1. **预录制音频**：优先使用预录制的MP3音频文件
2. **Web Speech API**：如果找不到预录制音频，降级使用浏览器原生的语音合成

### 音频查找逻辑

1. 首先在多音字目录中查找：`audio/multi_pronunciation/{汉字}_{拼音}.mp3`
2. 如果未找到，在单音字目录中查找：`audio/single_chars/{汉字}.mp3`
3. 如果仍未找到，使用Web Speech API作为备选方案

### 音频索引

`audio/index.json`文件包含所有音频文件的元数据：

```json
{
  "version": "1.0",
  "total_count": 7991,
  "single_chars_count": 7000,
  "multi_chars_count": 991,
  "single_chars": [
    {
      "char": "一",
      "jyutping": "jat1",
      "audio_path": "audio/single_chars/一.mp3",
      "type": "single"
    }
  ],
  "multi_chars": [
    {
      "char": "行",
      "jyutping": "hang4",
      "audio_path": "audio/multi_pronunciation/行_hang4.mp3",
      "type": "multi"
    }
  ]
}
```

## 优势

1. **发音质量一致**：所有音频使用相同的TTS引擎生成
2. **跨平台兼容**：MP3格式在所有浏览器中都能播放
3. **离线可用**：音频文件可以缓存，无需网络连接
4. **快速响应**：预录制音频播放速度快于实时TTS
5. **降级方案**：即使某些音频缺失，仍可使用Web Speech API

## 注意事项

### 音频文件大小

- 单个音频文件约10-20KB
- 总计约150-200MB
- 建议使用Git LFS管理大文件

### 生成时间

- 单音字：约2-3小时
- 多音字：约30分钟
- 总计：约3-4小时

### 浏览器兼容性

- 现代浏览器都支持MP3播放
- IE11及以下版本不支持

### GitHub Pages部署

GitHub Pages有100MB的单文件大小限制，但总仓库大小限制为1GB。建议：

1. 使用Git LFS管理音频文件
2. 或者使用CDN托管音频文件
3. 或者只生成高频汉字的音频（前1000个）

## 故障排除

### 音频无法播放

1. 检查音频文件是否存在
2. 检查浏览器控制台是否有错误
3. 确认音频文件路径正确

### 生成音频失败

1. 确认macOS的`say`命令可用
2. 检查是否有足够的磁盘空间
3. 查看错误日志了解具体原因

### 音频质量不佳

1. 尝试使用不同的语音引擎
2. 调整音频编码参数
3. 考虑使用专业录音设备录制

## 进阶使用

### 自定义语音引擎

修改`scripts/generate_audio_files.py`中的`voice`参数：

```python
def generate_audio_file(self, text, output_path, voice="Ting-Ting"):
    # 使用不同的语音引擎
    pass
```

### 调整音频质量

修改音频编码参数：

```python
cmd_convert = [
    'afconvert',
    '-f', 'mp4f',
    '-d', 'mp3',
    '-b', '192000',  # 提高比特率
    str(temp_aiff),
    str(output_path)
]
```

### 批量重新生成

删除现有音频文件后重新生成：

```bash
rm -rf audio/
python scripts/generate_audio_files.py
```

## 总结

预录制发音功能为粤语拼音学习系统提供了高质量的发音支持。通过预生成所有汉字的音频文件，确保了发音的一致性和准确性，同时提供了快速的播放体验。

对于需要高质量发音的项目，强烈建议使用预录制发音方案。
