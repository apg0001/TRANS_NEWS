from fastapi import APIRouter, Query, HTTPException
from ..crawler import Crawler
from ..summarizer import Summarizer
from ..services.hf_translate_service import HuggingFaceTranslateService
from ..schemas.models import ArticleDetail

router = APIRouter()

crawler = Crawler()
summarizer = Summarizer()
hf_translator = HuggingFaceTranslateService()


@router.get("/article", response_model=ArticleDetail)
async def get_article(
    url: str = Query(..., description="기사 URL"),
    max_summary_len: int = Query(128, ge=16, le=512),
    chunk_min_chars: int = Query(500, ge=200, le=3000),
    lang: str = Query("ko", description="응답 언어: ko|en"),
):
    content = crawler.extract_article(url)
    if not content or content.startswith("[ERROR]"):
        raise HTTPException(status_code=422, detail="기사 본문 추출 실패")

    try:
        summary = summarizer.summarize_aggregated(content, min_chars=chunk_min_chars, max_length=max_summary_len)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"요약 실패: {e}")

    original_ko = content
    summary_ko = summary

    original_en = None
    summary_en = None
    if lang == "en":
        # 허깅페이스 모델로 번역
        original_en = await hf_translator.translate_async(original_ko, src="ko", tgt="en")
        summary_en = await hf_translator.translate_async(summary_ko, src="ko", tgt="en")

    return ArticleDetail(
        url=url,
        original_ko=original_ko,
        summary_ko=summary_ko,
        original_en=original_en,
        summary_en=summary_en,
    )


