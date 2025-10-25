from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from ..services.hf_translate_service import HuggingFaceTranslateService

router = APIRouter()

# 싱글톤 인스턴스
hf_translator = HuggingFaceTranslateService()


class TranslationRequest(BaseModel):
    text: str
    source: str = "ko"
    target: str = "en"


class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    source: str
    target: str


@router.post("/translate", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    """텍스트 번역 API"""
    try:
        translated = await hf_translator.translate_async(
            request.text, 
            request.source, 
            request.target
        )
        
        return TranslationResponse(
            original_text=request.text,
            translated_text=translated,
            source=request.source,
            target=request.target
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"번역 실패: {str(e)}")


@router.get("/translate", response_model=TranslationResponse)
async def translate_text_get(
    text: str = Query(..., description="번역할 텍스트"),
    source: str = Query("ko", description="원본 언어"),
    target: str = Query("en", description="대상 언어")
):
    """GET 방식 텍스트 번역 API"""
    try:
        translated = await hf_translator.translate_async(text, source, target)
        
        return TranslationResponse(
            original_text=text,
            translated_text=translated,
            source=source,
            target=target
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"번역 실패: {str(e)}")


@router.get("/translate/health")
async def translate_health():
    """번역 서비스 상태 확인"""
    return {
        "status": "healthy" if hf_translator.model is not None else "unhealthy",
        "model_name": hf_translator.model_name,
        "model_loaded": hf_translator.model is not None
    }
