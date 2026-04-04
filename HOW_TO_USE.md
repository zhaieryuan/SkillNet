# SkillNet 使用指南

## 🎯 重要说明

**SkillNet 不是需要"启动"的 Web 服务项目！**

它是一个：
- ✅ **命令行工具**（CLI）：在终端直接使用 `skillnet` 命令
- ✅ **Python SDK**：在 Python 代码中导入使用
- ✅ **在线平台**：访问 http://skillnet.openkg.cn/

---

## 🚀 三种使用方式

### 方式 1: CLI 命令行（推荐新手）⭐

激活环境后直接使用命令：

```bash
# 1️⃣ 激活虚拟环境
source .venv/bin/activate

# 2️⃣ 使用 skillnet 命令
skillnet --help
```

#### 常用命令示例

```bash
# 🔍 搜索技能
skillnet search "pdf处理" --limit 5
skillnet search "docker" --mode keyword
skillnet search "图像处理和可视化" --mode vector --threshold 0.85

# 📥 下载技能
skillnet download <技能URL> -d ./my_skills
skillnet download <URL> --mirror https://ghfast.top/  # 使用镜像加速

# ✨ 创建技能（需要 API_KEY）
skillnet create --prompt "创建一个图片压缩工具"
skillnet create trajectory.txt -d ./skills
skillnet create --github https://github.com/owner/repo
skillnet create --office tutorial.pdf

# 📊 评估技能（需要 API_KEY）
skillnet evaluate ./my_skills/某个技能
skillnet evaluate <GitHub URL>

# 🕸️ 分析关系（需要 API_KEY）
skillnet analyze ./my_skills
```

---

### 方式 2: Python SDK（推荐开发者）💻

#### 基础示例

创建 Python 文件（如 `my_script.py`）：

```python
from skillnet_ai import SkillNetClient

# 初始化客户端
client = SkillNetClient()

# 搜索技能
results = client.search(q="python", limit=5)
for skill in results:
    print(f"{skill.skill_name}: {skill.skill_description}")

# 下载技能
if results:
    local_path = client.download(
        url=results[0].skill_url,
        target_dir="./my_skills"
    )
    print(f"下载到: {local_path}")
```

运行：

```bash
source .venv/bin/activate
python my_script.py
```

#### 高级功能示例

```python
from skillnet_ai import SkillNetClient
import os

# 初始化（使用环境变量中的 API_KEY）
client = SkillNetClient(
    api_key=os.getenv("API_KEY"),
    github_token=os.getenv("GITHUB_TOKEN")
)

# 创建技能
created_paths = client.create(
    prompt="创建一个 JSON 格式化工具",
    output_dir="./generated_skills"
)

# 评估技能
report = client.evaluate(
    target="./my_skill",
    category="Development"
)
print(f"安全性: {report['safety']['level']}")

# 分析关系
relationships = client.analyze(
    skills_dir="./my_skills",
    save_to_file=True
)
```

---

### 方式 3: 在线 Web 平台 🌐

访问官方网站：**http://skillnet.openkg.cn/**

功能：
- 🔍 在线搜索技能
- 📦 浏览技能详情
- ⬇️ 下载技能包
- 📊 查看评估报告
- 🎓 学习教程和文档

---

## 📋 完整工作流程示例

### 场景：为 AI Agent 构建技能库

```bash
# 1. 激活环境
source .venv/bin/activate

# 2. 搜索所需技能
skillnet search "PDF处理" --limit 3 > search_results.txt

# 3. 下载技能
skillnet download <URL1> -d ./agent_skills
skillnet download <URL2> -d ./agent_skills
skillnet download <URL3> -d ./agent_skills

# 4. 评估技能质量（需要 API_KEY）
export API_KEY="sk-..."
skillnet evaluate ./agent_skills/pdf-parser
skillnet evaluate ./agent_skills/doc-parser

# 5. 分析技能关系
skillnet analyze ./agent_skills

# 6. 查看关系图
cat ./agent_skills/relationships.json
```

---

## 🔧 环境变量配置

### 快速配置（3 步）

#### 1️⃣ 复制配置模板

```bash
cp .env.example .env
```

#### 2️⃣ 编辑 .env 文件

```bash
vim .env  # 或使用您喜欢的编辑器
```

#### 3️⃣ 填写必需配置

**最小配置**（仅搜索和下载）：
```bash
# 无需配置，开箱即用！
```

**基础配置**（创建和评估功能）：
```env
API_KEY=sk-your-openai-api-key-here
SKILLNET_MODEL=gpt-4o
```

**完整配置**（最佳体验）：
```env
API_KEY=sk-your-openai-api-key-here
SKILLNET_MODEL=gpt-4o
GITHUB_TOKEN=ghp-your-github-token-here
GITHUB_MIRROR=https://ghfast.top/
```

### 主要环境变量

| 变量 | 必需 | 说明 |
|------|------|------|
| `API_KEY` | 部分* | OpenAI API Key（创建/评估/分析需要） |
| `SKILLNET_MODEL` | 否 | LLM 模型（默认 gpt-4o） |
| `GITHUB_TOKEN` | 否 | GitHub Token（强烈推荐） |
| `GITHUB_MIRROR` | 否 | GitHub 镜像（国内推荐） |
| `BASE_URL` | 否 | API 基础 URL（代理/第三方服务） |
| `HOST` | 否 | API 服务器地址（默认 0.0.0.0） |
| `PORT` | 否 | API 服务器端口（默认 8000） |

*仅在使用 create/evaluate/analyze 功能时必需

### 在代码中使用

```python
from dotenv import load_dotenv
load_dotenv()  # 自动加载 .env 文件

from skillnet_ai import SkillNetClient
client = SkillNetClient()  # 自动读取环境变量
```

### 📖 详细配置指南

查看完整的环境变量配置说明：**[ENV_SETUP.md](ENV_SETUP.md)**

包含：
- 🔑 如何获取 API Key 和 GitHub Token
- 🤖 模型选择指南（推荐模型、成本对比）
- 💡 配置示例（最小配置、国内环境、企业环境）
- ❓ 常见问题解答
- 🔐 安全最佳实践

---

## 📚 示例代码库

项目自带示例代码，可以直接运行：

```bash
# 查看示例文件
ls examples/

# 运行搜索示例
python examples/search_demo.py

# 运行创建示例（需要 API_KEY）
export API_KEY="sk-..."
python examples/create_example.py

# 运行评估示例
python examples/evaluate_example.py

# 打开 Jupyter 教程
pip install jupyter
jupyter notebook examples/skillnet_usage_demo.ipynb
```

---

## 🎓 学习路径

### 初学者（30 分钟）

1. **运行快速开始**
   ```bash
   source .venv/bin/activate
   python quick_start.py
   ```

2. **尝试搜索命令**
   ```bash
   skillnet search "docker"
   skillnet search "python测试"
   ```

3. **阅读文档**
   ```bash
   open docs/README.md
   ```

### 中级用户（2 小时）

1. 搜索并下载 5 个技能
2. 使用 Python SDK 编写自动化脚本
3. 设置 API_KEY 并创建自己的技能

### 高级用户（5 小时）

1. 阅读源码：`skillnet-ai/src/skillnet_ai/`
2. 运行实验代码：`experiments/`
3. 修改和扩展功能

---

## 🆘 常见问题

### Q1: 提示 "No such command"

**解决**：先激活虚拟环境
```bash
source .venv/bin/activate
```

### Q2: 下载失败（GitHub API 超时）

**解决**：使用镜像加速
```bash
export GITHUB_MIRROR="https://ghfast.top/"
skillnet download <URL> --mirror https://ghfast.top/
```

### Q3: 创建/评估功能报错

**原因**：缺少 API_KEY

**解决**：
```bash
export API_KEY="sk-..."
# 或创建 .env 文件
echo 'API_KEY=sk-...' > .env
```

### Q4: 想看源码和架构

**阅读文档**：
```bash
open docs/02-directory-structure.md  # 目录结构
open docs/04-architecture-design.md  # 架构设计
open docs/05-api-reference.md        # API 参考
```

---

## 🎯 快速命令参考

| 功能 | 命令 |
|------|------|
| 激活环境 | `source .venv/bin/activate` |
| 搜索技能 | `skillnet search "关键词"` |
| 下载技能 | `skillnet download <URL> -d ./dir` |
| 创建技能 | `skillnet create --prompt "描述"` |
| 评估技能 | `skillnet evaluate ./skill` |
| 分析关系 | `skillnet analyze ./skills` |
| 查看帮助 | `skillnet --help` |
| 运行示例 | `python quick_start.py` |

---

## 📖 延伸阅读

- **完整文档**: `docs/README.md`
- **学习路径**: `docs/03-learning-path.md`
- **API 参考**: `docs/05-api-reference.md`
- **安装报告**: `INSTALLATION_REPORT.md`
- **项目概览**: `CLAUDE.md`
- **主 README**: `README.md`

---

## ✅ 总结

**SkillNet 已经"启动"成功了！**

你现在可以：
1. ✅ 使用 CLI 工具搜索技能
2. ✅ 使用 Python SDK 编程
3. ✅ 访问在线平台浏览

**无需启动服务器，直接使用即可！** 🎉

---

**创建时间**: 2026-04-04  
**版本**: skillnet-ai 0.0.17  
**生成工具**: Claude Code
