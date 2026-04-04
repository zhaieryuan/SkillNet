# SkillNet 学习路径

本文档提供从零开始学习 SkillNet 的完整路径，分为**用户**、**开发者**和**研究者**三个学习轨道。

---

## 🎯 选择你的学习轨道

### 👤 用户轨道
**适合**: 想使用 SkillNet 搜索和安装技能的普通用户

**时间**: 30 分钟 - 1 小时

**目标**: 能够搜索、下载、使用社区技能

### 💻 开发者轨道
**适合**: 想贡献代码、集成 SkillNet 或自定义功能的开发者

**时间**: 3 - 5 小时

**目标**: 理解架构、能够修改源码、添加新功能

### 🔬 研究者轨道
**适合**: 想进行学术研究、运行实验、发表论文的研究人员

**时间**: 5 - 10 小时

**目标**: 运行基准测试、理解评估方法、复现论文结果

---

## 👤 用户学习路径

### 第 1 步: 安装 SkillNet (5 分钟)

#### 方法 1: 通过 pip 安装（推荐）

```bash
pip install skillnet-ai
```

验证安装:
```bash
skillnet --help
```

#### 方法 2: 从源码安装

```bash
git clone https://github.com/zjunlp/SkillNet.git
cd SkillNet
pip install -e skillnet-ai/
```

### 第 2 步: 搜索技能 (10 分钟)

#### 使用 CLI

```bash
# 关键词搜索
skillnet search "pdf" --limit 5

# 语义搜索（更智能）
skillnet search "处理 Excel 文件" --mode vector --threshold 0.85

# 按类别过滤
skillnet search "可视化" --category "Development" --sort-by stars
```

#### 使用 Python SDK

创建文件 `test_search.py`:

```python
from skillnet_ai import SkillNetClient

# 初始化（搜索不需要 API Key）
client = SkillNetClient()

# 搜索技能
results = client.search(
    q="pdf 提取",
    mode="keyword",  # 或 "vector"
    limit=10
)

# 打印结果
for skill in results:
    print(f"⭐ {skill.stars} | {skill.skill_name}")
    print(f"   {skill.skill_description}")
    print(f"   URL: {skill.skill_url}\n")
```

运行:
```bash
python test_search.py
```

**练习任务**:
- ✅ 搜索 "docker" 相关技能
- ✅ 使用语义搜索找到 "图像处理" 技能
- ✅ 找到 star 数最多的技能

### 第 3 步: 下载技能 (10 分钟)

#### 使用 CLI

```bash
# 下载单个技能
skillnet download https://github.com/anthropics/skills/tree/main/skills/pdf-parser

# 指定下载目录
skillnet download <url> -d ./my_agent/skills

# 使用镜像加速（国内用户）
skillnet download <url> --mirror https://ghfast.top/
```

#### 使用 Python SDK

```python
from skillnet_ai import SkillNetClient

client = SkillNetClient()

# 搜索并下载
results = client.search(q="pdf", limit=1)
if results:
    local_path = client.download(
        url=results[0].skill_url,
        target_dir="./my_skills"
    )
    print(f"✅ 技能已安装到: {local_path}")
```

**练习任务**:
- ✅ 下载一个 PDF 处理技能
- ✅ 查看下载后的文件结构
- ✅ 尝试运行技能中的示例代码

### 第 4 步: 在线体验 (可选, 5 分钟)

访问 **[SkillNet 网站](http://skillnet.openkg.cn/)**:

1. **搜索技能**: 在搜索框输入关键词
2. **浏览类别**: 点击不同的技能类别
3. **查看详情**: 点击技能查看描述、代码、评分
4. **下载技能**: 点击下载按钮获取技能

### 第 5 步: 实战练习 (20 分钟)

#### 练习 1: 构建技能库

**目标**: 为你的 Agent 构建一个包含 5 个技能的技能库

```python
from skillnet_ai import SkillNetClient

client = SkillNetClient()

# 技能需求列表
skill_needs = [
    "PDF 文本提取",
    "图像处理",
    "数据库操作",
    "网页爬取",
    "邮件发送"
]

# 搜索并下载
for need in skill_needs:
    results = client.search(q=need, mode="vector", limit=1)
    if results:
        print(f"正在下载: {results[0].skill_name}")
        client.download(
            url=results[0].skill_url,
            target_dir="./my_agent_skills"
        )
```

#### 练习 2: 技能对比

**目标**: 对比两个相似技能

```python
# 搜索两个 PDF 技能
results = client.search(q="pdf", limit=2)

for skill in results:
    print(f"\n技能: {skill.skill_name}")
    print(f"作者: {skill.author}")
    print(f"Star: {skill.stars}")
    print(f"描述: {skill.skill_description}")
```

**思考**:
- 哪个技能更受欢迎？（star 数）
- 哪个技能功能更丰富？（描述）
- 你会选择哪个？为什么？

### 🎓 用户轨道完成！

**你现在可以**:
- ✅ 搜索社区技能
- ✅ 下载技能到本地
- ✅ 为 Agent 构建技能库

**下一步**:
- 学习如何创建技能 → [开发者轨道](#-开发者学习路径)
- 了解技能评估 → [研究者轨道](#-研究者学习路径)

---

## 💻 开发者学习路径

**前置要求**: 完成 [用户轨道](#-用户学习路径)

### 第 1 步: 环境配置 (15 分钟)

#### 克隆仓库

```bash
git clone https://github.com/zjunlp/SkillNet.git
cd SkillNet
```

#### 安装开发依赖

```bash
# 安装核心包（可编辑模式）
pip install -e skillnet-ai/

# 安装实验依赖（可选）
pip install -r experiments/requirements.txt
```

#### 配置环境变量

创建 `.env` 文件（项目根目录）:

```bash
# 必需（创建、评估功能）
API_KEY=sk-...

# 可选
BASE_URL=https://api.openai.com/v1
GITHUB_TOKEN=ghp_...
SKILLNET_MODEL=gpt-4o
GITHUB_MIRROR=https://ghfast.top/
```

加载环境变量:

```python
from dotenv import load_dotenv
load_dotenv()
```

### 第 2 步: 阅读核心代码 (1 - 2 小时)

#### 2.1 理解客户端入口 (15 分钟)

阅读 `skillnet-ai/src/skillnet_ai/client.py`:

```python
class SkillNetClient:
    def __init__(self, api_key, base_url, github_token):
        # 1. 存储配置
        self.api_key = api_key
        self.base_url = base_url
        self.github_token = github_token
    
    def search(self, ...):
        # 2. 委托给 SkillNetSearcher
        searcher = SkillNetSearcher()
        return searcher.search(...)
    
    # ... 其他方法类似
```

**关键理解**:
- 客户端是**门面模式**（Facade）
- 每个方法委托给专门的模块
- 不做复杂逻辑，只做协调

#### 2.2 深入搜索模块 (15 分钟)

阅读 `skillnet-ai/src/skillnet_ai/searcher.py`:

```python
class SkillNetSearcher:
    API_BASE_URL = "http://api-skillnet.openkg.cn/v1"
    
    def search(self, q, mode, ...):
        # 1. 构建请求参数
        params = {
            "q": q,
            "mode": mode,
            # ...
        }
        
        # 2. 调用 API
        response = requests.get(f"{self.API_BASE_URL}/search", params=params)
        
        # 3. 解析响应
        data = response.json()
        return [Skill(**item) for item in data["data"]]
```

**关键理解**:
- 纯 HTTP 客户端，调用远程 API
- 无复杂逻辑，只做数据转换

#### 2.3 分析创建模块 (30 分钟)

阅读 `skillnet-ai/src/skillnet_ai/creator.py`:

**重点关注**:

1. **多源创建策略**:
```python
def create(self, input_type, ...):
    if input_type == "trajectory":
        return self.create_from_trajectory(...)
    elif input_type == "github":
        return self.create_from_github(...)
    # ...
```

2. **LLM 调用流程**:
```python
def create_from_trajectory(self, trajectory, output_dir):
    # Step 1: 提取技能元数据
    meta_prompt = CANDIDATE_METADATA_USER_PROMPT_TEMPLATE.format(
        trajectory=trajectory
    )
    meta_response = self._get_llm_response([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": meta_prompt}
    ])
    
    # Step 2: 生成技能内容
    for skill_meta in parsed_skills:
        content_prompt = SKILL_CONTENT_USER_PROMPT_TEMPLATE.format(...)
        content_response = self._get_llm_response([...])
        
        # Step 3: 保存文件
        self._save_skill_files(content_response, output_dir)
```

**关键理解**:
- 两阶段生成：元数据 → 内容
- 使用 Prompt 模板（在 `prompts.py`）
- LLM 返回结构化 JSON，解析后保存

#### 2.4 探索评估模块 (30 分钟)

阅读 `skillnet-ai/src/skillnet_ai/evaluator.py`:

**重点关注**:

1. **5 维度并行评估**:
```python
def evaluate_from_path(self, path, ...):
    dimensions = ["safety", "completeness", "executability", 
                  "maintainability", "cost_awareness"]
    
    # 并行评估
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(self._evaluate_dimension, dim, skill_content): dim
            for dim in dimensions
        }
        
        for future in as_completed(futures):
            dim = futures[future]
            result[dim] = future.result()
```

2. **单维度评估流程**:
```python
def _evaluate_dimension(self, dimension, skill_content):
    prompt = SKILL_EVALUATION_PROMPT.format(
        dimension=dimension,
        content=skill_content
    )
    
    response = self.client.chat.completions.create(...)
    
    # 解析为: {"level": "Good", "reason": "..."}
    return json.loads(response)
```

**关键理解**:
- 并发提高效率（5 个维度同时评估）
- 每个维度独立打分
- 结果结构化（便于比较）

### 第 3 步: 创建技能实战 (1 小时)

#### 练习 1: 从轨迹创建技能

**场景**: Agent 完成了一个任务，你想提取为技能

创建 `trajectory.txt`:
```
User: 重命名所有 .jpg 文件为 .png
Agent: 好的，我将执行以下步骤：
1. 列出当前目录的 .jpg 文件
   命令: ls *.jpg
2. 批量重命名
   命令: for f in *.jpg; do mv "$f" "${f%.jpg}.png"; done
User: 成功！
```

创建技能:
```python
from skillnet_ai import SkillNetClient

client = SkillNetClient(api_key="sk-...")

with open("trajectory.txt", "r") as f:
    trajectory = f.read()

created_paths = client.create(
    trajectory_content=trajectory,
    output_dir="./generated_skills"
)

print(f"技能已创建: {created_paths}")
```

#### 练习 2: 从 GitHub 仓库创建技能

```python
created_paths = client.create(
    github_url="https://github.com/psf/requests",
    output_dir="./generated_skills",
    max_files=20  # 限制分析文件数
)
```

**思考**:
- 生成的技能结构是什么？
- SKILL.md 文件内容准确吗？
- 代码是否可执行？

### 第 4 步: 评估技能实战 (30 分钟)

#### 评估本地技能

```python
from skillnet_ai import SkillNetClient

client = SkillNetClient(api_key="sk-...")

# 评估刚才创建的技能
report = client.evaluate(
    target="./generated_skills/batch-rename",
    category="Automation"
)

# 打印评估报告
for dimension, result in report.items():
    print(f"\n{dimension.upper()}:")
    print(f"  等级: {result['level']}")
    print(f"  原因: {result['reason']}")
```

#### 评估远程技能

```python
report = client.evaluate(
    target="https://github.com/anthropics/skills/tree/main/skills/pdf-parser"
)
```

**练习任务**:
- ✅ 对比两个相似技能的评估结果
- ✅ 找到评分最低的维度并改进
- ✅ 重新评估看分数是否提高

### 第 5 步: 分析技能关系 (30 分钟)

```python
from skillnet_ai import SkillNetClient

client = SkillNetClient(api_key="sk-...")

# 分析技能目录
relationships = client.analyze(
    skills_dir="./my_skills",
    save_to_file=True  # 保存为 relationships.json
)

# 打印关系
for rel in relationships:
    print(f"{rel['source']} --[{rel['type']}]--> {rel['target']}")
    print(f"  原因: {rel['reason']}\n")
```

**关系可视化**（可选）:

```python
import json
from collections import defaultdict

# 读取关系
with open("./my_skills/relationships.json", "r") as f:
    rels = json.load(f)

# 统计每种关系类型
rel_types = defaultdict(int)
for rel in rels:
    rel_types[rel["type"]] += 1

print("关系统计:")
for rel_type, count in rel_types.items():
    print(f"  {rel_type}: {count}")
```

### 第 6 步: 修改源码（进阶）(1 小时)

#### 示例: 添加新的搜索过滤器

**需求**: 添加按编程语言过滤的功能

1. **修改 `searcher.py`**:

```python
def search(self, q, mode, language=None, ...):  # 新增 language 参数
    params = {
        "q": q,
        "mode": mode,
    }
    
    if language:  # 添加语言过滤
        params["language"] = language
    
    # ... 其余代码
```

2. **修改 `client.py`**:

```python
def search(self, q, mode, language=None, ...):
    searcher = SkillNetSearcher()
    return searcher.search(q=q, mode=mode, language=language, ...)
```

3. **修改 `cli.py`**:

```python
@app.command()
def search(
    q: str,
    language: str = typer.Option(None, help="按编程语言过滤")
):
    client = SkillNetClient()
    results = client.search(q=q, language=language)
```

4. **测试**:

```bash
skillnet search "parser" --language python
```

### 🎓 开发者轨道完成！

**你现在可以**:
- ✅ 理解 SkillNet 架构
- ✅ 创建和评估技能
- ✅ 分析技能关系
- ✅ 修改源码添加新功能

**下一步**:
- 贡献代码到 GitHub
- 集成到你的 Agent 框架
- 发布自己的技能包

---

## 🔬 研究者学习路径

**前置要求**: 完成 [用户轨道](#-用户学习路径)

### 第 1 步: 理解评估方法 (1 小时)

#### 阅读论文

📄 **[SkillNet Technical Report](https://arxiv.org/abs/2603.04448)**

**重点章节**:
- Section 3: 技能创建方法
- Section 4: 多维评估体系
- Section 5: 实验设置和结果

#### 评估维度详解

| 维度 | 评估指标 | 权重 |
|------|----------|------|
| **Safety** | 有害内容检测、恶意代码扫描 | 25% |
| **Completeness** | 文档完整性、依赖声明、错误处理 | 20% |
| **Executability** | 语法正确性、运行能力 | 25% |
| **Maintainability** | 代码可读性、模块化 | 15% |
| **Cost-Awareness** | Token 优化、API 调用效率 | 15% |

### 第 2 步: 环境搭建 (30 分钟)

```bash
# 克隆仓库
git clone https://github.com/zjunlp/SkillNet.git
cd SkillNet

# 安装依赖
pip install -e skillnet-ai/
pip install -r experiments/requirements.txt

# 安装实验环境（根据需要）
pip install alfworld  # AlfWorld
pip install scienceworld  # ScienceWorld
pip install webshop  # WebShop
```

### 第 3 步: 运行基准实验 (2 - 3 小时)

#### 实验 1: AlfWorld 环境

**任务**: 在家庭任务环境中测试技能效果

```bash
cd experiments

# 运行 AlfWorld 实验
python alfworld_run.py --num_episodes 10
```

**观察指标**:
- 任务成功率
- 平均步数
- 技能调用次数

#### 实验 2: 技能质量评估

**任务**: 评估 experiments/src/skills 中的所有技能

创建 `evaluate_all.py`:

```python
import os
from pathlib import Path
from skillnet_ai import SkillNetClient

client = SkillNetClient(api_key="sk-...")

skills_dir = "./experiments/src/skills/alfworld"
results = {}

for skill_folder in Path(skills_dir).iterdir():
    if skill_folder.is_dir():
        print(f"评估: {skill_folder.name}")
        report = client.evaluate(target=str(skill_folder))
        results[skill_folder.name] = report

# 保存结果
import json
with open("evaluation_results.json", "w") as f:
    json.dump(results, f, indent=2)
```

运行:
```bash
python evaluate_all.py
```

#### 实验 3: 技能关系图谱

```python
from skillnet_ai import SkillNetClient

client = SkillNetClient(api_key="sk-...")

# 分析 AlfWorld 技能关系
relationships = client.analyze(
    skills_dir="./experiments/src/skills/alfworld",
    save_to_file=True
)

# 统计关系类型分布
from collections import Counter
rel_types = Counter(r["type"] for r in relationships)
print("关系分布:", rel_types)
```

### 第 4 步: 数据分析 (1 - 2 小时)

#### 分析评估结果

```python
import json
import pandas as pd

# 加载评估结果
with open("evaluation_results.json", "r") as f:
    results = json.load(f)

# 转换为 DataFrame
data = []
for skill_name, report in results.items():
    row = {"skill": skill_name}
    for dim, result in report.items():
        row[f"{dim}_level"] = result["level"]
    data.append(row)

df = pd.DataFrame(data)

# 统计分析
print("维度等级分布:")
for col in df.columns:
    if col.endswith("_level"):
        print(f"\n{col}:")
        print(df[col].value_counts())
```

#### 可视化

```python
import matplotlib.pyplot as plt
import seaborn as sns

# 等级映射
level_map = {"Excellent": 5, "Good": 4, "Fair": 3, "Poor": 2, "Bad": 1}

# 转换为数值
for col in df.columns:
    if col.endswith("_level"):
        df[f"{col}_score"] = df[col].map(level_map)

# 热力图
score_cols = [c for c in df.columns if c.endswith("_score")]
plt.figure(figsize=(12, 8))
sns.heatmap(df[score_cols].T, annot=True, cmap="RdYlGn", vmin=1, vmax=5)
plt.title("技能质量评估热力图")
plt.tight_layout()
plt.savefig("skill_quality_heatmap.png")
```

### 第 5 步: 复现论文结果 (2 - 3 小时)

#### 对比实验设置

**表 1: 不同技能来源的创建成功率**

| 来源 | 成功率（论文） | 你的结果 |
|------|---------------|----------|
| Trajectory | 92% | ? |
| GitHub | 87% | ? |
| Office | 85% | ? |
| Prompt | 79% | ? |

**实验代码**:

```python
from skillnet_ai import SkillNetClient
import os

client = SkillNetClient(api_key="sk-...")

# 准备测试数据
test_cases = {
    "trajectory": ["traj1.txt", "traj2.txt", ...],
    "github": ["https://github.com/...", ...],
    "office": ["doc1.pdf", "doc2.pptx", ...],
    "prompt": ["提示1", "提示2", ...]
}

success_rates = {}

for source, cases in test_cases.items():
    success = 0
    for case in cases:
        try:
            if source == "trajectory":
                with open(case) as f:
                    client.create(trajectory_content=f.read(), ...)
            # ... 其他来源类似
            success += 1
        except Exception as e:
            print(f"失败: {case}, 错误: {e}")
    
    success_rates[source] = success / len(cases) * 100
    print(f"{source}: {success_rates[source]:.1f}%")
```

### 第 6 步: 撰写研究报告 (可选)

#### 报告结构

```markdown
# SkillNet 实验报告

## 1. 研究目标
- 验证技能创建方法的有效性
- 评估技能质量分布
- 分析技能关系图谱

## 2. 实验设置
- 环境: AlfWorld/ScienceWorld/WebShop
- 技能数量: XX 个
- 评估维度: 5 个

## 3. 实验结果
### 3.1 创建成功率
[插入表格和图表]

### 3.2 质量评估
[插入热力图]

### 3.3 关系分析
[插入关系图]

## 4. 结论
- 主要发现
- 与论文对比
- 改进建议

## 5. 参考文献
[1] SkillNet Technical Report (arXiv:2603.04448)
```

### 🎓 研究者轨道完成！

**你现在可以**:
- ✅ 理解 SkillNet 评估方法
- ✅ 运行基准实验
- ✅ 分析实验数据
- ✅ 复现论文结果

**下一步**:
- 发表研究论文
- 提出改进方法
- 贡献新的评估维度

---

## 📚 学习资源

### 官方资源
- **网站**: http://skillnet.openkg.cn/
- **论文**: https://arxiv.org/abs/2603.04448
- **GitHub**: https://github.com/zjunlp/SkillNet
- **HuggingFace**: https://huggingface.co/blog/xzwnlp/skillnet

### 示例代码
- `examples/` - 各功能使用示例
- `examples/*.ipynb` - Jupyter 交互式教程

### 社区
- **Issue 提问**: https://github.com/zjunlp/SkillNet/issues
- **PR 贡献**: https://github.com/zjunlp/SkillNet/pulls

---

## 🎯 学习检查清单

### 用户轨道
- [ ] 安装 SkillNet
- [ ] 成功搜索技能
- [ ] 下载至少 3 个技能
- [ ] 构建自己的技能库

### 开发者轨道
- [ ] 阅读核心代码
- [ ] 创建技能（4种方式各试一次）
- [ ] 评估技能质量
- [ ] 分析技能关系
- [ ] 修改源码添加功能

### 研究者轨道
- [ ] 阅读技术论文
- [ ] 运行基准实验
- [ ] 评估所有技能
- [ ] 数据分析和可视化
- [ ] 复现论文结果

---

[← 上一篇: 目录结构](./02-directory-structure.md) | [返回首页](./README.md) | [下一篇: 架构设计 →](./04-architecture-design.md)
