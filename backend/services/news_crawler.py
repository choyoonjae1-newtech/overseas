"""
뉴스 및 공시 크롤링 서비스
- 미얀마: Central Bank of Myanmar (CBM)
- 인도네시아: Otoritas Jasa Keuangan (OJK)
"""
import httpx
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
from sqlalchemy.orm import Session
from models import News, Country
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger(__name__)


class NewsCrawler:
    """뉴스 및 금융 규제 공시 크롤러"""

    def __init__(self):
        self.timeout = 30.0
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

    async def crawl_cbm_news(self, db: Session) -> int:
        """
        미얀마 중앙은행(CBM) 뉴스 크롤링
        URL: https://www.cbm.gov.mm/news
        """
        try:
            logger.info("🇲🇲 CBM 뉴스 크롤링 시작...")
            url = "https://www.cbm.gov.mm/news"

            async with httpx.AsyncClient(timeout=self.timeout, headers=self.headers) as client:
                response = await client.get(url)
                response.raise_for_status()

            soup = BeautifulSoup(response.content, 'lxml')

            # CBM 웹사이트 구조에 맞게 파싱
            # 실제 구조는 웹사이트에 따라 다를 수 있으므로 조정 필요
            news_items = soup.find_all('div', class_='news-item')  # 예시 클래스명

            count = 0
            myanmar = db.query(Country).filter(Country.code == 'MM').first()

            if not myanmar:
                logger.error("미얀마 국가 정보를 찾을 수 없습니다")
                return 0

            for item in news_items[:10]:  # 최근 10개만 수집
                try:
                    title_elem = item.find('h3') or item.find('h2') or item.find('a')
                    if not title_elem:
                        continue

                    title = title_elem.get_text(strip=True)

                    # 날짜 파싱 (CBM 웹사이트 형식에 맞게 조정)
                    date_elem = item.find('span', class_='date') or item.find('time')
                    published_at = None
                    if date_elem:
                        try:
                            date_text = date_elem.get_text(strip=True)
                            published_at = datetime.strptime(date_text, '%d-%m-%Y')  # 예시 포맷
                        except:
                            published_at = datetime.now()

                    # URL 파싱
                    link_elem = item.find('a')
                    url_path = link_elem.get('href') if link_elem else None
                    full_url = f"https://www.cbm.gov.mm{url_path}" if url_path and url_path.startswith('/') else url_path

                    # 카테고리 자동 분류
                    category = self._classify_category(title)

                    # 데이터베이스에 저장 (중복 방지)
                    news = News(
                        country_id=myanmar.id,
                        title=title,
                        content=None,  # 상세 내용은 별도 크롤링 필요
                        source='Central Bank of Myanmar',
                        url=full_url,
                        category=category,
                        published_at=published_at or datetime.now(),
                        source_type='crawl'
                    )

                    try:
                        db.add(news)
                        db.commit()
                        count += 1
                    except IntegrityError:
                        db.rollback()
                        logger.debug(f"중복 뉴스 무시: {title[:50]}")

                except Exception as e:
                    logger.error(f"CBM 뉴스 항목 파싱 오류: {e}")
                    continue

            logger.info(f"✅ CBM 뉴스 {count}개 수집 완료")
            return count

        except Exception as e:
            logger.error(f"❌ CBM 크롤링 실패: {e}")
            return 0

    async def crawl_ojk_announcements(self, db: Session) -> int:
        """
        인도네시아 금융감독청(OJK) 공시 크롤링
        URL: https://www.ojk.go.id/id/kanal/pasar-modal/regulasi
        """
        try:
            logger.info("🇮🇩 OJK 공시 크롤링 시작...")
            url = "https://www.ojk.go.id/id/kanal/pasar-modal/regulasi"

            async with httpx.AsyncClient(timeout=self.timeout, headers=self.headers) as client:
                response = await client.get(url)
                response.raise_for_status()

            soup = BeautifulSoup(response.content, 'lxml')

            # OJK 웹사이트 구조에 맞게 파싱
            regulation_items = soup.find_all('div', class_='regulation-item')  # 예시 클래스명

            count = 0
            indonesia = db.query(Country).filter(Country.code == 'ID').first()

            if not indonesia:
                logger.error("인도네시아 국가 정보를 찾을 수 없습니다")
                return 0

            for item in regulation_items[:10]:  # 최근 10개만 수집
                try:
                    title_elem = item.find('h3') or item.find('h4') or item.find('a')
                    if not title_elem:
                        continue

                    title = title_elem.get_text(strip=True)

                    # 날짜 파싱
                    date_elem = item.find('span', class_='date') or item.find('time')
                    published_at = None
                    if date_elem:
                        try:
                            date_text = date_elem.get_text(strip=True)
                            published_at = datetime.strptime(date_text, '%d %B %Y')  # 예시: "15 January 2026"
                        except:
                            published_at = datetime.now()

                    # URL 파싱
                    link_elem = item.find('a')
                    url_path = link_elem.get('href') if link_elem else None
                    full_url = f"https://www.ojk.go.id{url_path}" if url_path and url_path.startswith('/') else url_path

                    # 카테고리: OJK는 주로 금융규제
                    category = 'regulation'

                    # 데이터베이스에 저장
                    news = News(
                        country_id=indonesia.id,
                        title=title,
                        content=None,
                        source='Otoritas Jasa Keuangan (OJK)',
                        url=full_url,
                        category=category,
                        published_at=published_at or datetime.now(),
                        source_type='crawl'
                    )

                    try:
                        db.add(news)
                        db.commit()
                        count += 1
                    except IntegrityError:
                        db.rollback()
                        logger.debug(f"중복 뉴스 무시: {title[:50]}")

                except Exception as e:
                    logger.error(f"OJK 공시 항목 파싱 오류: {e}")
                    continue

            logger.info(f"✅ OJK 공시 {count}개 수집 완료")
            return count

        except Exception as e:
            logger.error(f"❌ OJK 크롤링 실패: {e}")
            return 0

    async def crawl_generic_news(self, country_code: str, url: str, db: Session) -> int:
        """
        범용 뉴스 크롤러
        - RSS 피드나 기본 HTML 구조를 파싱
        """
        try:
            logger.info(f"🌐 범용 크롤링 시작: {url}")

            async with httpx.AsyncClient(timeout=self.timeout, headers=self.headers) as client:
                response = await client.get(url)
                response.raise_for_status()

            soup = BeautifulSoup(response.content, 'lxml')

            # 일반적인 뉴스 아티클 구조 파싱
            articles = soup.find_all('article') or soup.find_all('div', class_=['news', 'post', 'article'])

            count = 0
            country = db.query(Country).filter(Country.code == country_code).first()

            if not country:
                logger.error(f"국가 정보를 찾을 수 없습니다: {country_code}")
                return 0

            for article in articles[:10]:
                try:
                    # 제목 추출
                    title_elem = article.find(['h1', 'h2', 'h3', 'h4'])
                    if not title_elem:
                        continue

                    title = title_elem.get_text(strip=True)

                    # 링크 추출
                    link = article.find('a')
                    article_url = link.get('href') if link else None

                    # 카테고리 자동 분류
                    category = self._classify_category(title)

                    news = News(
                        country_id=country.id,
                        title=title,
                        content=None,
                        source=url,
                        url=article_url,
                        category=category,
                        published_at=datetime.now(),
                        source_type='crawl'
                    )

                    try:
                        db.add(news)
                        db.commit()
                        count += 1
                    except IntegrityError:
                        db.rollback()

                except Exception as e:
                    logger.error(f"뉴스 항목 파싱 오류: {e}")
                    continue

            logger.info(f"✅ 범용 크롤링 {count}개 수집 완료")
            return count

        except Exception as e:
            logger.error(f"❌ 범용 크롤링 실패: {e}")
            return 0

    def _classify_category(self, title: str) -> str:
        """
        제목을 기반으로 카테고리 자동 분류
        """
        title_lower = title.lower()

        # 금융규제 키워드
        regulation_keywords = ['regulation', 'policy', 'directive', 'guideline', 'circular',
                               'rule', 'requirement', 'compliance', 'licensing', 'supervision',
                               '규제', '정책', '지침', '허가', '감독']

        # 지정학적 키워드
        geopolitical_keywords = ['political', 'military', 'conflict', 'sanction', 'coup',
                                 'election', 'government', 'crisis', 'protest',
                                 '정치', '군사', '분쟁', '제재', '선거', '정부', '위기']

        # 경제 키워드
        economic_keywords = ['economic', 'gdp', 'inflation', 'trade', 'export', 'import',
                             'investment', 'growth', 'recession', 'currency', 'exchange',
                             '경제', '성장', '무역', '투자', '환율', '인플레이션']

        if any(keyword in title_lower for keyword in regulation_keywords):
            return 'regulation'
        elif any(keyword in title_lower for keyword in geopolitical_keywords):
            return 'geopolitical'
        elif any(keyword in title_lower for keyword in economic_keywords):
            return 'economic'
        else:
            return 'other'

    async def crawl_all(self, db: Session) -> Dict[str, int]:
        """
        모든 소스에서 뉴스 수집
        """
        results = {
            'cbm': 0,
            'ojk': 0,
            'total': 0
        }

        try:
            # CBM 크롤링
            cbm_count = await self.crawl_cbm_news(db)
            results['cbm'] = cbm_count

            # OJK 크롤링
            ojk_count = await self.crawl_ojk_announcements(db)
            results['ojk'] = ojk_count

            results['total'] = cbm_count + ojk_count

            logger.info(f"🎉 전체 크롤링 완료: CBM {cbm_count}개, OJK {ojk_count}개 (총 {results['total']}개)")

        except Exception as e:
            logger.error(f"❌ 전체 크롤링 오류: {e}")

        return results


# 싱글톤 인스턴스
news_crawler = NewsCrawler()
