"""API 响应模型"""

from typing import List, Optional, Dict, Any, Literal

from pydantic import BaseModel


class DownloadResponse(BaseModel):
    """下载技能响应"""

    success: bool = True
    installed_path: str
    skill_name: str


class TaskResponse(BaseModel):
    """异步任务响应"""

    task_id: str
    status: Literal["pending", "processing", "completed", "failed"]
    message: Optional[str] = None


class CreateResponse(BaseModel):
    """创建技能响应"""

    success: bool = True
    created_skills: List[str]
    count: int


class EvaluateResponse(BaseModel):
    """评估技能响应"""

    success: bool = True
    evaluation: Dict[str, Any]


class AnalyzeResponse(BaseModel):
    """分析技能关系响应"""

    success: bool = True
    relationships: List[Dict[str, Any]]
    count: int
    saved_path: Optional[str] = None


class ErrorResponse(BaseModel):
    """错误响应"""

    success: bool = False
    error: str
    detail: Optional[str] = None
