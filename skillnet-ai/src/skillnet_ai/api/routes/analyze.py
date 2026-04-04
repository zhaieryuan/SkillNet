"""分析技能关系端点"""

import os

from fastapi import APIRouter, HTTPException

from skillnet_ai import SkillNetClient
from skillnet_ai.api.dependencies import get_skillnet_client, validate_api_key_for_operation
from skillnet_ai.api.models import AnalyzeRequest, AnalyzeResponse

router = APIRouter(prefix="/api/v1/skills", tags=["Analyze"])


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_skills(
    request: AnalyzeRequest,
) -> AnalyzeResponse:
    """
    分析技能关系

    使用 LLM 分析多个技能之间的关系。

    ## 环境变量

    需要配置 `API_KEY` 环境变量（OpenAI API Key）

    在 `.env` 文件中配置：
    ```
    API_KEY=sk-your-openai-api-key-here
    ```

    ## 关系类型

    分析 4 种技能关系：

    1. **similar_to**: 功能相似 - 两个技能提供类似的功能
    2. **belong_to**: 归属关系 - 技能属于某个类别或领域
    3. **compose_with**: 可组合使用 - 技能可以组合使用以完成复杂任务
    4. **depend_on**: 依赖关系 - 技能依赖其他技能的功能

    ## 参数

    - **skills_dir**: 包含多个技能的目录路径
    - **save_to_file**: 是否保存分析结果到文件（默认 true）
    - **model**: 使用的 LLM 模型（默认 gpt-4o）

    ## 返回

    - **relationships**: 关系列表
    - **count**: 关系总数
    - **saved_path**: 保存的文件路径（如果 save_to_file=true）

    ## 示例

    ```bash
    curl -X POST "http://localhost:8000/api/v1/skills/analyze" \\
      -H "Content-Type: application/json" \\
      -d '{
        "skills_dir": "./my_skills",
        "save_to_file": true
      }'
    ```

    ## 响应示例

    ```json
    {
      "success": true,
      "relationships": [
        {
          "type": "similar_to",
          "source": "pdf-parser",
          "target": "doc-parser",
          "reason": "Both parse document files"
        },
        {
          "type": "depend_on",
          "source": "report-generator",
          "target": "pdf-parser",
          "reason": "Uses PDF parsing for input"
        }
      ],
      "count": 2,
      "saved_path": "./my_skills/relationships.json"
    }
    ```
    """
    try:
        # 验证 API_KEY 已配置
        validate_api_key_for_operation("Analyze skill relationships")

        # 创建客户端（自动从环境变量读取配置）
        client = get_skillnet_client()

        # 分析技能关系
        relationships = client.analyze(
            skills_dir=request.skills_dir,
            save_to_file=request.save_to_file,
            model=request.model,
        )

        # 确定保存路径
        saved_path = None
        if request.save_to_file:
            saved_path = os.path.join(request.skills_dir, "relationships.json")

        return AnalyzeResponse(
            success=True,
            relationships=relationships,
            count=len(relationships),
            saved_path=saved_path,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}",
        )
