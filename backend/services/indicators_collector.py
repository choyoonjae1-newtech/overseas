"""
경제 지표 자동 수집 서비스
"""
import httpx
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.country import Country
from models.indicator import EconomicIndicator
from core.database import SessionLocal
import logging

logger = logging.getLogger(__name__)


class IndicatorsCollector:
    """경제 지표 수집기"""

    # 데이터 소스 URL
    SOURCES = {
        "MM": {
            "exchange_rate": "https://www.cbm.gov.mm/content/exchange-rate",
            "gdp_growth": "https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG?locations=MM",
            "inflation": "https://www.csostat.gov.mm/",
            "interest_rate": "https://www.cbm.gov.mm/content/monetary-policy",
            "forex_reserve": "https://www.cbm.gov.mm/content/foreign-reserve"
        },
        "ID": {
            "exchange_rate": "https://www.bi.go.id/en/statistik/informasi-kurs/transaksi-bi/default.aspx",
            "gdp_growth": "https://www.bps.go.id/en/statistics-table/2/MTk3IzI=/gross-domestic-product.html",
            "inflation": "https://www.bps.go.id/en/statistics-table/2/MTI3NiMy/inflation-rate.html",
            "interest_rate": "https://www.bi.go.id/en/fungsi-utama/moneter/bi-7day-rr/default.aspx",
            "forex_reserve": "https://www.bi.go.id/en/statistik/ekonomi-keuangan/sdsk/Default.aspx"
        }
    }

    async def collect_all_indicators(self):
        """모든 국가의 경제 지표 수집"""
        db = SessionLocal()
        try:
            countries = db.query(Country).all()
            for country in countries:
                await self.collect_country_indicators(country.code, db)
        finally:
            db.close()

    async def collect_country_indicators(self, country_code: str, db: Session = None):
        """특정 국가의 경제 지표 수집"""
        should_close = False
        if db is None:
            db = SessionLocal()
            should_close = True

        try:
            country = db.query(Country).filter(Country.code == country_code).first()
            if not country:
                logger.error(f"국가를 찾을 수 없습니다: {country_code}")
                return

            logger.info(f"📊 [{country_code}] 경제 지표 수집 시작...")

            # World Bank API를 통한 GDP 성장률 수집 시도
            collected_count = 0

            # GDP 성장률
            gdp_data = await self._fetch_worldbank_gdp(country_code)
            if gdp_data:
                collected_count += await self._save_indicator(
                    db, country.id, "gdp_growth", gdp_data,
                    self.SOURCES.get(country_code, {}).get("gdp_growth", "World Bank")
                )

            # 환율 (실제 구현 시 각 중앙은행 API 사용)
            # 현재는 mock 데이터로 대체
            logger.info(f"  ℹ️  실제 API 연동은 추후 구현 예정 (현재는 수동 데이터 사용)")

            logger.info(f"✅ [{country_code}] 경제 지표 {collected_count}개 수집 완료")

        except Exception as e:
            logger.error(f"❌ [{country_code}] 경제 지표 수집 실패: {e}")
        finally:
            if should_close:
                db.close()

    async def _fetch_worldbank_gdp(self, country_code: str):
        """World Bank API로 GDP 성장률 조회"""
        try:
            # World Bank API 국가 코드 매핑
            wb_codes = {"MM": "MMR", "ID": "IDN"}
            wb_code = wb_codes.get(country_code)

            if not wb_code:
                return None

            # 최근 5년 데이터 조회
            current_year = datetime.now().year
            url = f"https://api.worldbank.org/v2/country/{wb_code}/indicator/NY.GDP.MKTP.KD.ZG"
            params = {
                "format": "json",
                "date": f"{current_year-5}:{current_year}",
                "per_page": 10
            }

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, params=params)

                if response.status_code == 200:
                    data = response.json()
                    if len(data) > 1 and data[1]:
                        # 가장 최근 데이터
                        latest = data[1][0]
                        if latest.get("value"):
                            return {
                                "value": round(float(latest["value"]), 2),
                                "period": str(latest["date"]),
                                "unit": "%",
                                "source": "World Bank"
                            }
        except Exception as e:
            logger.warning(f"World Bank API 조회 실패: {e}")

        return None

    async def _save_indicator(self, db: Session, country_id: int, indicator_type: str,
                             data: dict, source_url: str) -> int:
        """지표 데이터 저장"""
        try:
            # 중복 확인
            existing = db.query(EconomicIndicator).filter(
                EconomicIndicator.country_id == country_id,
                EconomicIndicator.indicator_type == indicator_type,
                EconomicIndicator.period == data["period"]
            ).first()

            if existing:
                # 업데이트
                existing.value = data["value"]
                existing.unit = data.get("unit")
                existing.source = data.get("source")
                existing.note = f"자동 수집 - {source_url}"
                db.commit()
                return 1
            else:
                # 신규 생성
                indicator = EconomicIndicator(
                    country_id=country_id,
                    indicator_type=indicator_type,
                    value=data["value"],
                    unit=data.get("unit"),
                    period=data["period"],
                    recorded_at=datetime.now(),
                    source=data.get("source"),
                    note=f"자동 수집 - {source_url}"
                )
                db.add(indicator)
                db.commit()
                return 1
        except Exception as e:
            logger.error(f"지표 저장 실패: {e}")
            db.rollback()
            return 0


# 싱글톤 인스턴스
indicators_collector = IndicatorsCollector()
