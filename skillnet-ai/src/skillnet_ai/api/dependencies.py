"""FastAPI 依赖注入"""

from typing import Optional

from fastapi import Header, HTTPException

from skillnet_ai import SkillNetClient


async def get_api_key(x_api_key: Optional[str] = Header(None)) -> str:
    """
    验证 API Key（必需）

    用于需要 OpenAI API 的操作（创建、评估、分析）

    Args:
        x_api_key: OpenAI API Key (通过 X-API-Key header 传递)

    Returns:
        str: 验证后的 API Key

    Raises:
        HTTPException: 如果 API Key 缺失
    """
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="API Key is required. Set X-API-Key header with your OpenAI API key.",
        )
    return x_api_key


async def get_github_token(
    x_github_token: Optional[str] = Header(None),
) -> Optional[str]:
    """
    获取 GitHub Token（可选）

    用于提高 GitHub API 速率限制或访问私有仓库

    Args:
        x_github_token: GitHub Personal Access Token (通过 X-GitHub-Token header 传递)

    Returns:
        Optional[str]: GitHub Token 或 None
    """
    return x_github_token


def get_skillnet_client(
    api_key: Optional[str] = None,
    github_token: Optional[str] = None,
) -> SkillNetClient:
    """
    创建 SkillNetClient 实例

    Args:
        api_key: OpenAI API Key（可选）
        github_token: GitHub Token（可选）

    Returns:
        SkillNetClient: 配置好的客户端实例
    """
    return SkillNetClient(
        api_key=api_key,
        github_token=github_token,
    )
