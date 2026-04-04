"""下载技能端点"""

import os

from fastapi import APIRouter, HTTPException

from skillnet_ai import SkillNetClient
from controller.dependencies import get_skillnet_client
from controller.models import DownloadRequest, DownloadResponse

router = APIRouter(prefix="/api/v1/skills", tags=["Download"])


@router.post("/download", response_model=DownloadResponse)
async def download_skill(
    request: DownloadRequest,
) -> DownloadResponse:
    """
    下载技能到本地

    从 GitHub 仓库下载技能包到指定目录。

    ## 环境变量

    - 可选: `GITHUB_TOKEN` - 用于提高速率限制和访问私有仓库
    - 可选: `GITHUB_MIRROR` - GitHub 镜像 URL（国内加速）

    在 `.env` 文件中配置：
    ```
    GITHUB_TOKEN=ghp-your-github-token-here
    GITHUB_MIRROR=https://ghfast.top/
    ```

    ## 参数

    - **url**: GitHub 技能 URL
    - **target_dir**: 本地安装目录（默认当前目录）
    - **token**: GitHub Token（可选，覆盖环境变量）
    - **mirror_url**: GitHub 镜像 URL（可选，覆盖环境变量）

    ## 示例

    ```bash
    curl -X POST "http://localhost:8000/api/v1/skills/download" \\
      -H "Content-Type: application/json" \\
      -d '{
        "url": "https://github.com/anthropics/skills/tree/main/skills/pdf-parser",
        "target_dir": "./my_skills",
        "mirror_url": "https://ghfast.top/"
      }'
    ```
    """
    try:
        # 创建客户端（自动从环境变量读取配置）
        # 如果请求体提供了 token 或 mirror_url，则覆盖环境变量
        client = get_skillnet_client()

        # 下载技能
        # 如果请求中提供了 mirror_url，则使用请求中的，否则使用环境变量
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
