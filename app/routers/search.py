from fastapi import APIRouter, Query, HTTPException
from typing import List
from ..services.search_service import NewsSearchService
from ..services.hf_translate_service import HuggingFaceTranslateService
from ..schemas.models import SearchItem

router = APIRouter()

search_service = NewsSearchService()
hf_translator = HuggingFaceTranslateService()


@router.get("/search", response_model=List[SearchItem])
async def search_news(
    keywords: List[str] = Query(..., description="검색 키워드, 여러 개 가능"),
    limit: int = Query(10, ge=1, le=50),
    lang: str = Query("ko", description="응답 언어: ko|en"),
):
    try:
        items = await search_service.search(keywords=keywords, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"검색 실패: {e}")

    if lang == "en":
        # 제목/요약 영문화 (허깅페이스 모델 사용)
        for it in items:
            if it.title:
                it.title = await hf_translator.translate_async(it.title, src="ko", tgt="en")
            if it.summary:
                it.summary = await hf_translator.translate_async(it.summary, src="ko", tgt="en")
    return items


