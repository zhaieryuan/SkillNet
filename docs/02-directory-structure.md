# 目录结构详解

本文档详细说明 SkillNet 项目的目录组织和每个文件的作用。

## 📁 项目总览

```
SkillNet/
├── skillnet-ai/              # 核心 Python SDK 包 (PyPI 发布)
├── examples/                 # 使用示例和教程
├── experiments/              # 学术研究实验代码
├── skills/                   # 技能模板和集成示例
├── images/                   # 项目文档图片
├── docs/                     # 项目文档（本目录）
├── .github/                  # GitHub 配置和工作流
├── README.md                 # 主项目文档
├── LICENSE                   # MIT 许可证
├── .gitignore                # Git 忽略规则
└── CLAUDE.md                 # Claude Code 工作指南
```

---

## 1️⃣ skillnet-ai/ - 核心 SDK 包

这是项目的**核心代码库**，发布到 PyPI 作为 `skillnet-ai` 包。

### 目录结构

```
skillnet-ai/
├── pyproject.toml           # 📦 包配置文件
├── README.md                # 📄 SDK 文档
└── src/
    └── skillnet_ai/         # 源代码目录
        ├── __init__.py      # 包入口
        ├── client.py        # 统一客户端
        ├── searcher.py      # 搜索模块
        ├── downloader.py    # 下载模块
        ├── creator.py       # 创建模块
        ├── evaluator.py     # 评估模块
        ├── analyzer.py      # 分析模块
        ├── prompts.py       # Prompt 模板
        ├── models.py        # 数据模型
        └── cli.py           # CLI 工具
```

### 核心文件说明

#### pyproject.toml
**作用**: Python 包配置文件

```toml
[project]
name = "skillnet-ai"
version = "0.0.17"
dependencies = [
    "requests>=2.32.5",
    "openai>=1.109.1",
    "pydantic>=2.12.5",
    # ...
]

[project.scripts]
skillnet = "skillnet_ai.cli:app"  # CLI 命令入口
```

**关键配置**：
- **dependencies**: 运行时依赖
- **scripts**: 定义 `skillnet` 命令

#### client.py - 统一客户端接口

**作用**: 提供 `SkillNetClient` 类，聚合所有功能

```python
class SkillNetClient:
    def __init__(self, api_key, base_url, github_token):
        """初始化客户端"""
    
    def search(self, q, mode, ...):
        """搜索技能 → SkillNetSearcher"""
    
    def download(self, url, target_dir):
        """下载技能 → SkillDownloader"""
    
    def create(self, input_type, ...):
        """创建技能 → SkillCreator"""
    
    def evaluate(self, target, ...):
        """评估技能 → SkillEvaluator"""
    
    def analyze(self, skills_dir, ...):
        """分析关系 → SkillRelationshipAnalyzer"""
```

**设计模式**: 门面模式（Facade），隐藏内部复杂性

#### searcher.py - 搜索引擎

**作用**: 调用 SkillNet API 进行技能搜索

```python
class SkillNetSearcher:
    API_BASE_URL = "http://api-skillnet.openkg.cn/v1"
    
    def search(self, q, mode="keyword", ...):
        """
        mode="keyword": 关键词模糊匹配
        mode="vector": AI 语义搜索
        """
```

**数据流**:
```
用户查询 → SkillNetSearcher → SkillNet API → 技能列表
```

#### downloader.py - GitHub 下载器

**作用**: 从 GitHub URL 下载技能到本地

```python
class SkillDownloader:
    def download(self, folder_url, target_dir):
        """
        1. 解析 GitHub URL
        2. 调用 GitHub API 获取文件列表
        3. 下载所有文件到本地
        4. 返回安装路径
        """
```

**关键功能**:
- 支持 GitHub API Token（提高速率限制）
- 支持镜像加速（GITHUB_MIRROR）
- 递归下载文件夹

#### creator.py - 技能创建器

**作用**: 从 4 种来源创建技能包

```python
class SkillCreator:
    def create_from_trajectory(self, trajectory, output_dir):
        """从执行日志创建"""
    
    def create_from_github(self, github_url, output_dir):
        """从 GitHub 仓库创建"""
    
    def create_from_office(self, file_path, output_dir):
        """从 PDF/PPT/Word 创建"""
    
    def create_from_prompt(self, user_input, output_dir):
        """从自然语言描述创建"""
```

**工作流程**:
```
输入 → LLM 分析 → 生成技能元数据 → 生成技能代码 → 保存文件
```

**LLM 依赖**: 使用 OpenAI API（或兼容端点）

#### evaluator.py - 质量评估器

**作用**: 5 维度质量评分

```python
class SkillEvaluator:
    def evaluate_from_path(self, path, ...):
        """评估本地技能"""
    
    def evaluate_from_url(self, url, ...):
        """评估远程技能（先下载）"""
    
    def _evaluate_dimension(self, dimension, skill_content):
        """评估单个维度（并行执行）"""
```

**评估维度**:
1. **Safety**: 安全性检查
2. **Completeness**: 文档完整性
3. **Executability**: 代码可执行性
4. **Maintainability**: 代码可维护性
5. **Cost-Awareness**: 成本优化意识

**并发策略**: 使用 `ThreadPoolExecutor` 并行评估 5 个维度

#### analyzer.py - 关系分析器

**作用**: 分析技能之间的关系

```python
class SkillRelationshipAnalyzer:
    def analyze_local_skills(self, skills_dir, save_to_file):
        """
        1. 扫描目录中的所有技能
        2. 提取技能名称和描述
        3. LLM 推断技能关系
        4. 返回关系列表
        """
```

**关系类型**:
- `similar_to`: 功能相似
- `belong_to`: 归属某类别
- `compose_with`: 可组合使用
- `depend_on`: 依赖关系

#### prompts.py - Prompt 模板库

**作用**: 存储所有 LLM Prompt 模板

```python
# 技能创建 Prompt
CANDIDATE_METADATA_SYSTEM_PROMPT = "..."
SKILL_CONTENT_USER_PROMPT_TEMPLATE = "..."

# 技能评估 Prompt
SKILL_EVALUATION_PROMPT = "..."

# GitHub 分析 Prompt
GITHUB_SKILL_SYSTEM_PROMPT = "..."
```

**设计原则**: 
- 所有 Prompt 集中管理
- 使用 Template 字符串（支持变量替换）

#### cli.py - 命令行工具

**作用**: 提供 `skillnet` 命令

```python
import typer
from rich import print

app = typer.Typer()

@app.command()
def search(q: str, mode: str = "keyword", ...):
    """搜索技能"""

@app.command()
def download(url: str, target_dir: str = "."):
    """下载技能"""

# ...其他命令
```

**CLI 框架**: Typer（基于类型提示）+ Rich（美化输出）

---

## 2️⃣ examples/ - 使用示例

### 目录结构

```
examples/
├── search_demo.py                      # 搜索和下载示例
├── create_example.py                   # 技能创建示例
├── evaluate_example.py                 # 技能评估示例
├── analyze_example.py                  # 关系分析示例
├── skillnet_usage_demo.ipynb           # Jupyter 综合演示
├── scientific_workflow_demo.ipynb      # 科学工作流案例
└── JiuwenClaw/
    └── README.md                       # JiuwenClaw 集成指南
```

### 文件说明

#### search_demo.py
**内容**: 演示搜索和下载功能

```python
from skillnet_ai import SkillNetClient

client = SkillNetClient()
results = client.search(q="pdf", limit=5)
client.download(url=results[0].skill_url, target_dir="./my_skills")
```

**适合**: 初学者快速上手

#### scientific_workflow_demo.ipynb
**内容**: 端到端科学工作流示例

```
场景: 分析 scRNA-seq 数据找癌症靶点
步骤:
1. Agent 规划任务
2. 搜索相关技能 (cellxgene-census, kegg-database)
3. 评估技能质量
4. 执行技能生成报告
```

**适合**: 了解 SkillNet 在实际场景中的应用

---

## 3️⃣ experiments/ - 学术研究

### 目录结构

```
experiments/
├── requirements.txt           # 实验依赖
├── README.md                  # 实验说明
├── alfworld_run.py            # AlfWorld 环境运行
├── scienceworld_run.py        # ScienceWorld 环境运行
├── webshop_run.py             # WebShop 环境运行
└── src/
    ├── alfworld/              # AlfWorld 适配代码
    │   ├── prompts/
    │   │   └── system_prompt.py
    │   └── alfworld_procedure_code_template.py
    ├── scienceworld/          # ScienceWorld 适配代码
    ├── webshop/               # WebShop 适配代码
    ├── skills/                # 实验技能库
    │   ├── alfworld/          # 19+ AlfWorld 技能
    │   ├── scienceworld/      # ScienceWorld 技能
    │   └── webshop/           # WebShop 技能
    ├── prompt_generator.py    # Prompt 生成工具
    ├── skill.py               # 技能加载器
    └── utils.py               # 工具函数
```

### 实验环境说明

#### AlfWorld (家庭任务模拟)

**任务类型**: 家庭日常任务（如"把苹果放进冰箱"）

**技能示例**:
```
experiments/src/skills/alfworld/
├── alfworld-open-receptacle/      # 打开容器
├── alfworld-object-picker/        # 拾取物体
├── alfworld-navigation-planner/   # 导航规划
├── alfworld-task-verifier/        # 任务验证
└── ... (共 19 个技能)
```

**技能结构**（以 `alfworld-open-receptacle` 为例）:
```
alfworld-open-receptacle/
├── SKILL.md                    # 技能描述
├── receptors/                  # 接收器（输入处理）
│   └── action_sequence_examples.md
└── references/                 # 参考文档
    └── common_receptacles.md
```

#### ScienceWorld (科学实验模拟)

**任务类型**: 科学实验（如"测量物质密度"）

#### WebShop (电子商务)

**任务类型**: 在线购物（如"找到符合要求的产品"）

### 实验运行流程

```python
# alfworld_run.py 示例
from src.skill import load_skills
from src.prompt_generator import generate_prompt

# 1. 加载技能
skills = load_skills("./src/skills/alfworld")

# 2. 生成 Prompt
prompt = generate_prompt(task, skills)

# 3. Agent 执行
result = agent.run(prompt)

# 4. 评估结果
score = evaluate(result, ground_truth)
```

---

## 4️⃣ skills/ - 技能模板

### 目录结构

```
skills/
└── skillnet/                  # OpenClaw 集成技能
    ├── SKILL.md               # 技能描述
    ├── scripts/               # 可执行脚本
    │   ├── skillnet_create.py
    │   └── skillnet_validate.py
    └── references/            # 参考文档
```

### SKILL.md 标准格式

```markdown
# Skill: skillnet

## Description
SkillNet integration for OpenClaw

## Usage
```bash
skillnet search "pdf"
```

## Scripts
- `skillnet_create.py`: 创建技能
- `skillnet_validate.py`: 验证技能

## Environment Variables
- `API_KEY`: OpenAI API Key
- `GITHUB_TOKEN`: GitHub Token
```

---

## 5️⃣ 其他重要文件

### CLAUDE.md
**作用**: 为 Claude Code 提供项目工作指南

**内容**:
- 项目架构概览
- 核心模块说明
- 开发命令
- 环境变量配置

**使用场景**: Claude Code 打开项目时自动读取

### .github/workflows/
**作用**: GitHub Actions 自动化工作流

**可能包含**:
- CI/CD 测试
- 自动发布到 PyPI
- 文档自动部署

### LICENSE
**许可证**: MIT License

**含义**: 
- 可自由使用、修改、分发
- 需保留版权声明
- 无担保条款

---

## 📊 目录大小和重要性

| 目录 | 代码量 | 重要性 | 更新频率 |
|------|--------|--------|----------|
| `skillnet-ai/` | ⭐⭐⭐⭐⭐ | 🔥🔥🔥🔥🔥 | 高 |
| `examples/` | ⭐⭐ | 🔥🔥🔥 | 中 |
| `experiments/` | ⭐⭐⭐⭐ | 🔥🔥 | 低 |
| `skills/` | ⭐ | 🔥🔥 | 低 |
| `docs/` | ⭐⭐ | 🔥🔥🔥🔥 | 中 |

---

## 🎯 快速定位指南

| 我想... | 应该查看... |
|---------|-------------|
| 了解搜索实现 | `skillnet-ai/src/skillnet_ai/searcher.py` |
| 了解创建流程 | `skillnet-ai/src/skillnet_ai/creator.py` |
| 查看评估逻辑 | `skillnet-ai/src/skillnet_ai/evaluator.py` |
| 学习如何使用 | `examples/*.py` 和 `*.ipynb` |
| 运行实验 | `experiments/*_run.py` |
| 查看技能结构 | `experiments/src/skills/alfworld/*` |
| 修改 Prompt | `skillnet-ai/src/skillnet_ai/prompts.py` |
| 添加新命令 | `skillnet-ai/src/skillnet_ai/cli.py` |

---

[← 上一篇: 项目概览](./01-project-overview.md) | [返回首页](./README.md) | [下一篇: 学习路径 →](./03-learning-path.md)
