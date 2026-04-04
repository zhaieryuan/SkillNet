"""任务状态查询端点"""

from fastapi import APIRouter, HTTPException

from controller.background_tasks import get_task_status
from controller.models import CreateResponse

router = APIRouter(prefix="/api/v1/tasks", tags=["Tasks"])


@router.get("/{task_id}")
async def get_task(task_id: str) -> dict:
    """
    查询异步任务状态

    用于查询创建技能等长时间运行任务的状态和结果。

    ## 任务状态

    - **pending**: 任务已创建，等待执行
    - **processing**: 任务正在执行中
    - **completed**: 任务成功完成
    - **failed**: 任务执行失败

    ## 参数

    - **task_id**: 任务 ID（从创建端点返回）

    ## 响应

    根据任务状态返回不同的信息：

    ### 进行中（pending/processing）
    ```json
    {
      "task_id": "uuid",
      "status": "processing",
      "created_at": "2026-04-04T10:00:00",
      "result": null,
      "error": null
    }
    ```

    ### 已完成（completed）
    ```json
    {
      "task_id": "uuid",
      "status": "completed",
      "created_at": "2026-04-04T10:00:00",
      "completed_at": "2026-04-04T10:05:00",
      "result": {
        "success": true,
        "created_skills": ["/path/to/skill1", "/path/to/skill2"],
        "count": 2
      }
    }
    ```

    ### 失败（failed）
    ```json
    {
      "task_id": "uuid",
      "status": "failed",
      "created_at": "2026-04-04T10:00:00",
      "completed_at": "2026-04-04T10:02:00",
      "error": "Error message..."
    }
    ```

    ## 示例

    ```bash
    # 创建任务
    TASK_ID=$(curl -X POST "http://localhost:8000/api/v1/skills/create/prompt" \\
      -H "Content-Type: application/json" \\
      -H "X-API-Key: sk-..." \\
      -d '{"prompt": "创建一个工具"}' | jq -r '.task_id')

    # 轮询任务状态
    while true; do
      STATUS=$(curl "http://localhost:8000/api/v1/tasks/$TASK_ID" | jq -r '.status')
      echo "Status: $STATUS"
      if [ "$STATUS" = "completed" ] || [ "$STATUS" = "failed" ]; then
        break
      fi
      sleep 5
    done

    # 获取最终结果
    curl "http://localhost:8000/api/v1/tasks/$TASK_ID" | jq
    ```
    """
    # 查询任务状态
    task = get_task_status(task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task not found: {task_id}",
        )

    # 如果任务完成且有结果，格式化结果
    if task["status"] == "completed" and task.get("result"):
        result_data = task["result"]

        # 如果结果是列表（创建技能返回的路径列表），包装成 CreateResponse
        if isinstance(result_data, list):
            return {
                **task,
                "result": CreateResponse(
                    success=True,
                    created_skills=result_data,
                    count=len(result_data),
                ).dict(),
            }

    # 返回原始任务状态
    return task
