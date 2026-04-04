"""API 请求和响应模型"""

from .requests import (
    DownloadRequest,
    CreatePromptRequest,
    CreateGitHubRequest,
    CreateTrajectoryRequest,
    CreateOfficeRequest,
    EvaluateRequest,
    AnalyzeRequest,
)

from .responses import (
    DownloadResponse,
    TaskResponse,
    CreateResponse,
    EvaluateResponse,
    AnalyzeResponse,
    ErrorResponse,
)

__all__ = [
    # Requests
    "DownloadRequest",
    "CreatePromptRequest",
    "CreateGitHubRequest",
    "CreateTrajectoryRequest",
    "CreateOfficeRequest",
    "EvaluateRequest",
    "AnalyzeRequest",
    # Responses
    "DownloadResponse",
    "TaskResponse",
    "CreateResponse",
    "EvaluateResponse",
    "AnalyzeResponse",
    "ErrorResponse",
]
