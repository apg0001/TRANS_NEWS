from transformers import MarianMTModel, MarianTokenizer
from typing import Optional
import torch


class HuggingFaceTranslateService:
    """허깅페이스 번역 모델을 사용한 번역 서비스 (지연 로딩)"""

    def __init__(self, model_name: str = "Helsinki-NLP/opus-mt-ko-en"):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None

    def _ensure_loaded(self) -> bool:
        """필요 시 모델 로드. 성공 여부 반환"""
        if self.model is not None and self.tokenizer is not None:
            return True
        try:
            print(f"Loading translation model: {self.model_name}")
            self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)
            self.model = MarianMTModel.from_pretrained(self.model_name)
            print("Translation model loaded successfully")
            return True
        except Exception as e:
            print(f"Failed to load translation model: {e}")
            self.model = None
            self.tokenizer = None
            return False
    
    def translate_ko_to_en(self, text: str) -> str:
        """한국어를 영어로 번역"""
        if not text:
            return text

        if not self._ensure_loaded():
            return text
        
        try:
            # 텍스트를 토큰화
            inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
            
            # 번역 수행
            with torch.no_grad():
                translated = self.model.generate(**inputs, max_length=512, num_beams=4, early_stopping=True)
            
            # 결과 디코딩
            translated_text = self.tokenizer.decode(translated[0], skip_special_tokens=True)
            return translated_text.strip()
            
        except Exception as e:
            print(f"Translation error: {e}")
            return text
    
    def translate_en_to_ko(self, text: str) -> str:
        """영어를 한국어로 번역 (역방향 모델 필요)"""
        # 역방향 번역을 위한 모델이 필요하지만, 일단 원본 반환
        # 실제로는 en-ko 모델을 별도로 로드해야 함
        return text
    
    async def translate_async(self, text: str, src: str, tgt: str) -> str:
        """비동기 번역 (동기 함수를 래핑)"""
        if not text:
            return text
        
        if src == tgt:
            return text
        
        if src == "ko" and tgt == "en":
            return self.translate_ko_to_en(text)
        elif src == "en" and tgt == "ko":
            return self.translate_en_to_ko(text)
        else:
            return text
