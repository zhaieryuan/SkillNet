"""评估技能端点"""

from fastapi import APIRouter, Depends, HTTPException

from skillnet_ai import SkillNetClient
from skillnet_ai.api.dependencies import get_api_key
from skillnet_ai.api.models import EvaluateRequest, EvaluateResponse

router = APIRouter(prefix="/api/v1/skills", tags=["Evaluate"])


@router.post("/evaluate", response_model=EvaluateResponse)
async def evaluate_skill(
    request: EvaluateRequest,
    api_key: str = Depends(get_api_key),
) -> EvaluateResponse:
    """
    评估技能质量

    使用 LLM 对技能进行多维度质量评估。

    ## 认证

    需要 `X-API-Key` header（OpenAI API Key）

    ## 评估维度

    返回 5 个维度的评估结果：

    1. **safety**: 安全性 - 代码是否安全、是否处理错误
    2. **completeness**: 完整性 - 功能是否完整、文档是否齐全
    3. **executability**: 可执行性 - 代码是否可以直接运行
    4. **maintainability**: 可维护性 - 代码质量、可读性、可扩展性
    5. **cost_awareness**: 成本意识 - 资源使用效率、API 调用成本

    每个维度包含：
    - **level**: 评级（Excellent/Good/Average/Poor/Critical）
    - **score**: 分数（0-100）
    - **feedback**: 详细反馈和改进建议

    ## 参数

    - **target**: 技能路径（本地目录）或 GitHub URL
    - **name**: 技能名称（可选，从目录推断）
    - **category**: 技能类别（可选）
    - **description**: 技能描述（可选）
    - **model**: 使用的 LLM 模型（默认 gpt-4o）
    - **max_workers**: 并行评估的最大线程数（默认 5）

    ## 示例

    ```bash
    curl -X POST "http://localhost:8000/api/v1/skills/evaluate" \\
      -H "Content-Type: application/json" \\
      -H "X-API-Key: sk-..." \\
      -d '{
        "target": "./my_skills/pdf-parser",
        "name": "PDF Parser",
        "category": "Productivity"
      }'
    ```

    ## 响应示例

    ```json
    {
      "success": true,
      "evaluation": {
        "safety": {
          "level": "Good",
          "score": 85,
          "feedback": "Code handles most error cases..."
        },
        "completeness": {
          "level": "Excellent",
          "score": 95,
          "feedback": "Comprehensive documentation..."
        },
        ...
      }
    }
    ```
    """
    try:
        # 创建客户端
        client = SkillNetClient(api_key=api_key)

        # 评估技能
        evaluation = client.evaluate(
            target=request.target,
            name=request.name,
            category=request.category,
            description=request.description,
            model=request.model,
            max_workers=request.max_workers,
        )

        return EvaluateResponse(
            success=True,
            evaluation=evaluation,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Evaluation failed: {str(e)}",
        )
