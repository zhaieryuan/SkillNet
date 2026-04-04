# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

SkillNet 是一个开源平台，将 AI Agent 技能视为一等公民、可共享的包——类似于 AI 能力的 npm。提供端到端工具来**搜索**、**安装**、**创建**、**评估**和**组织**技能。

## 核心架构

### 主要组件

```
skillnet-ai/           # Python SDK 核心包
├── src/skillnet_ai/
│   ├── client.py      # SkillNetClient - 统一客户端接口
│   ├── searcher.py    # 搜索技能（关键词/语义搜索）
│   ├── downloader.py  # 从 GitHub 下载技能
│   ├── creator.py     # 从多源创建技能（轨迹/GitHub/文档/提示）
│   ├── evaluator.py   # 5维度质量评估
│   ├── analyzer.py    # 技能关系图分析
│   ├── prompts.py     # LLM prompt 模板
│   └── models.py      # 数据模型

examples/              # SDK 使用示例
experiments/           # 研究实验（AlfWorld, ScienceWorld, WebShop）
skills/                # 技能模板（如 skillnet/ 用于 OpenClaw 集成）
```

### 设计模式

1. **统一客户端**: `SkillNetClient` 聚合所有功能（搜索、下载、创建、评估、分析）
2. **多源创建**: 支持从 4 种来源创建技能
   - `trajectory`: 执行日志/对话轨迹
   - `github`: GitHub 仓库
   - `office`: PDF/PPT/Word 文档
   - `prompt`: 自然语言描述
3. **LLM 驱动**: 使用 OpenAI API 进行技能创建、评估和关系分析

### 技能评估维度

5 个质量维度（在 `evaluator.py` 中实现）:
- **Safety**: 安全性（有害内容、恶意代码检测）
- **Completeness**: 完整性（文档、依赖、错误处理）
- **Executability**: 可执行性（代码质量、运行能力）
- **Maintainability**: 可维护性（代码结构、可读性）
- **Cost-Awareness**: 成本意识（Token 使用、API 调用优化）

### 技能关系类型

4 种关系（在 `analyzer.py` 中实现）:
- `similar_to`: 相似技能
- `belong_to`: 归属关系（技能 → 类别）
- `compose_with`: 组合关系（协同工作）
- `depend_on`: 依赖关系

## 开发命令

### 安装开发环境

```bash
# 从源码安装（可编辑模式）
pip install -e skillnet-ai/

# 安装实验依赖
pip install -r experiments/requirements.txt
```

### CLI 使用

```bash
# 搜索技能
skillnet search "pdf" --mode keyword --limit 10
skillnet search "analyze financial reports" --mode vector --threshold 0.85

# 下载技能
skillnet download <github_url> -d ./my_skills

# 创建技能
skillnet create trajectory.txt -d ./generated_skills
skillnet create --github https://github.com/owner/repo
skillnet create --office guide.pdf
skillnet create --prompt "A skill for web scraping"

# 评估技能
skillnet evaluate ./my_skill
skillnet evaluate <github_url>

# 分析技能关系
skillnet analyze ./my_skills
```

### Python SDK 使用

```python
from skillnet_ai import SkillNetClient

# 初始化（搜索和下载不需要 API key）
client = SkillNetClient(
    api_key="sk-...",      # create/evaluate/analyze 需要
    github_token="ghp-..." # 私有仓库需要
)

# 搜索
results = client.search(q="pdf", mode="keyword", limit=10)

# 下载
client.download(url=results[0].skill_url, target_dir="./skills")

# 创建（4种方式）
client.create(trajectory_content="...", output_dir="./skills")
client.create(github_url="https://...", output_dir="./skills")
client.create(office_file="guide.pdf", output_dir="./skills")
client.create(prompt="A skill for...", output_dir="./skills")

# 评估
result = client.evaluate(target="./my_skill")

# 分析关系
relationships = client.analyze(skills_dir="./my_skills")
```

## 环境变量

| 变量 | 用途 | 默认值 |
|------|------|--------|
| `API_KEY` | create/evaluate/analyze | - |
| `BASE_URL` | 自定义 LLM 端点 | `https://api.openai.com/v1` |
| `GITHUB_TOKEN` | 私有仓库/提高速率限制 | - |
| `SKILLNET_MODEL` | 默认 LLM 模型 | `gpt-4o` |
| `GITHUB_MIRROR` | 加速下载的镜像 | - |

## 关键实现细节

### SkillCreator (creator.py)

- **轨迹创建**: 解析执行日志 → LLM 提取技能模式 → 生成结构化包
- **GitHub 创建**: 克隆仓库 → 分析代码文件 → LLM 提取核心功能 → 生成技能
- **Office 创建**: 解析 PDF/PPT/Word → LLM 理解内容 → 生成技能
- **提示创建**: 用户描述 → LLM 生成完整技能包

所有创建方法返回 `List[str]`（生成的技能目录路径）

### SkillEvaluator (evaluator.py)

- 支持本地路径和 GitHub URL
- 并行评估 5 个维度（使用 ThreadPoolExecutor）
- 缓存机制（`cache_dir` 参数）
- 返回评估报告字典：`{"safety": {"level": "Good", "reason": "..."}, ...}`

### SkillNetSearcher (searcher.py)

- **关键词模式**: 基于 SkillNet API 的模糊匹配
- **语义模式**: 向量相似度搜索（threshold 参数）
- 支持过滤：category, min_stars, sort_by
- 返回 `List[Skill]` 对象

### SkillDownloader (downloader.py)

- 使用 GitHub API 下载特定文件夹
- 支持镜像加速（`mirror_url` 参数）
- 处理速率限制和认证错误
- 返回本地安装路径

## 集成方式

### OpenClaw 集成
SkillNet 作为内置技能集成到 OpenClaw 中（参见 `skills/skillnet/`）

### MCP 集成
Model Context Protocol 服务器集成（由 CycleChain 维护）

## 实验代码

`experiments/` 包含三个环境的集成研究:
- **AlfWorld**: 家庭任务模拟环境
- **ScienceWorld**: 科学实验环境
- **WebShop**: 电子商务购物环境

每个环境有:
- 运行脚本: `{env}_run.py`
- Prompt 模板: `src/{env}/prompts/`
- 技能模板: `src/skills/{env}/`