from pydantic import BaseModel, HttpUrl
from typing import Optional


class SearchItem(BaseModel):
    title: str
    url: HttpUrl
    summary: Optional[str] = None


class ArticleDetail(BaseModel):
    url: HttpUrl
    original_ko: str
    summary_ko: str
    original_en: Optional[str] = None
    summary_en: Optional[str] = None


