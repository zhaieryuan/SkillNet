"""下载技能端点"""

import os
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from skillnet_ai import SkillNetClient
from controller.dependencies import get_github_token
from controller.models import DownloadRequest, DownloadResponse

router = APIRouter(prefix="/api/v1/skills", tags=["Download"])


@router.post("/download", response_model=DownloadResponse)
async def download_skill(
    request: DownloadRequest,
    github_token: Optional[str] = Depends(get_github_token),
) -> DownloadResponse:
    """
    下载技能到本地

    从 GitHub 仓库下载技能包到指定目录。

    ## 参数

    - **url**: GitHub 技能 URL
    - **target_dir**: 本地安装目录（默认当前目录）
    - **token**: GitHub Token（可选，用于提高速率限制）
    - **mirror_url**: GitHub 镜像 URL（可选，用于加速下载）

    ## 认证

    可通过以下方式提供 GitHub Token：
    1. 请求体中的 `token` 字段
    2. HTTP Header: `X-GitHub-Token`

    Header 中的 Token 优先级更高。

    ## 示例

    ```bash
    curl -X POST "http://localhost:8000/api/v1/skills/download" \\
      -H "Content-Type: application/json" \\
      -H "X-GitHub-Token: ghp_..." \\
      -d '{
        "url": "https://github.com/anthropics/skills/tree/main/skills/pdf-parser",
        "target_dir": "./my_skills",
        "mirror_url": "https://ghfast.top/"
      }'
    ```
    """
    try:
        # Header 中的 token 优先于请求体中的 token
        effective_token = github_token or request.token

        # 创建客户端
        client = SkillNetClient(github_token=effective_token)

        # 下载技能
        installed_path = client.download(
            url=request.url,
            target_dir=request.target_dir,
            mirror_url=request.mirror_url,
        )

        # 提取技能名称
        skill_name = os.path.basename(installed_path)

        return DownloadResponse(
            success=True,
            installed_path=installed_path,
            skill_name=skill_name,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Download failed: {str(e)}",
        )
