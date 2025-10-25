# app/main.py
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# 앱 생성 (통합 앱)
app = FastAPI(title="TransNews - 검색·크롤링·요약·번역", version="1.0.0")

# 정적/템플릿
BASE_DIR = os.path.dirname(__file__)
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# 라우터 등록
from .routers.search import router as search_router
from .routers.article import router as article_router
from .routers.translate import router as translate_router
from .routers.email import router as email_router

app.include_router(search_router, prefix="/api", tags=["search"]) 
app.include_router(article_router, prefix="/api", tags=["article"])
app.include_router(translate_router, prefix="/api", tags=["translate"])
app.include_router(email_router, prefix="/api", tags=["email"]) 


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    # 키워드 검색 폼 렌더링
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/search", response_class=HTMLResponse)
def search_results(request: Request):
    # 검색 결과 페이지 렌더링
    return templates.TemplateResponse("search_results.html", {"request": request})


@app.get("/article", response_class=HTMLResponse)
def article_detail(request: Request):
    # 기사 상세 페이지 렌더링
    return templates.TemplateResponse("article_detail.html", {"request": request})