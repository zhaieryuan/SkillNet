"""搜索技能端点"""

from typing import Optional

from fastapi import APIRouter, Query, HTTPException

from skillnet_ai import SkillNetClient
from skillnet_ai.models import SearchResponse

router = APIRouter(prefix="/api/v1/skills", tags=["Search"])


@router.get("/search", response_model=SearchResponse)
async def search_skills(
    q: str = Query(..., description="搜索查询（关键词或自然语言）"),
    mode: str = Query("keyword", regex="^(keyword|vector)$", description="搜索模式"),
    category: Optional[str] = Query(None, description="按类别过滤"),
    limit: int = Query(20, ge=1, le=100, description="返回结果数量"),
    page: int = Query(1, ge=1, description="页码（仅 keyword 模式）"),
    min_stars: int = Query(0, ge=0, description="最小 Star 数（仅 keyword 模式）"),
    sort_by: str = Query(
        "stars",
        regex="^(stars|recent)$",
        description="排序方式（仅 keyword 模式）",
    ),
    threshold: float = Query(
        0.8,
        ge=0.0,
        le=1.0,
        description="相似度阈值（仅 vector 模式）",
    ),
) -> SearchResponse:
    """
    搜索技能

    支持两种搜索模式：
    - **keyword**: 关键词搜索，支持分页、排序、Star 过滤
    - **vector**: 语义搜索，使用相似度阈值

    ## 示例

    关键词搜索：
    ```
    GET /api/v1/skills/search?q=pdf&mode=keyword&limit=5
    ```

    语义搜索：
    ```
    GET /api/v1/skills/search?q=图片处理和可视化&mode=vector&threshold=0.85
    ```
    """
    try:
        client = SkillNetClient()

        # 调用 SkillNetClient 搜索
        results = client.search(
            q=q,
            mode=mode,
            category=category,
            limit=limit,
            page=page,
            min_stars=min_stars,
            sort_by=sort_by,
            threshold=threshold,
        )

        # 如果 results 已经是 SearchResponse 对象，直接返回
        if isinstance(results, SearchResponse):
            return results

        # 如果是列表，需要构造 SearchResponse
        from skillnet_ai.models import MetaModel

        meta = MetaModel(
            query=q,
            search_mode=mode,
            category=category,
            limit=limit,
            total=len(results) if isinstance(results, list) else 0,
            page=page if mode == "keyword" else None,
            min_stars=min_stars if mode == "keyword" else None,
            sort_by=sort_by if mode == "keyword" else None,
            threshold=threshold if mode == "vector" else None,
        )

        return SearchResponse(
            data=results if isinstance(results, list) else [],
            meta=meta,
            success=True,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
