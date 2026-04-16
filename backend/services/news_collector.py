"""
뉴스 자동 수집 서비스
NewsAPI를 사용하여 미얀마/인도네시아 관련 뉴스 수집
"""
import os
import json
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
import httpx

from models.news import News
from models.country import Country
from models.scheduler_config import SchedulerConfig


class NewsCollector:
    """뉴스 수집기"""

    def __init__(self, db: Session):
        self.db = db
        self.newsapi_key = os.getenv("NEWSAPI_KEY", "")  # NewsAPI 키 (선택)

    async def collect_news(self, country_code: str) -> dict:
        """
        특정 국가의 뉴스 수집

        Args:
            country_code: 국가 코드 (MM, ID)

        Returns:
            수집 결과 딕셔너리
        """
        country = self.db.query(Country).filter(Country.code == country_code).first()
        if not country:
            return {"success": False, "error": "Country not found"}

        config = self.db.query(SchedulerConfig).filter(
            SchedulerConfig.country_code == country_code
        ).first()

        if not config or not config.enabled:
            return {"success": False, "error": "Scheduler not enabled"}

        # 키워드 파싱
        keywords = json.loads(config.keywords) if config.keywords else []
        if not keywords:
            keywords = self._get_default_keywords(country_code)

        collected_count = 0
        errors = []

        try:
            # NewsAPI 사용 (키가 있는 경우)
            if self.newsapi_key:
                result = await self._collect_from_newsapi(country, keywords)
                collected_count += result.get("count", 0)
                if result.get("error"):
                    errors.append(result["error"])

            # 웹 크롤링 (NewsAPI 없거나 추가 수집)
            # TODO: 실제 크롤링 구현
            # result = await self._collect_from_web_scraping(country)
            # collected_count += result.get("count", 0)

            # 설정 업데이트
            config.last_run_at = datetime.utcnow()
            config.next_run_at = datetime.utcnow() + timedelta(hours=config.interval_hours)
            config.status = "idle"
            config.last_error = None
            self.db.commit()

            return {
                "success": True,
                "collected_count": collected_count,
                "errors": errors if errors else None
            }

        except Exception as e:
            config.status = "error"
            config.last_error = str(e)
            self.db.commit()
            return {"success": False, "error": str(e)}

    async def _collect_from_newsapi(self, country: Country, keywords: List[str]) -> dict:
        """NewsAPI에서 뉴스 수집"""
        if not self.newsapi_key:
            return {"count": 0, "error": "NewsAPI key not configured"}

        collected = 0
        country_names = {
            "MM": "Myanmar",
            "ID": "Indonesia"
        }
        country_name = country_names.get(country.code, country.name_en)

        try:
            async with httpx.AsyncClient() as client:
                for keyword in keywords:
                    query = f"{country_name} {keyword}"
                    url = "https://newsapi.org/v2/everything"
                    params = {
                        "q": query,
                        "apiKey": self.newsapi_key,
                        "language": "en",
                        "sortBy": "publishedAt",
                        "pageSize": 10,
                        "from": (datetime.utcnow() - timedelta(days=7)).isoformat()
                    }

                    response = await client.get(url, params=params)
                    if response.status_code != 200:
                        continue

                    data = response.json()
                    articles = data.get("articles", [])

                    for article in articles:
                        # 중복 체크
                        existing = self.db.query(News).filter(
                            News.title == article["title"],
                            News.country_id == country.id
                        ).first()

                        if not existing:
                            # 카테고리 자동 분류
                            category = self._classify_category(article["title"], article.get("description", ""))

                            news = News(
                                country_id=country.id,
                                title=article["title"],
                                content=article.get("description") or article.get("content"),
                                source=article["source"]["name"],
                                url=article["url"],
                                category=category,
                                published_at=datetime.fromisoformat(article["publishedAt"].replace("Z", "+00:00")),
                                source_type="api"
                            )
                            self.db.add(news)
                            collected += 1

            self.db.commit()
            return {"count": collected}

        except Exception as e:
            return {"count": collected, "error": str(e)}

    def _classify_category(self, title: str, description: str) -> str:
        """제목과 내용으로 카테고리 자동 분류"""
        text = f"{title} {description}".lower()

        regulation_keywords = ["regulation", "policy", "law", "central bank", "financial authority", "ojk", "cbm", "rule", "compliance"]
        geopolitical_keywords = ["conflict", "tension", "political", "military", "election", "government", "crisis", "sanction"]
        economic_keywords = ["economy", "gdp", "trade", "export", "import", "inflation", "growth", "investment", "market"]

        if any(keyword in text for keyword in regulation_keywords):
            return "regulation"
        elif any(keyword in text for keyword in geopolitical_keywords):
            return "geopolitical"
        elif any(keyword in text for keyword in economic_keywords):
            return "economic"
        else:
            return "other"

    def _get_default_keywords(self, country_code: str) -> List[str]:
        """기본 검색 키워드"""
        common_keywords = [
            "financial regulation",
            "central bank",
            "economy",
            "investment",
            "trade"
        ]

        country_keywords = {
            "MM": ["CBM", "Myanmar central bank", "Myanmar economy"],
            "ID": ["OJK", "Bank Indonesia", "Indonesian economy"]
        }

        return common_keywords + country_keywords.get(country_code, [])
