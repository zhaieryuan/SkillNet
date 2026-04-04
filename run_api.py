#!/usr/bin/env python3
"""启动 SkillNet API 服务器

Usage:
    python run_api.py

默认配置:
    - Host: 0.0.0.0 (所有网络接口)
    - Port: 8000
    - Reload: True (开发模式，代码变更自动重启)
    - Log Level: info

环境变量:
    - HOST: 服务器地址（默认 0.0.0.0）
    - PORT: 服务器端口（默认 8000）
    - RELOAD: 是否启用自动重载（默认 true）
"""

import os
import sys

# 添加 skillnet-ai/src 到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "skillnet-ai", "src"))

import uvicorn

if __name__ == "__main__":
    # 从环境变量读取配置
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8010"))
    reload = os.getenv("RELOAD", "true").lower() in ("true", "1", "yes")

    print("=" * 60)
    print("SkillNet API Server")
    print("=" * 60)
    print(f"Starting server at http://{host}:{port}")
    print(f"Swagger UI: http://{host}:{port}/docs")
    print(f"ReDoc: http://{host}:{port}/redoc")
    print(f"Auto-reload: {reload}")
    print("=" * 60)

    uvicorn.run(
        "controller.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info",
    )
