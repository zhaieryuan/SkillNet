"""SkillNet FastAPI Application"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from skillnet_ai.client import SkillNetError
from skillnet_ai.downloader import GitHubAPIError

# FastAPI 应用实例
app = FastAPI(
    title="SkillNet API",
    description="""
    ## SkillNet AI Agent Skills Management Platform

    SkillNet 提供全面的 AI Agent 技能管理功能，包括：
    - 🔍 **搜索技能**: 关键词搜索和语义搜索
    - 📥 **下载技能**: 从 GitHub 下载技能到本地
    - ✨ **创建技能**: 从多种来源创建新技能（提示词、GitHub、轨迹文件、Office 文档）
    - 📊 **评估技能**: 5 维度质量评估（安全性、完整性、可执行性、可维护性、成本意识）
    - 🕸️ **分析关系**: 分析技能之间的关系（相似、归属、组合、依赖）

    ### 认证

    部分端点需要 API Key 认证：
    - 使用 `X-API-Key` header 传递 OpenAI API Key
    - 可选 `X-GitHub-Token` header 用于 GitHub 操作

    ### 在线平台

    - 网站: http://skillnet.openkg.cn/
    - 论文: https://arxiv.org/abs/2603.04448
    - GitHub: https://github.com/zjunlp/SkillNet
    """,
    version="0.0.17",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "SkillNet Team",
        "url": "https://github.com/zjunlp/SkillNet",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

# CORS 中间件配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应配置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 全局异常处理器
@app.exception_handler(SkillNetError)
async def skillnet_error_handler(request: Request, exc: SkillNetError) -> JSONResponse:
    """处理 SkillNetError 异常"""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "SkillNet Error",
            "detail": str(exc),
        },
    )


@app.exception_handler(GitHubAPIError)
async def github_error_handler(request: Request, exc: GitHubAPIError) -> JSONResponse:
    """处理 GitHubAPIError 异常"""
    return JSONResponse(
        status_code=502,
        content={
            "success": False,
            "error": "GitHub API Error",
            "detail": str(exc),
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """处理所有未捕获的异常"""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal Server Error",
            "detail": str(exc),
        },
    )


# 健康检查端点
@app.get("/health", tags=["Health"])
async def health_check() -> dict:
    """
    健康检查

    返回服务状态和版本信息
    """
    return {
        "status": "healthy",
        "service": "SkillNet API",
        "version": "0.0.17",
    }


# 根路径
@app.get("/", tags=["Info"])
async def root() -> dict:
    """
    API 根路径

    返回 API 基本信息和文档链接
    """
    return {
        "message": "SkillNet API - AI Agent Skills Management Platform",
        "version": "0.0.17",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "links": {
            "website": "http://skillnet.openkg.cn/",
            "github": "https://github.com/zjunlp/SkillNet",
            "paper": "https://arxiv.org/abs/2603.04448",
        },
    }


# 路由注册
from .routes import search, download, create, evaluate, analyze, tasks

app.include_router(search.router)
app.include_router(download.router)
app.include_router(create.router)
app.include_router(evaluate.router)
app.include_router(analyze.router)
app.include_router(tasks.router)
