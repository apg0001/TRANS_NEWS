# TransNews

키워드 기반 뉴스 검색과 기사 본문 크롤링/요약, 한↔영 번역을 하나의 FastAPI 앱으로 통합한 프로젝트입니다.

## 기능
- 키워드 기반 뉴스 검색 (네이버 뉴스 결과 파싱, 개수 제한)
- 기사 URL 입력 시 본문 크롤링 및 요약
- 한↔영 번역 지원: 검색 결과(제목/요약) 및 기사 상세(원문/요약)를 한국어 또는 영어로 보기
- 간단한 웹 UI 제공 (키워드 입력 → 리스트업 → 기사 상세 보기)

## 구조
```
TransNews/
  app/
    main.py                  # FastAPI 앱 시작점 (라우터 등록, 템플릿 마운트)
    crawler.py               # 기사 본문 크롤링 클래스
    summarizer.py            # 요약 모델 래퍼 (T5)
    routers/
      search.py              # /api/search: 키워드 기반 검색 API
      article.py             # /api/article: 기사 상세 조회(본문 크롤링+요약+번역) API
    services/
      search_service.py      # 네이버 뉴스 검색 파서/로더
      translate_service.py   # 번역 서비스 (LibreTranslate 기본)
    schemas/
      models.py              # Pydantic 응답 모델
    templates/
      index.html             # 웹 UI (검색/리스트/상세)
    static/
      styles.css
  requirements.txt
  LICENSE
  README.md
```

## 설치
Windows CMD 기준:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

PyTorch는 환경에 따라 별도 설치가 필요할 수 있습니다. CUDA가 없는 경우 CPU 버전으로 설치하세요.

## 실행
```bash
uvicorn app.main:app --reload --port 8000
```
브라우저에서 `http://localhost:8000` 접속.

## REST API
- GET `/api/search?keywords=스포츠&keywords=야구&limit=10&lang=ko|en`
  - 응답: `SearchItem[]` (제목/요약은 lang=en이면 영문 번역 적용)
- GET `/api/article?url=<기사URL>&max_summary_len=128&chunk_min_chars=500&lang=ko|en`
  - 응답: `ArticleDetail` (요청 lang=en이면 원문/요약 영문 포함)

## 번역 백엔드
기본으로 LibreTranslate 퍼블릭 인스턴스(`https://libretranslate.de`)를 사용합니다. 가용성 문제 시 `app/services/translate_service.py`의 `endpoint`를 교체하거나 유료 번역 API로 래핑하세요.

## 주의사항
- 뉴스 검색 파싱은 네이버 UI 변경에 따라 깨질 수 있습니다.
- 요약 모델 로딩에 시간이 걸릴 수 있습니다(초기 1회). 모델/토치 버전은 환경에 맞춰 조정하세요.

## 라이선스
LICENSE 파일 참고.


