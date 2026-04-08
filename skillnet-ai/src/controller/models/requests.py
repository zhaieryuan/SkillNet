"""API 请求模型"""

from typing import Optional, Literal

from pydantic import BaseModel, Field


class DownloadRequest(BaseModel):
    """下载技能请求"""

    url: str = Field(..., description="GitHub 技能 URL")
    target_dir: str = Field(".", description="本地安装目录")
    token: Optional[str] = Field(None, description="GitHub Token（可选，优先使用 header）")
    mirror_url: Optional[str] = Field(None, description="GitHub 镜像 URL（用于加速下载）")


class CreatePromptRequest(BaseModel):
    """从提示创建技能请求"""

    prompt: str = Field(..., min_length=10, description="自然语言描述，说明想要创建的技能")
    output_dir: str = Field("./generated_skills", description="生成技能的输出目录")
    model: str = Field("glm-4-flash", description="使用的 LLM 模型")


class CreateGitHubRequest(BaseModel):
    """从 GitHub 创建技能请求"""

    github_url: str = Field(..., description="GitHub 仓库 URL")
    output_dir: str = Field("./generated_skills", description="生成技能的输出目录")
    model: str = Field("glm-4-flash", description="使用的 LLM 模型")
    max_files: int = Field(50, ge=1, le=500, description="最大分析文件数")


class CreateTrajectoryRequest(BaseModel):
    """从轨迹文件创建技能请求（文件上传模式，用于表单验证）"""

    output_dir: str = Field("./generated_skills", description="生成技能的输出目录")
    model: str = Field("glm-4-flash", description="使用的 LLM 模型")


class CreateOfficeRequest(BaseModel):
    """从 Office 文档创建技能请求（文件上传模式，用于表单验证）"""

    output_dir: str = Field("./generated_skills", description="生成技能的输出目录")
    model: str = Field("glm-4-flash", description="使用的 LLM 模型")


class EvaluateRequest(BaseModel):
    """评估技能请求"""

    target: str = Field(..., description="技能路径或 GitHub URL")
    name: Optional[str] = Field(None, description="技能名称（可选，从目录推断）")
    category: Optional[str] = Field(None, description="技能类别（可选）")
    description: Optional[str] = Field(None, description="技能描述（可选）")
    model: str = Field("glm-4-flash", description="使用的 LLM 模型")
    max_workers: int = Field(5, ge=1, le=20, description="并行评估的最大线程数")


class AnalyzeRequest(BaseModel):
    """分析技能关系请求"""

    skills_dir: str = Field(..., description="包含多个技能的目录路径")
    save_to_file: bool = Field(True, description="是否保存分析结果到文件")
    model: str = Field("glm-4-flash", description="使用的 LLM 模型")
