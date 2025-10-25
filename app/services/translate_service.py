from enum import Enum
from typing import Optional
import httpx


class LanguageCode(str, Enum):
    ko = "ko"
    en = "en"


class TranslatorService:
    """간단한 무료 번역기 호출 래퍼.

    기본은 LibreTranslate 퍼블릭 인스턴스를 사용하며, 배포 환경에서는
    자체 호스팅 혹은 유료 API로 교체할 수 있도록 인터페이스를 단순화.
    """

    def __init__(self, endpoint: Optional[str] = None):
        # 퍼블릭 엔드포인트는 가용성 변동이 있으므로 필요 시 교체
        self.endpoint = endpoint or "https://de.libretranslate.com/translate"

    async def translate_async(self, text: str, src: str, tgt: str) -> str:
        if not text:
            return text
        
        # 같은 언어면 번역하지 않음
        if src == tgt:
            return text
            
        payload = {"q": text, "source": src, "target": tgt, "format": "text"}
        async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
            try:
                r = await client.post(self.endpoint, data=payload, headers={
                    "accept": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                })
                r.raise_for_status()
                data = r.json()
                return data.get("translatedText", text)
            except Exception as e:
                print(f"번역 실패: {e}")
                # 번역 실패 시 원본 텍스트 반환
                return text


