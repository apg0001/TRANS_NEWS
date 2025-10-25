from bs4 import BeautifulSoup
from typing import List
from urllib.parse import quote_plus
import httpx
from ..schemas.models import SearchItem


class NewsSearchService:
    BASE_URL = "https://search.naver.com/search.naver?where=news&ie=utf8&sm=nws_hty&query={query}"

    async def _fetch_html(self, url: str) -> str:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            })
            resp.raise_for_status()
            return resp.text

    def _build_search_url(self, keywords: List[str]) -> str:
        filtered = [k.strip() for k in keywords if k and k.strip()]
        query = "+".join([quote_plus(k) for k in filtered])
        return self.BASE_URL.format(query=query)

    def _parse(self, html: str, limit: int) -> List[SearchItem]:
        soup = BeautifulSoup(html, "lxml")
        items: List[SearchItem] = []

        headline_spans = soup.select("span.sds-comps-text-type-headline1")
        print(f"DEBUG: Found {len(headline_spans)} headline spans")
        
        seen = set()
        for i, span in enumerate(headline_spans):
            a = span.find_parent("a")
            if not a or not a.has_attr("href"):
                print(f"DEBUG: Span {i} - No parent link or href")
                continue
                
            title = span.get_text(strip=True)
            url = a["href"]
            
            if not title:
                print(f"DEBUG: Span {i} - Empty title")
                continue
                
            key = f"{title}|{url}"
            if key in seen:
                print(f"DEBUG: Span {i} - Duplicate item")
                continue
            seen.add(key)

            container = a
            for _ in range(6):
                if container and container.name != "div":
                    container = container.parent
                elif container and container.name == "div" and container.find("span", class_="sds-comps-text-type-body1"):
                    break
                else:
                    container = container.parent if container else None

            summary = ""
            if container:
                body_span = container.select_one("span.sds-comps-text-type-body1")
                if body_span:
                    summary = body_span.get_text(" ", strip=True)

            print(f"DEBUG: Item {len(items)} - Title: {title[:50]}...")
            items.append(SearchItem(title=title, url=url, summary=summary))
            if len(items) >= limit:
                break

        print(f"DEBUG: Returning {len(items)} items")
        return items

    async def search(self, keywords: List[str], limit: int = 10) -> List[SearchItem]:
        url = self._build_search_url(keywords)
        html = await self._fetch_html(url)
        return self._parse(html, limit)


