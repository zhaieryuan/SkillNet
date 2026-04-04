"""后台任务管理

使用内存存储任务状态（开发阶段）。
重启后任务丢失，生产环境建议使用 Redis。
"""

import asyncio
from datetime import datetime
from typing import Any, Callable, Dict
from uuid import uuid4

# 内存存储：任务 ID -> 任务状态
tasks_db: Dict[str, Dict[str, Any]] = {}


def create_task(func: Callable, *args, **kwargs) -> str:
    """
    创建后台任务

    Args:
        func: 要执行的函数
        *args: 位置参数
        **kwargs: 关键字参数

    Returns:
        str: 任务 ID
    """
    task_id = str(uuid4())

    # 初始化任务状态
    tasks_db[task_id] = {
        "task_id": task_id,
        "status": "pending",
        "created_at": datetime.utcnow().isoformat(),
        "result": None,
        "error": None,
    }

    # 启动后台任务
    asyncio.create_task(_run_task(task_id, func, *args, **kwargs))

    return task_id


async def _run_task(task_id: str, func: Callable, *args, **kwargs) -> None:
    """
    执行任务（内部使用）

    Args:
        task_id: 任务 ID
        func: 要执行的函数
        *args: 位置参数
        **kwargs: 关键字参数
    """
    try:
        # 更新状态为处理中
        tasks_db[task_id]["status"] = "processing"

        # 执行任务（同步函数在异步环境中执行）
        # 注意：这里使用 asyncio.to_thread 来避免阻塞事件循环
        result = await asyncio.to_thread(func, *args, **kwargs)

        # 更新状态为完成
        tasks_db[task_id]["status"] = "completed"
        tasks_db[task_id]["result"] = result
        tasks_db[task_id]["completed_at"] = datetime.utcnow().isoformat()

    except Exception as e:
        # 更新状态为失败
        tasks_db[task_id]["status"] = "failed"
        tasks_db[task_id]["error"] = str(e)
        tasks_db[task_id]["completed_at"] = datetime.utcnow().isoformat()


def get_task_status(task_id: str) -> Dict[str, Any] | None:
    """
    查询任务状态

    Args:
        task_id: 任务 ID

    Returns:
        Dict[str, Any] | None: 任务状态，如果任务不存在返回 None
    """
    return tasks_db.get(task_id)


def clear_completed_tasks() -> int:
    """
    清理已完成的任务（可用于定期清理）

    Returns:
        int: 清理的任务数量
    """
    global tasks_db
    completed_tasks = [
        task_id
        for task_id, task in tasks_db.items()
        if task["status"] in ("completed", "failed")
    ]

    for task_id in completed_tasks:
        del tasks_db[task_id]

    return len(completed_tasks)
