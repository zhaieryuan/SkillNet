# SkillNet 项目概览

## 🎯 项目简介

**SkillNet** 是一个开源平台，将 AI Agent 技能视为一等公民、可共享的包——**类似于 AI 能力的 npm**。

它提供端到端工具来**搜索**、**安装**、**创建**、**评估**和**组织**技能，让 AI Agent 能够从社区学习并持续成长。

### 核心理念

```
传统开发者                    AI Agent 开发者
     ↓                              ↓
npm install lodash        skillnet download pdf-parser
     ↓                              ↓
使用现成的包                    使用现成的技能
```

**SkillNet 让技能变得像 npm 包一样易于分享和复用。**

## ✨ 核心功能

### 1. 🔍 搜索技能 (Search)

从 500+ 社区技能中查找你需要的能力。

**支持两种搜索模式**：
- **关键词搜索**: 模糊匹配技能名称和描述
- **语义搜索**: AI 理解你的需求，找到最相关的技能

```bash
# 关键词搜索
skillnet search "pdf" --limit 10

# 语义搜索（更智能）
skillnet search "分析金融报告" --mode vector --threshold 0.85
```

### 2. 📦 安装技能 (Download)

一行命令从 GitHub 下载技能到本地。

```bash
skillnet download https://github.com/anthropics/skills/tree/main/skills/pdf-parser
```

**特点**：
- 无需 API Key（公开技能）
- 支持 GitHub 镜像加速
- 自动处理依赖

### 3. ✨ 创建技能 (Create)

从 4 种来源自动创建结构化技能包：

| 来源 | 说明 | 使用场景 |
|------|------|----------|
| **轨迹/日志** | 执行记录、对话日志 | Agent 完成任务后自动提取技能 |
| **GitHub 仓库** | 开源代码仓库 | 将现有代码转化为技能 |
| **Office 文档** | PDF/PPT/Word | 从教程、文档中提取技能 |
| **自然语言** | 文字描述 | 快速创建自定义技能 |

```bash
# 从执行日志创建
skillnet create trajectory.txt

# 从 GitHub 仓库创建
skillnet create --github https://github.com/owner/repo

# 从 PDF 文档创建
skillnet create --office tutorial.pdf

# 从文字描述创建
skillnet create --prompt "一个用于爬取网页标题的技能"
```

### 4. 📊 评估技能 (Evaluate)

5 维度质量评分系统：

| 维度 | 评估内容 | 权重 |
|------|----------|------|
| **Safety** 安全性 | 有害内容、恶意代码检测 | ⭐⭐⭐⭐⭐ |
| **Completeness** 完整性 | 文档、依赖、错误处理 | ⭐⭐⭐⭐ |
| **Executability** 可执行性 | 代码质量、运行能力 | ⭐⭐⭐⭐⭐ |
| **Maintainability** 可维护性 | 代码结构、可读性 | ⭐⭐⭐ |
| **Cost-Awareness** 成本意识 | Token 使用、API 调用优化 | ⭐⭐⭐ |

```bash
skillnet evaluate ./my_skill
# 输出: {"safety": {"level": "Good", "reason": "..."}, ...}
```

### 5. 🕸️ 分析关系 (Analyze)

自动发现技能之间的 4 种关系：

| 关系类型 | 含义 | 示例 |
|----------|------|------|
| `similar_to` | 相似技能 | pdf-parser ↔ doc-parser |
| `belong_to` | 归属关系 | pdf-parser → 文档处理类 |
| `compose_with` | 组合使用 | pdf-parser + text-summarizer |
| `depend_on` | 依赖关系 | pdf-parser → file-reader |

```bash
skillnet analyze ./my_skills
# 输出: relationships.json (技能关系图)
```

## 🏗️ 技术架构

### 系统组成

```
┌─────────────────────────────────────────┐
│         SkillNet 平台                    │
├─────────────────────────────────────────┤
│  1. Web 界面 (http://skillnet.openkg.cn)│
│  2. REST API (搜索、下载)                │
│  3. Python SDK (所有功能)                │
│  4. CLI 工具 (命令行)                    │
└─────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│         技能生态系统                      │
├─────────────────────────────────────────┤
│  • 500+ 社区技能                         │
│  • GitHub 技能仓库                       │
│  • 技能关系图谱                          │
└─────────────────────────────────────────┘
```

### 核心模块

```python
from skillnet_ai import SkillNetClient

client = SkillNetClient(
    api_key="sk-...",      # create/evaluate/analyze 需要
    github_token="ghp-..." # 私有仓库需要
)

# 6 大核心功能
client.search()     # 搜索技能
client.download()   # 下载技能
client.create()     # 创建技能
client.evaluate()   # 评估技能
client.analyze()    # 分析关系
```

## 🎓 应用场景

### 场景 1: Agent 开发者

**需求**: 为 AI Agent 快速添加新能力

```python
# 1. 搜索现有技能
results = client.search(q="PDF 提取", mode="vector")

# 2. 下载并使用
client.download(url=results[0].skill_url, target_dir="./agent/skills")

# 3. Agent 立即获得 PDF 处理能力
```

### 场景 2: 研究人员

**需求**: 评估和比较不同技能的质量

```python
# 批量评估多个技能
skills = ["skill-a", "skill-b", "skill-c"]
for skill in skills:
    report = client.evaluate(target=f"./skills/{skill}")
    print(f"{skill}: {report['safety']['level']}")
```

### 场景 3: 科学工作流

**需求**: 从原始数据到科学发现的完整流程

```
用户: "分析 scRNA-seq 数据找到癌症靶点"
  ↓
Agent 规划: 数据 → 机制 → 验证 → 报告
  ↓
搜索技能: cellxgene-census, kegg-database
  ↓
评估质量: 确保技能可靠
  ↓
执行流程: 生成发现报告
```

完整示例见: [examples/scientific_workflow_demo.ipynb](../examples/scientific_workflow_demo.ipynb)

## 🌐 集成方式

### 1. OpenClaw 集成

SkillNet 作为 OpenClaw 的内置技能：

```bash
# 安装
clawhub install skillnet

# Agent 自动使用
"搜索一个 Docker 技能并总结"
```

### 2. MCP 集成

支持 Claude Desktop、Cursor、Windsurf 等 IDE：

```json
{
  "mcpServers": {
    "skillnet": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "fmdogancan/skillnet-mcp:latest"]
    }
  }
}
```

### 3. 直接集成

在你的 Python 项目中：

```python
pip install skillnet-ai

from skillnet_ai import SkillNetClient
# 开始使用
```

## 📊 项目数据

| 指标 | 数据 |
|------|------|
| 社区技能数量 | 500+ |
| GitHub Stars | 持续增长 |
| PyPI 下载量 | 见徽章 |
| 支持的 AI 框架 | OpenClaw, MCP, 自定义 |
| 论文引用 | [arXiv:2603.04448](https://arxiv.org/abs/2603.04448) |

## 🎯 核心价值

### 对个人开发者
- ✅ 避免重复造轮子
- ✅ 快速为 Agent 添加能力
- ✅ 学习社区最佳实践

### 对团队
- ✅ 统一技能管理
- ✅ 质量评估和筛选
- ✅ 技能复用和积累

### 对研究者
- ✅ 基准测试和比较
- ✅ 新方法验证
- ✅ 开源数据集

## 🚀 下一步

- **普通用户**: 阅读 [学习路径](./03-learning-path.md) 快速上手
- **开发者**: 查看 [架构设计](./04-architecture-design.md) 理解实现
- **研究者**: 浏览 [目录结构](./02-directory-structure.md) 了解实验代码

## 📚 相关资源

- **官网**: http://skillnet.openkg.cn/
- **论文**: https://arxiv.org/abs/2603.04448
- **GitHub**: https://github.com/zjunlp/SkillNet
- **PyPI**: https://pypi.org/project/skillnet-ai/
- **HuggingFace**: https://huggingface.co/blog/xzwnlp/skillnet

---

[返回文档首页](./README.md) | [下一篇: 目录结构详解 →](./02-directory-structure.md)
