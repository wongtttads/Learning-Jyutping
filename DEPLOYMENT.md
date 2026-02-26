# 部署指南

## 概述

粤语拼音学习系统支持多种免费托管平台部署。本指南将详细介绍如何将项目部署到不同的免费平台。

## 部署选项对比

| 平台 | 免费额度 | 后端支持 | 发音方案 | 部署难度 | 推荐度 |
|------|----------|----------|----------|----------|--------|
| GitHub Pages | 完全免费 | ❌ 不支持 | Web Speech API | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Vercel | 免费额度充足 | ✅ 支持（Serverless） | Web Speech API + 可选后端 | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Netlify | 免费额度充足 | ✅ 支持（Serverless） | Web Speech API + 可选后端 | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| 本地部署 | 免费 | ✅ 支持 | macOS say命令 | ⭐ | ⭐⭐⭐ |

## 准备部署

### 1. 安装依赖

在部署前，请确保已安装必要的依赖：

```bash
pip install -r requirements.txt
```

### 2. 生成数据文件

```bash
python scripts/build_master_db.py
python scripts/generate_char_data.py
python scripts/generate_example_words_v3.py
```

### 3. 使用部署准备脚本

我们提供了一个便捷的部署准备脚本：

```bash
./prepare_deploy.sh
```

按照提示选择部署平台，脚本会自动准备相应的部署文件。

## 方案一：GitHub Pages（推荐）

### 优点
- 完全免费，无限流量
- 部署简单，无需服务器
- 自动SSL证书
- 支持自定义域名

### 限制
- 只支持静态文件
- 发音功能使用Web Speech API，粤语支持取决于浏览器
- 无法运行Python后端

### 部署步骤

#### 方法A：使用GitHub Actions（推荐）

1. 将项目推送到GitHub仓库
2. 在仓库设置中启用GitHub Pages：
   - 进入 Settings → Pages
   - Source 选择 "GitHub Actions"
3. 系统会自动使用 `.github/workflows/deploy.yml` 进行部署

#### 方法B：手动部署

1. 生成部署文件：
   ```bash
   ./prepare_deploy.sh
   ```
   选择选项1（GitHub Pages）

2. 将 `_site` 目录内容推送到GitHub仓库的 `gh-pages` 分支

3. 在仓库设置中启用GitHub Pages：
   - 进入 Settings → Pages
   - Source 选择 "gh-pages" 分支
   - 选择根目录 `/`

### 访问地址
- 默认地址：`https://<用户名>.github.io/<仓库名>`
- 支持自定义域名

## 方案二：Vercel

### 优点
- 免费额度充足（100GB带宽/月）
- 支持Serverless函数
- 自动SSL证书
- 全球CDN

### 部署步骤

1. 安装Vercel CLI：
   ```bash
   npm i -g vercel
   ```

2. 部署项目：
   ```bash
   vercel
   ```

3. 按照提示完成部署：
   - 登录Vercel账户
   - 选择项目设置
   - 确认构建设置

4. 生产环境部署：
   ```bash
   vercel --prod
   ```

### 配置文件
项目已包含 `vercel.json` 配置文件，会自动：
- 将Python文件作为Serverless函数
- 将静态文件直接托管
- 配置路由规则

### 访问地址
- 默认地址：`https://<项目名>.vercel.app`
- 支持自定义域名

## 方案三：Netlify

### 优点
- 免费额度充足（100GB带宽/月）
- 支持Serverless函数
- 自动SSL证书
- 表单处理功能

### 部署步骤

1. 将项目推送到GitHub/GitLab仓库

2. 登录Netlify，选择 "New site from Git"

3. 选择仓库，构建设置会自动读取 `netlify.toml`

4. 确认部署设置：
   - Build command: `pip install -r requirements.txt && python scripts/build_master_db.py && python scripts/generate_char_data.py && python scripts/generate_example_words_v3.py`
   - Publish directory: `output`

### Serverless函数
项目包含Netlify函数配置：
- `/api/*` 请求会被转发到 `netlify/functions/server.py`
- 函数会返回Web Speech API指导信息

### 访问地址
- 默认地址：`https://<随机名>.netlify.app`
- 支持自定义域名

## 方案四：本地部署

### 适用于
- 开发测试
- 内部网络使用
- macOS用户（可获得完整发音功能）

### 部署步骤

1. 启动增强版服务器：
   ```bash
   python server_enhanced.py
   ```

2. 访问 `http://localhost:5001`

### 功能说明
- macOS系统：使用系统 `say` 命令，支持粤语发音
- 其他系统：自动切换为Web Speech API模式

## 发音功能说明

### Web Speech API模式
当部署到不支持macOS say命令的环境时，系统会自动使用Web Speech API：

#### 支持情况
- ✅ Chrome 33+
- ✅ Edge 14+
- ✅ Safari 7+
- ✅ Firefox 49+
- ⚠️ 粤语支持取决于浏览器和操作系统

#### 浏览器测试
1. 打开 `scripts/test_tts.html`
2. 点击 "测试朗读" 按钮
3. 查看控制台日志

### 兼容性处理
系统会自动检测环境并选择最佳发音方案：
1. 优先尝试macOS say命令
2. 失败时自动切换到Web Speech API
3. 都不支持时显示拼音文本

## 数据管理

### 数据文件
- `data/processed/jyutping_master.csv` - 主数据文件
- `output/data/chapter_characters.json` - 章节数据
- `output/data/example_words.json` - 例词数据

### 重新生成数据
如果需要更新或重新生成数据：

```bash
# 清理旧数据
rm -rf data/processed/* output/data/*

# 重新生成
python scripts/build_master_db.py
python scripts/generate_char_data.py
python scripts/generate_example_words_v3.py
```

## 自定义配置

### 修改API地址
如需修改发音API地址，编辑以下文件：

1. `scripts/pronunciation_enhanced.js` - 第6行 `apiBaseUrl`
2. 各HTML文件中的API调用

### 添加新功能
1. 前端功能：在 `output/` 目录添加HTML/JS/CSS文件
2. 后端功能：在 `server_enhanced.py` 中添加API端点
3. 数据处理：在 `scripts/` 目录添加Python脚本

## 故障排除

### 常见问题

#### Q1: 部署后发音功能不工作
**原因**: Web Speech API不支持或浏览器限制
**解决方案**:
1. 使用Chrome或Edge浏览器
2. 检查浏览器控制台错误
3. 访问 `chrome://flags/#enable-experimental-web-platform-features` 启用实验功能

#### Q2: GitHub Pages显示404错误
**原因**: 文件路径错误或未正确配置
**解决方案**:
1. 确保有 `.nojekyll` 文件
2. 检查文件路径大小写
3. 确认GitHub Pages已正确配置

#### Q3: Vercel/Netlify构建失败
**原因**: 依赖问题或配置错误
**解决方案**:
1. 检查 `requirements.txt` 格式
2. 查看构建日志
3. 确保Python版本兼容

#### Q4: 数据文件丢失
**原因**: 未正确生成或上传
**解决方案**:
1. 运行数据生成脚本
2. 检查文件是否在部署目录中
3. 确认文件权限

### 日志查看
- 本地服务器：查看终端输出
- GitHub Pages：查看Actions日志
- Vercel：查看部署日志
- Netlify：查看构建日志

## 性能优化

### 前端优化
1. 使用CDN加载公共库
2. 压缩JS/CSS文件
3. 图片懒加载
4. 使用浏览器缓存

### 后端优化
1. 使用Serverless函数按需执行
2. 实现API缓存
3. 优化数据库查询
4. 使用CDN加速静态资源

## 安全注意事项

1. **API密钥**: 不要在代码中硬编码敏感信息
2. **CORS配置**: 生产环境限制跨域请求
3. **输入验证**: 验证所有用户输入
4. **HTTPS**: 确保使用HTTPS协议

## 更新维护

### 定期更新
1. 检查依赖包更新
2. 更新汉字数据
3. 修复安全漏洞
4. 优化性能

### 备份策略
1. 定期备份数据文件
2. 使用Git版本控制
3. 备份配置文件
4. 导出用户学习数据

## 支持与帮助

### 文档资源
1. [README.md](README.md) - 项目说明
2. [QUICKSTART.md](QUICKSTART.md) - 快速开始
3. [IMPROVEMENTS.md](IMPROVEMENTS.md) - 改进记录

### 问题反馈
1. 查看现有Issue
2. 提交新Issue
3. 查看部署日志
4. 浏览器控制台错误

### 社区支持
1. GitHub Discussions
2. 相关技术论坛
3. 开发者社区

---

## 快速参考

### 一键部署命令

```bash
# GitHub Pages
./prepare_deploy.sh  # 选择1，然后推送_site目录

# Vercel
vercel

# Netlify
git push  # 然后在Netlify控制台导入

# 本地测试
python server_enhanced.py
```

### 配置文件位置
- GitHub Pages: `.github/workflows/deploy.yml`
- Vercel: `vercel.json`
- Netlify: `netlify.toml`
- 通用: `prepare_deploy.sh`

### 关键文件
- 主服务器: `server_enhanced.py`
- 发音模块: `scripts/pronunciation_enhanced.js`
- 数据生成: `scripts/build_master_db.py`
- 部署脚本: `prepare_deploy.sh`

---

**祝部署顺利！** 🚀