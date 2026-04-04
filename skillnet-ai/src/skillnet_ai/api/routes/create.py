"""创建技能端点"""

import os
import tempfile
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from skillnet_ai import SkillNetClient
from skillnet_ai.api.background_tasks import create_task
from skillnet_ai.api.dependencies import get_api_key, get_github_token
from skillnet_ai.api.models import (
    CreatePromptRequest,
    CreateGitHubRequest,
    TaskResponse,
)

router = APIRouter(prefix="/api/v1/skills/create", tags=["Create"])


@router.post("/prompt", response_model=TaskResponse, status_code=202)
async def create_from_prompt(
    request: CreatePromptRequest,
    api_key: str = Depends(get_api_key),
) -> TaskResponse:
    """
    从自然语言提示创建技能

    使用 LLM 根据自然语言描述生成技能代码。

    ## 认证

    需要 `X-API-Key` header（OpenAI API Key）

    ## 参数

    - **prompt**: 自然语言描述，说明想要创建的技能
    - **output_dir**: 生成技能的输出目录
    - **model**: 使用的 LLM 模型（默认 gpt-4o）

    ## 返回

    返回任务 ID，使用 `GET /api/v1/tasks/{task_id}` 查询进度

    ## 示例

    ```bash
    curl -X POST "http://localhost:8000/api/v1/skills/create/prompt" \\
      -H "Content-Type: application/json" \\
      -H "X-API-Key: sk-..." \\
      -d '{
        "prompt": "创建一个图片压缩工具",
        "output_dir": "./generated_skills"
      }'
    ```
    """
    try:
        # 创建客户端
        client = SkillNetClient(api_key=api_key)

        # 创建后台任务
        task_id = create_task(
            client.create,
            prompt=request.prompt,
            output_dir=request.output_dir,
            model=request.model,
        )

        return TaskResponse(
            task_id=task_id,
            status="pending",
            message="Skill creation from prompt started",
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create task: {str(e)}",
        )


@router.post("/github", response_model=TaskResponse, status_code=202)
async def create_from_github(
    request: CreateGitHubRequest,
    api_key: str = Depends(get_api_key),
    github_token: Optional[str] = Depends(get_github_token),
) -> TaskResponse:
    """
    从 GitHub 仓库创建技能

    分析 GitHub 仓库代码并生成技能。

    ## 认证

    - 必需: `X-API-Key` header（OpenAI API Key）
    - 可选: `X-GitHub-Token` header（用于访问私有仓库）

    ## 参数

    - **github_url**: GitHub 仓库 URL
    - **output_dir**: 生成技能的输出目录
    - **model**: 使用的 LLM 模型（默认 gpt-4o）
    - **max_files**: 最大分析文件数（默认 50）

    ## 返回

    返回任务 ID，使用 `GET /api/v1/tasks/{task_id}` 查询进度

    ## 示例

    ```bash
    curl -X POST "http://localhost:8000/api/v1/skills/create/github" \\
      -H "Content-Type: application/json" \\
      -H "X-API-Key: sk-..." \\
      -H "X-GitHub-Token: ghp_..." \\
      -d '{
        "github_url": "https://github.com/owner/repo",
        "output_dir": "./generated_skills"
      }'
    ```
    """
    try:
        # 创建客户端
        client = SkillNetClient(api_key=api_key, github_token=github_token)

        # 创建后台任务
        task_id = create_task(
            client.create,
            github_url=request.github_url,
            output_dir=request.output_dir,
            model=request.model,
            max_files=request.max_files,
        )

        return TaskResponse(
            task_id=task_id,
            status="pending",
            message="Skill creation from GitHub repository started",
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create task: {str(e)}",
        )


@router.post("/trajectory", response_model=TaskResponse, status_code=202)
async def create_from_trajectory(
    trajectory_file: UploadFile = File(..., description="执行轨迹文件（.txt）"),
    output_dir: str = Form("./generated_skills", description="生成技能的输出目录"),
    model: str = Form("gpt-4o", description="使用的 LLM 模型"),
    api_key: str = Depends(get_api_key),
) -> TaskResponse:
    """
    从执行轨迹文件创建技能

    根据 Agent 执行轨迹生成技能代码。

    ## 认证

    需要 `X-API-Key` header（OpenAI API Key）

    ## 参数

    - **trajectory_file**: 轨迹文件（.txt 格式）
    - **output_dir**: 生成技能的输出目录
    - **model**: 使用的 LLM 模型（默认 gpt-4o）

    ## 返回

    返回任务 ID，使用 `GET /api/v1/tasks/{task_id}` 查询进度

    ## 示例

    ```bash
    curl -X POST "http://localhost:8000/api/v1/skills/create/trajectory" \\
      -H "X-API-Key: sk-..." \\
      -F "trajectory_file=@trajectory.txt" \\
      -F "output_dir=./generated_skills"
    ```
    """
    try:
        # 验证文件类型
        if not trajectory_file.filename.endswith(".txt"):
            raise HTTPException(
                status_code=400,
                detail="Only .txt files are supported for trajectory",
            )

        # 保存上传的文件到临时目录
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
            content = await trajectory_file.read()
            tmp.write(content)
            tmp_path = tmp.name

        # 读取内容
        with open(tmp_path, "r", encoding="utf-8") as f:
            trajectory_content = f.read()

        # 创建客户端
        client = SkillNetClient(api_key=api_key)

        # 创建后台任务
        task_id = create_task(
            client.create,
            trajectory_content=trajectory_content,
            output_dir=output_dir,
            model=model,
        )

        # 清理临时文件
        os.unlink(tmp_path)

        return TaskResponse(
            task_id=task_id,
            status="pending",
            message="Skill creation from trajectory file started",
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create task: {str(e)}",
        )


@router.post("/office", response_model=TaskResponse, status_code=202)
async def create_from_office(
    office_file: UploadFile = File(..., description="Office 文档（.pdf/.docx/.pptx）"),
    output_dir: str = Form("./generated_skills", description="生成技能的输出目录"),
    model: str = Form("gpt-4o", description="使用的 LLM 模型"),
    api_key: str = Depends(get_api_key),
) -> TaskResponse:
    """
    从 Office 文档创建技能

    从 PDF、Word 或 PowerPoint 文档中提取信息并生成技能。

    ## 认证

    需要 `X-API-Key` header（OpenAI API Key）

    ## 参数

    - **office_file**: Office 文档（支持 .pdf, .docx, .doc, .pptx, .ppt）
    - **output_dir**: 生成技能的输出目录
    - **model**: 使用的 LLM 模型（默认 gpt-4o）

    ## 返回

    返回任务 ID，使用 `GET /api/v1/tasks/{task_id}` 查询进度

    ## 示例

    ```bash
    curl -X POST "http://localhost:8000/api/v1/skills/create/office" \\
      -H "X-API-Key: sk-..." \\
      -F "office_file=@tutorial.pdf" \\
      -F "output_dir=./generated_skills"
    ```
    """
    try:
        # 验证文件类型
        allowed_extensions = [".pdf", ".docx", ".doc", ".pptx", ".ppt"]
        file_ext = os.path.splitext(office_file.filename)[1].lower()

        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}",
            )

        # 保存到临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
            content = await office_file.read()
            tmp.write(content)
            tmp_path = tmp.name

        # 创建客户端
        client = SkillNetClient(api_key=api_key)

        # 创建后台任务
        task_id = create_task(
            client.create,
            office_file=tmp_path,
            output_dir=output_dir,
            model=model,
        )

        # 注意：临时文件在任务执行完成后才删除
        # 这里不能立即删除，因为任务是异步的

        return TaskResponse(
            task_id=task_id,
            status="pending",
            message="Skill creation from office document started",
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create task: {str(e)}",
        )
