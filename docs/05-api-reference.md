# API 参考文档

完整的 SkillNet Python SDK 和 CLI 工具 API 文档。

---

## 📦 Python SDK

### SkillNetClient

统一客户端，提供所有核心功能。

#### 初始化

```python
from skillnet_ai import SkillNetClient

client = SkillNetClient(
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    github_token: Optional[str] = None
)
```

**参数**:

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `api_key` | `str` | 否* | `os.getenv("API_KEY")` | OpenAI API Key（create/evaluate/analyze 需要） |
| `base_url` | `str` | 否 | `os.getenv("BASE_URL")` 或 `https://api.openai.com/v1` | LLM API 端点 |
| `github_token` | `str` | 否 | `os.getenv("GITHUB_TOKEN")` | GitHub Token（私有仓库/提高速率） |

\* **注意**: search 和 download（公开仓库）不需要 `api_key`

**示例**:

```python
# 只使用搜索和下载（无需 API Key）
client = SkillNetClient()

# 使用所有功能（需要 API Key）
client = SkillNetClient(api_key="sk-...")

# 自定义 LLM 端点
client = SkillNetClient(
    api_key="sk-...",
    base_url="https://api.deepseek.com/v1"
)
```

---

### search() - 搜索技能

搜索 SkillNet 社区技能。

```python
client.search(
    q: str,
    mode: str = "keyword",
    category: Optional[str] = None,
    limit: int = 20,
    page: int = 1,
    min_stars: int = 0,
    sort_by: str = "stars",
    threshold: float = 0.8
) -> List[Skill]
```

**参数**:

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `q` | `str` | **必需** | 搜索查询（关键词或自然语言） |
| `mode` | `str` | `"keyword"` | 搜索模式：`"keyword"`（关键词） 或 `"vector"`（语义） |
| `category` | `str` | `None` | 按类别过滤（如 "Development", "AIGC"） |
| `limit` | `int` | `20` | 返回结果数量（最大 50） |
| `page` | `int` | `1` | 页码（仅 keyword 模式） |
| `min_stars` | `int` | `0` | 最小 star 数（仅 keyword 模式） |
| `sort_by` | `str` | `"stars"` | 排序方式：`"stars"` 或 `"recent"`（仅 keyword 模式） |
| `threshold` | `float` | `0.8` | 相似度阈值 0.0-1.0（仅 vector 模式） |

**返回**: `List[Skill]` - 技能对象列表

**Skill 对象结构**:

```python
@dataclass
class Skill:
    skill_name: str          # 技能名称
    skill_description: str   # 技能描述
    author: str              # 作者
    stars: int               # Star 数
    skill_url: str           # GitHub URL
    category: str            # 类别
```

**示例**:

```python
# 关键词搜索
results = client.search(
    q="pdf",
    mode="keyword",
    min_stars=5,
    sort_by="stars",
    limit=10
)

# 语义搜索（AI 理解查询意图）
results = client.search(
    q="我需要处理 Excel 文件并生成图表",
    mode="vector",
    threshold=0.85
)

# 按类别过滤
results = client.search(
    q="可视化",
    category="Development"
)

# 处理结果
for skill in results:
    print(f"⭐ {skill.stars} | {skill.skill_name}")
    print(f"   {skill.skill_description}")
    print(f"   {skill.skill_url}\n")
```

**异常**:

- `SkillNetError`: 搜索失败（网络错误、API 错误等）

---

### download() - 下载技能

从 GitHub 下载技能到本地。

```python
client.download(
    url: str,
    target_dir: str = ".",
    token: Optional[str] = None,
    mirror_url: Optional[str] = None
) -> str
```

**参数**:

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `url` | `str` | **必需** | GitHub 技能 URL（文件夹链接） |
| `target_dir` | `str` | `"."` | 本地安装目录 |
| `token` | `str` | `None` | GitHub Token（覆盖初始化时的 token） |
| `mirror_url` | `str` | `None` | GitHub 镜像 URL（如 `https://ghfast.top/`） |

**返回**: `str` - 本地安装路径（绝对路径）

**支持的 URL 格式**:

```
https://github.com/owner/repo/tree/main/path/to/skill
https://github.com/owner/repo/blob/main/path/to/skill
```

**示例**:

```python
# 基本用法
local_path = client.download(
    url="https://github.com/anthropics/skills/tree/main/skills/pdf-parser",
    target_dir="./my_skills"
)
print(f"技能已安装到: {local_path}")
# 输出: 技能已安装到: /path/to/my_skills/pdf-parser

# 私有仓库（需要 token）
local_path = client.download(
    url="https://github.com/my-org/private-repo/tree/main/skills/secret-skill",
    token="ghp_...",
    target_dir="./skills"
)

# 使用镜像加速（国内用户）
local_path = client.download(
    url="https://github.com/...",
    mirror_url="https://ghfast.top/"
)

# 环境变量方式（推荐）
import os
os.environ["GITHUB_MIRROR"] = "https://ghfast.top/"
local_path = client.download(url="...")
```

**异常**:

- `SkillNetError`: 下载失败
  - 403: 速率限制（提示设置 GitHub Token）
  - 404: 资源不存在（检查 URL 或设置 Token）
  - 网络错误、解析错误等

---

### create() - 创建技能

从多种来源自动创建技能包。

```python
client.create(
    input_type: str = "auto",
    trajectory_content: Optional[str] = None,
    github_url: Optional[str] = None,
    office_file: Optional[str] = None,
    prompt: Optional[str] = None,
    output_dir: Union[str, Path] = "./generated_skills",
    model: str = "gpt-4o",
    max_files: int = 50
) -> List[str]
```

**参数**:

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `input_type` | `str` | `"auto"` | 输入类型：`"auto"`（自动检测）、`"trajectory"`、`"github"`、`"office"`、`"prompt"` |
| `trajectory_content` | `str` | `None` | 执行日志/对话轨迹内容 |
| `github_url` | `str` | `None` | GitHub 仓库 URL |
| `office_file` | `str` | `None` | Office 文件路径（PDF/PPT/Word） |
| `prompt` | `str` | `None` | 自然语言描述 |
| `output_dir` | `str/Path` | `"./generated_skills"` | 输出目录 |
| `model` | `str` | `"gpt-4o"` | LLM 模型 |
| `max_files` | `int` | `50` | 最大分析文件数（仅 GitHub 模式） |

**返回**: `List[str]` - 生成的技能目录路径列表

**创建模式**:

#### 1. 从轨迹创建 (trajectory)

**适用场景**: Agent 完成任务后，提取可复用技能

```python
with open("execution_log.txt", "r") as f:
    trajectory = f.read()

created_paths = client.create(
    trajectory_content=trajectory,
    output_dir="./skills"
)

# 或自动检测
created_paths = client.create(
    trajectory_content=trajectory  # input_type="auto" 自动识别
)
```

**轨迹格式示例**:
```
User: 批量重命名所有 .jpg 文件为 .png
Agent: 执行以下步骤：
1. 列出文件: ls *.jpg
2. 重命名: for f in *.jpg; do mv "$f" "${f%.jpg}.png"; done
User: 成功！
```

#### 2. 从 GitHub 创建 (github)

**适用场景**: 将现有代码仓库转化为技能

```python
created_paths = client.create(
    github_url="https://github.com/psf/requests",
    output_dir="./skills",
    max_files=20  # 限制分析文件数（加快速度）
)
```

**注意**:
- 会克隆仓库并分析代码文件
- `max_files` 控制分析的文件数（避免超时）
- 大型仓库建议设置较小的 `max_files`

#### 3. 从 Office 文档创建 (office)

**适用场景**: 从教程、文档中提取技能

```python
created_paths = client.create(
    office_file="./tutorial.pdf",
    output_dir="./skills"
)
```

**支持格式**:
- PDF: `.pdf`
- PowerPoint: `.pptx`, `.ppt`
- Word: `.docx`, `.doc`

#### 4. 从提示创建 (prompt)

**适用场景**: 快速创建自定义技能

```python
created_paths = client.create(
    prompt="创建一个用于爬取网页标题的技能，使用 requests 和 BeautifulSoup",
    output_dir="./skills"
)
```

**示例**:

```python
# 完整示例
from skillnet_ai import SkillNetClient

client = SkillNetClient(api_key="sk-...")

# 创建技能
created_paths = client.create(
    prompt="一个用于压缩图片的技能，支持 JPEG 和 PNG 格式",
    output_dir="./my_skills",
    model="gpt-4o"
)

print(f"创建了 {len(created_paths)} 个技能:")
for path in created_paths:
    print(f"  - {path}")

# 查看生成的文件
import os
for path in created_paths:
    print(f"\n{path}:")
    for file in os.listdir(path):
        print(f"  - {file}")
```

**生成的技能结构**:
```
image-compressor/
├── SKILL.md              # 技能描述
├── compress.py           # 主要代码
├── requirements.txt      # 依赖
└── examples/
    └── example.py        # 使用示例
```

**异常**:

- `SkillNetError`: 
  - `"API_KEY is required for skill creation"`: 缺少 API Key
  - `"Must provide one of: trajectory_content, github_url, ..."`: 未提供输入源
  - LLM 调用失败、解析失败等

---

### evaluate() - 评估技能

对技能进行 5 维度质量评估。

```python
client.evaluate(
    target: str,
    name: Optional[str] = None,
    category: Optional[str] = None,
    description: Optional[str] = None,
    model: str = "gpt-4o",
    max_workers: int = 5,
    cache_dir: Union[str, Path] = "./evaluate_cache_dir"
) -> Dict[str, Any]
```

**参数**:

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `target` | `str` | **必需** | 本地路径或 GitHub URL |
| `name` | `str` | `None` | 覆盖技能名称 |
| `category` | `str` | `None` | 覆盖技能类别 |
| `description` | `str` | `None` | 覆盖技能描述 |
| `model` | `str` | `"gpt-4o"` | LLM 模型 |
| `max_workers` | `int` | `5` | 并发数（5个维度并行） |
| `cache_dir` | `str/Path` | `"./evaluate_cache_dir"` | 缓存目录 |

**返回**: `Dict[str, Any]` - 评估报告

**评估报告结构**:

```python
{
    "safety": {
        "level": "Good",      # Excellent/Good/Fair/Poor/Bad
        "reason": "无恶意代码，但缺少输入验证"
    },
    "completeness": {
        "level": "Excellent",
        "reason": "文档齐全，依赖明确，包含示例"
    },
    "executability": {
        "level": "Good",
        "reason": "语法正确，可以运行，但缺少测试"
    },
    "maintainability": {
        "level": "Fair",
        "reason": "函数过长，注释不足"
    },
    "cost_awareness": {
        "level": "Good",
        "reason": "使用批处理，但缺少缓存"
    }
}
```

**示例**:

```python
# 评估本地技能
report = client.evaluate(
    target="./my_skills/pdf-parser",
    category="Development"
)

# 评估远程技能
report = client.evaluate(
    target="https://github.com/anthropics/skills/tree/main/skills/pdf-parser"
)

# 打印评估结果
for dimension, result in report.items():
    print(f"\n{dimension.upper()}:")
    print(f"  等级: {result['level']}")
    print(f"  原因: {result['reason']}")

# 计算总分
level_scores = {"Excellent": 5, "Good": 4, "Fair": 3, "Poor": 2, "Bad": 1}
total_score = sum(level_scores[r['level']] for r in report.values())
avg_score = total_score / len(report)
print(f"\n平均分: {avg_score:.2f}/5.00")
```

**缓存机制**:

- 评估结果会缓存到 `cache_dir`
- 相同技能内容不会重复评估
- 手动清除缓存: `rm -rf ./evaluate_cache_dir`

**异常**:

- `SkillNetError`: 
  - `"API_KEY is required for evaluation"`: 缺少 API Key
  - 下载失败、LLM 调用失败等

---

### analyze() - 分析技能关系

分析本地技能目录中的技能关系。

```python
client.analyze(
    skills_dir: Union[str, Path],
    save_to_file: bool = True,
    model: str = "gpt-4o"
) -> List[Dict[str, Any]]
```

**参数**:

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `skills_dir` | `str/Path` | **必需** | 技能目录路径 |
| `save_to_file` | `bool` | `True` | 是否保存为 `relationships.json` |
| `model` | `str` | `"gpt-4o"` | LLM 模型 |

**返回**: `List[Dict[str, Any]]` - 关系列表

**关系对象结构**:

```python
{
    "source": "pdf-parser",
    "target": "text-summarizer",
    "type": "compose_with",  # similar_to/belong_to/compose_with/depend_on
    "reason": "PDF 解析后的文本可以输入到摘要器生成摘要"
}
```

**关系类型**:

| 类型 | 含义 | 示例 |
|------|------|------|
| `similar_to` | 功能相似 | pdf-parser ↔ doc-parser |
| `belong_to` | 归属类别 | pdf-parser → 文档处理 |
| `compose_with` | 可组合使用 | pdf-parser + text-summarizer |
| `depend_on` | 依赖关系 | pdf-parser → file-reader |

**示例**:

```python
# 分析技能关系
relationships = client.analyze(
    skills_dir="./my_skills",
    save_to_file=True
)

print(f"发现 {len(relationships)} 个关系:\n")

# 按类型分组
from collections import defaultdict
by_type = defaultdict(list)
for rel in relationships:
    by_type[rel["type"]].append(rel)

for rel_type, rels in by_type.items():
    print(f"{rel_type}: {len(rels)} 个")
    for rel in rels:
        print(f"  {rel['source']} → {rel['target']}")
        print(f"  原因: {rel['reason']}\n")
```

**输出文件**: `{skills_dir}/relationships.json`

```json
[
  {
    "source": "pdf-parser",
    "target": "doc-parser",
    "type": "similar_to",
    "reason": "都是文档解析工具，功能类似"
  },
  {
    "source": "pdf-parser",
    "target": "text-summarizer",
    "type": "compose_with",
    "reason": "可以组合使用：先解析PDF，再摘要文本"
  }
]
```

**异常**:

- `SkillNetError`: 
  - `"API_KEY is required for relationship analysis"`: 缺少 API Key
  - 目录不存在、LLM 调用失败等

---

## 🖥️ CLI 工具

SkillNet 提供命令行工具 `skillnet`，功能与 SDK 对应。

### 全局选项

```bash
skillnet --help
```

**环境变量**:

| 变量 | 用途 |
|------|------|
| `API_KEY` | OpenAI API Key |
| `BASE_URL` | LLM API 端点 |
| `GITHUB_TOKEN` | GitHub Token |
| `SKILLNET_MODEL` | 默认模型 |
| `GITHUB_MIRROR` | GitHub 镜像 |

---

### skillnet search

搜索技能。

```bash
skillnet search [OPTIONS] QUERY
```

**选项**:

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `QUERY` | `str` | **必需** | 搜索查询 |
| `--mode` | `str` | `keyword` | 搜索模式：keyword/vector |
| `--category` | `str` | - | 按类别过滤 |
| `--limit` | `int` | `10` | 结果数量 |
| `--page` | `int` | `1` | 页码 |
| `--min-stars` | `int` | `0` | 最小 star 数 |
| `--sort-by` | `str` | `stars` | 排序方式：stars/recent |
| `--threshold` | `float` | `0.8` | 相似度阈值（vector 模式） |

**示例**:

```bash
# 基本搜索
skillnet search "pdf"

# 语义搜索
skillnet search "处理 Excel 并生成图表" --mode vector --threshold 0.85

# 过滤和排序
skillnet search "可视化" --category Development --min-stars 10 --sort-by stars --limit 20
```

---

### skillnet download

下载技能。

```bash
skillnet download [OPTIONS] URL
```

**选项**:

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `URL` | `str` | **必需** | GitHub URL |
| `-d, --dir` | `str` | `.` | 下载目录 |
| `--token` | `str` | - | GitHub Token |
| `--mirror` | `str` | - | GitHub 镜像 |

**示例**:

```bash
# 基本下载
skillnet download https://github.com/anthropics/skills/tree/main/skills/pdf-parser

# 指定目录
skillnet download <url> -d ./my_skills

# 使用镜像
skillnet download <url> --mirror https://ghfast.top/

# 私有仓库
skillnet download <url> --token ghp_...
```

---

### skillnet create

创建技能。

```bash
skillnet create [OPTIONS] [SOURCE]
```

**选项**:

| 选项 | 类型 | 说明 |
|------|------|------|
| `SOURCE` | `str` | 轨迹文件路径（默认模式） |
| `--github` | `str` | GitHub 仓库 URL |
| `--office` | `str` | Office 文件路径 |
| `--prompt` | `str` | 自然语言描述 |
| `-d, --dir` | `str` | 输出目录（默认 `./generated_skills`） |
| `--model` | `str` | LLM 模型（默认 `gpt-4o`） |
| `--max-files` | `int` | 最大文件数（GitHub 模式，默认 50） |

**示例**:

```bash
# 从轨迹文件创建
skillnet create trajectory.txt -d ./skills

# 从 GitHub 创建
skillnet create --github https://github.com/owner/repo

# 从 PDF 创建
skillnet create --office tutorial.pdf

# 从提示创建
skillnet create --prompt "一个用于压缩图片的技能"

# 自定义模型
skillnet create --prompt "..." --model gpt-4-turbo
```

---

### skillnet evaluate

评估技能。

```bash
skillnet evaluate [OPTIONS] TARGET
```

**选项**:

| 选项 | 类型 | 说明 |
|------|------|------|
| `TARGET` | `str` | 本地路径或 GitHub URL |
| `--category` | `str` | 技能类别 |
| `--model` | `str` | LLM 模型 |

**示例**:

```bash
# 评估本地技能
skillnet evaluate ./my_skills/pdf-parser

# 评估远程技能
skillnet evaluate https://github.com/anthropics/skills/tree/main/skills/pdf-parser

# 指定类别和模型
skillnet evaluate ./my_skill --category Development --model gpt-4o
```

**输出示例**:

```
评估技能: pdf-parser

╭─────────────────── 评估结果 ───────────────────╮
│                                                 │
│  Safety           ⭐⭐⭐⭐ Good                  │
│  无恶意代码，但缺少输入验证                      │
│                                                 │
│  Completeness     ⭐⭐⭐⭐⭐ Excellent            │
│  文档齐全，依赖明确，包含示例                    │
│                                                 │
│  Executability    ⭐⭐⭐⭐ Good                  │
│  语法正确，可运行，但缺少测试                    │
│                                                 │
│  Maintainability  ⭐⭐⭐ Fair                    │
│  函数过长，注释不足                              │
│                                                 │
│  Cost-Awareness   ⭐⭐⭐⭐ Good                  │
│  使用批处理，但缺少缓存                          │
│                                                 │
╰─────────────────────────────────────────────────╯

平均分: 4.2/5.0
```

---

### skillnet analyze

分析技能关系。

```bash
skillnet analyze [OPTIONS] SKILLS_DIR
```

**选项**:

| 选项 | 类型 | 说明 |
|------|------|------|
| `SKILLS_DIR` | `str` | 技能目录路径 |
| `--no-save` | `flag` | 不保存文件（仅打印） |
| `--model` | `str` | LLM 模型 |

**示例**:

```bash
# 分析并保存
skillnet analyze ./my_skills

# 仅打印不保存
skillnet analyze ./my_skills --no-save

# 自定义模型
skillnet analyze ./my_skills --model gpt-4o
```

**输出示例**:

```
分析技能关系...

发现 12 个关系:

similar_to (4 个):
  pdf-parser → doc-parser
  原因: 都是文档解析工具，功能类似

belong_to (3 个):
  pdf-parser → 文档处理
  原因: PDF 解析属于文档处理类别

compose_with (3 个):
  pdf-parser → text-summarizer
  原因: 可组合使用：先解析PDF，再摘要

depend_on (2 个):
  pdf-parser → file-reader
  原因: PDF 解析依赖文件读取功能

关系已保存到: ./my_skills/relationships.json
```

---

## 🔧 高级用法

### 批量操作

```python
from skillnet_ai import SkillNetClient

client = SkillNetClient(api_key="sk-...")

# 批量搜索和下载
keywords = ["pdf", "excel", "image", "database"]
for keyword in keywords:
    results = client.search(q=keyword, limit=1)
    if results:
        client.download(
            url=results[0].skill_url,
            target_dir=f"./skills/{keyword}"
        )

# 批量评估
import os
from pathlib import Path

skills_dir = Path("./my_skills")
reports = {}

for skill_folder in skills_dir.iterdir():
    if skill_folder.is_dir():
        report = client.evaluate(target=str(skill_folder))
        reports[skill_folder.name] = report

# 保存评估报告
import json
with open("evaluation_reports.json", "w") as f:
    json.dump(reports, f, indent=2, ensure_ascii=False)
```

### 自定义 LLM 端点

```python
# 使用 DeepSeek
client = SkillNetClient(
    api_key="sk-...",
    base_url="https://api.deepseek.com/v1"
)

# 使用本地 Ollama
client = SkillNetClient(
    api_key="ollama",  # 任意值
    base_url="http://localhost:11434/v1"
)

# 使用 Azure OpenAI
client = SkillNetClient(
    api_key="...",
    base_url="https://<your-resource>.openai.azure.com/openai/deployments/<deployment-name>"
)
```

### 错误处理

```python
from skillnet_ai import SkillNetClient, SkillNetError

client = SkillNetClient()

try:
    results = client.search(q="pdf")
except SkillNetError as e:
    print(f"搜索失败: {e}")

try:
    local_path = client.download(url="https://...")
except SkillNetError as e:
    if "403" in str(e):
        print("速率限制，请设置 GitHub Token")
    elif "404" in str(e):
        print("资源不存在，检查 URL")
    else:
        print(f"下载失败: {e}")
```

---

## 📚 完整示例

### 端到端工作流

```python
from skillnet_ai import SkillNetClient
import os

# 1. 初始化
client = SkillNetClient(
    api_key=os.getenv("API_KEY"),
    github_token=os.getenv("GITHUB_TOKEN")
)

# 2. 搜索技能
print("🔍 搜索 PDF 处理技能...")
results = client.search(
    q="PDF 文本提取和分析",
    mode="vector",
    threshold=0.85,
    limit=5
)

# 3. 下载最佳技能
if results:
    best_skill = results[0]
    print(f"\n📦 下载: {best_skill.skill_name}")
    local_path = client.download(
        url=best_skill.skill_url,
        target_dir="./my_skills"
    )
    
    # 4. 评估技能质量
    print("\n📊 评估技能质量...")
    report = client.evaluate(target=local_path)
    
    for dimension, result in report.items():
        print(f"{dimension}: {result['level']}")
    
    # 5. 如果质量不满意，自己创建
    if report["executability"]["level"] in ["Poor", "Bad"]:
        print("\n✨ 质量不佳，创建新技能...")
        created = client.create(
            prompt="一个高质量的 PDF 文本提取和分析技能，支持表格提取",
            output_dir="./my_skills"
        )
        print(f"新技能已创建: {created}")

# 6. 分析所有技能关系
print("\n🕸️ 分析技能关系...")
relationships = client.analyze(
    skills_dir="./my_skills",
    save_to_file=True
)

print(f"\n✅ 完成！发现 {len(relationships)} 个技能关系")
```

---

[← 上一篇: 架构设计](./04-architecture-design.md) | [返回首页](./README.md)
