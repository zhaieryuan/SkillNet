"""FastAPI 依赖注入"""

import os
from typing import Optional

from fastapi import HTTPException

from skillnet_ai import SkillNetClient


def get_skillnet_client() -> SkillNetClient:
    """
    创建 SkillNetClient 实例

    从环境变量自动读取配置：
    - API_KEY: OpenAI API Key（创建、评估、分析功能需要）
    - GITHUB_TOKEN: GitHub Token（可选，提高速率限制）
    - BASE_URL: API 基础 URL（可选）
    - SKILLNET_MODEL: 默认模型（可选）

    Returns:
        SkillNetClient: 配置好的客户端实例

    Raises:
        HTTPException: 如果需要 API_KEY 但未配置

    Note:
        环境变量配置方式：
        1. 创建 .env 文件（推荐）
        2. 导出环境变量: export API_KEY=sk-...
        3. 在启动命令中设置: API_KEY=sk-... python run_api.py
    """
    # SkillNetClient 会自动从环境变量读取配置
    # os.getenv("API_KEY"), os.getenv("GITHUB_TOKEN") 等
    return SkillNetClient()


def validate_api_key_for_operation(operation: str) -> None:
    """
    验证 API Key 是否已配置（用于需要 LLM 的操作）

    Args:
        operation: 操作名称（用于错误提示）

    Raises:
        HTTPException: 如果 API_KEY 未配置
    """
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=400,
            detail=f"{operation} requires API_KEY environment variable. "
            f"Please set API_KEY in .env file or environment variables. "
            f"Example: API_KEY=sk-... in .env file",
        )
