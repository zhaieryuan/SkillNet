# Controller - SkillNet FastAPI Web Interface

## 概述

`controller/` 目录包含 SkillNet 的 FastAPI Web 接口实现，提供 RESTful API 访问所有 SkillNet 功能。

**重要**: 此目录是**新增**的，不影响原有的 CLI 和 SDK 代码。

## 目录结构

```
controller/
├── __init__.py              # 模块初始化，导出 app
├── main.py                  # FastAPI 应用实例、中间件、异常处理
├── dependencies.py          # 依赖注入（认证）
├── background_tasks.py      # 后台任务管理
├── models/                  # API 数据模型
│   ├── __init__.py
│   ├── requests.py          # 请求模型
│   └── responses.py         # 响应模型
└── routes/                  # API 路由
    ├── __init__.py
    ├── search.py            # GET /api/v1/skills/search
    ├── download.py          # POST /api/v1/skills/download
    ├── create.py            # POST /api/v1/skills/create/*
    ├── evaluate.py          # POST /api/v1/skills/evaluate
    ├── analyze.py           # POST /api/v1/skills/analyze
    └── tasks.py             # GET /api/v1/tasks/{task_id}
```

## 与原有代码的关系

### 不改动原有代码

- ✅ `skillnet_ai/cli.py` - CLI 工具保持不变
- ✅ `skillnet_ai/client.py` - SDK 核心保持不变
- ✅ `skillnet_ai/searcher.py` - 搜索功能保持不变
- ✅ `skillnet_ai/downloader.py` - 下载功能保持不变
- ✅ `skillnet_ai/creator.py` - 创建功能保持不变
- ✅ `skillnet_ai/evaluator.py` - 评估功能保持不变
- ✅ `skillnet_ai/analyzer.py` - 分析功能保持不变
- ✅ `skillnet_ai/models.py` - 数据模型保持不变

### 复用原有代码

Controller 通过导入复用 SkillNet SDK：

```python
from skillnet_ai import SkillNetClient
from skillnet_ai.models import SearchResponse, SkillModel, MetaModel
from skillnet_ai.client import SkillNetError
from skillnet_ai.downloader import GitHubAPIError
```

## 启动服务

### 使用项目根目录的启动脚本

```bash
# 从项目根目录启动
cd /Users/zhai/my_project/pycharm_workspaces/SkillNet
source .venv/bin/activate

# 默认端口 8000
python run_api.py

# 自定义端口
PORT=8080 python run_api.py
```

### 使用 uvicorn 命令

```bash
cd /Users/zhai/my_project/pycharm_workspaces/SkillNet
source .venv/bin/activate

# 方式 1: 直接指定模块路径（需要先添加 src 到 PYTHONPATH）
export PYTHONPATH="${PYTHONPATH}:skillnet-ai/src"
uvicorn controller.main:app --reload --port 8080

# 方式 2: 使用项目根目录的启动脚本（推荐）
python run_api.py
```

## API 端点

所有端点都已在 FastAPI 应用中注册，包括：

### 无需认证
- `GET /` - API 信息
- `GET /health` - 健康检查
- `GET /api/v1/skills/search` - 搜索技能
- `POST /api/v1/skills/download` - 下载技能（可选 GitHub Token）
- `GET /api/v1/tasks/{task_id}` - 查询任务状态

### 需要 X-API-Key 认证
- `POST /api/v1/skills/create/prompt` - 从提示创建
- `POST /api/v1/skills/create/github` - 从 GitHub 创建
- `POST /api/v1/skills/create/trajectory` - 从轨迹文件创建
- `POST /api/v1/skills/create/office` - 从 Office 文档创建
- `POST /api/v1/skills/evaluate` - 评估技能
- `POST /api/v1/skills/analyze` - 分析关系

## 文档访问

启动服务后，访问：

- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc
- **OpenAPI JSON**: http://localhost:8080/openapi.json

## 测试示例

### 健康检查

```bash
curl http://localhost:8080/health
```

### 搜索技能

```bash
curl "http://localhost:8080/api/v1/skills/search?q=pdf&limit=3"
```

### 创建技能（需要 API Key）

```bash
curl -X POST "http://localhost:8080/api/v1/skills/create/prompt" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk-..." \
  -d '{"prompt": "创建一个工具"}'
```

## 包管理

### 导入规则

在 `controller/` 目录中：

1. **导入 SkillNet SDK**: 使用绝对导入
   ```python
   from skillnet_ai import SkillNetClient
   from skillnet_ai.models import SearchResponse
   ```

2. **导入 Controller 内部模块**: 使用绝对导入
   ```python
   from controller.dependencies import get_api_key
   from controller.models import DownloadRequest
   from controller.background_tasks import create_task
   ```

3. **导入同级模块**: 使用相对导入
   ```python
   from .dependencies import get_api_key
   from .models import TaskResponse
   ```

### Python 路径配置

项目根目录的 `run_api.py` 脚本自动将 `skillnet-ai/src` 添加到 Python 路径：

```python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "skillnet-ai", "src"))
```

这样 `controller` 模块和 `skillnet_ai` 模块都可以正常导入。

## 开发指南

### 添加新端点

1. 在 `routes/` 目录创建新文件，如 `routes/new_feature.py`
2. 定义路由器和端点：
   ```python
   from fastapi import APIRouter
   
   router = APIRouter(prefix="/api/v1/new", tags=["New Feature"])
   
   @router.get("/endpoint")
   async def new_endpoint():
       return {"message": "Hello"}
   ```
3. 在 `main.py` 中注册路由：
   ```python
   from .routes import new_feature
   app.include_router(new_feature.router)
   ```

### 添加新的请求/响应模型

1. 在 `models/requests.py` 或 `models/responses.py` 中定义 Pydantic 模型
2. 在 `models/__init__.py` 中导出
3. 在路由中使用

## 技术栈

- **FastAPI**: Web 框架
- **Pydantic**: 数据验证
- **Uvicorn**: ASGI 服务器
- **python-multipart**: 文件上传支持

## 依赖关系

```
controller/
  ↓ 依赖
skillnet_ai/ (原有 SDK)
  ↓ 使用
原有的所有功能
```

Controller 是一个**薄层包装**，将 SkillNet SDK 的功能暴露为 HTTP API。

## 与 api/ 目录的关系

- `api/` 目录是之前的实现（用于参考）
- `controller/` 目录是新的位置（用于生产）
- 两者功能完全相同，只是位置不同
- 启动脚本已更新为使用 `controller/`

## 版本信息

- **SkillNet SDK**: 0.0.17
- **API Version**: 0.0.17
- **FastAPI**: 0.135.3
- **Uvicorn**: 0.43.0
