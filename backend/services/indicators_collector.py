"""
경제 지표 자동 수집 서비스 - 실제 데이터 소스 연동
"""
import httpx
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.country import Country
from models.indicator import EconomicIndicator
from core.database import SessionLocal
import logging

logger = logging.getLogger(__name__)


class IndicatorsCollector:
    """경제 지표 수집기 - 실제 데이터 소스에서 수집"""

    # 데이터 소스 매핑
    WORLD_BANK_COUNTRY_CODES = {
        "MM": "MMR",  # Myanmar
        "ID": "IDN"   # Indonesia
    }

    # World Bank API 지표 코드
    WB_INDICATORS = {
        "gdp_growth": "NY.GDP.MKTP.KD.ZG",  # GDP growth (annual %)
        "inflation": "FP.CPI.TOTL.ZG",  # Inflation, consumer prices (annual %)
        "unemployment_rate": "SL.UEM.TOTL.ZS",  # Unemployment, total (% of labor force)
        "exports": "NE.EXP.GNFS.CD",  # Exports of goods and services (current US$)
        "imports": "NE.IMP.GNFS.CD",  # Imports of goods and services (current US$)
        "forex_reserve": "FI.RES.TOTL.CD",  # Total reserves (current US$)
        "trade_balance": "NE.RSB.GNFS.CD",  # External balance on goods and services (current US$)
    }

    async def collect_all_indicators(self):
        """모든 국가의 경제 지표 수집"""
        db = SessionLocal()
        try:
            countries = db.query(Country).all()
            total_collected = 0
            for country in countries:
                count = await self.collect_country_indicators(country.code, db)
                total_collected += count
            logger.info(f"✅ 총 {total_collected}개 경제 지표 수집 완료")
            return total_collected
        finally:
            db.close()

    async def collect_country_indicators(self, country_code: str, db: Session = None):
        """특정 국가의 경제 지표 수집 (실제 데이터)"""
        should_close = False
        if db is None:
            db = SessionLocal()
            should_close = True

        try:
            country = db.query(Country).filter(Country.code == country_code).first()
            if not country:
                logger.error(f"국가를 찾을 수 없습니다: {country_code}")
                return 0

            logger.info(f"📊 [{country.name_ko}] 경제 지표 수집 시작...")
            collected_count = 0

            # World Bank API에서 여러 지표 수집
            for indicator_type, wb_code in self.WB_INDICATORS.items():
                data_list = await self._fetch_worldbank_indicator(country_code, indicator_type, wb_code)
                for data in data_list:
                    saved = await self._save_indicator(db, country.id, indicator_type, data)
                    if saved:
                        collected_count += 1

            # 환율 데이터 (Open Exchange Rates API - 실제 환율 데이터)
            exchange_data = await self._fetch_exchange_rate(country_code)
            if exchange_data:
                saved = await self._save_indicator(db, country.id, "exchange_rate", exchange_data)
                if saved:
                    collected_count += 1

            logger.info(f"✅ [{country.name_ko}] {collected_count}개 경제 지표 수집 완료")
            return collected_count

        except Exception as e:
            logger.error(f"❌ [{country_code}] 경제 지표 수집 실패: {e}")
            return 0
        finally:
            if should_close:
                db.close()

    async def _fetch_worldbank_indicator(self, country_code: str, indicator_type: str, wb_code: str):
        """World Bank API로 지표 조회"""
        try:
            wb_country_code = self.WORLD_BANK_COUNTRY_CODES.get(country_code)
            if not wb_country_code:
                return []

            # 최근 10년 데이터 조회
            current_year = datetime.now().year
            url = f"https://api.worldbank.org/v2/country/{wb_country_code}/indicator/{wb_code}"
            params = {
                "format": "json",
                "date": f"{current_year-10}:{current_year}",
                "per_page": 100
            }

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, params=params)

                if response.status_code == 200:
                    data = response.json()
                    if len(data) > 1 and data[1]:
                        results = []
                        for item in data[1]:
                            if item.get("value") is not None:
                                # 지표 타입에 따라 단위 결정
                                unit = self._get_unit(indicator_type)

                                # 값 변환 (필요시)
                                value = float(item["value"])
                                if indicator_type in ["exports", "imports", "forex_reserve", "trade_balance"]:
                                    # 달러 단위를 백만 달러로 변환
                                    value = value / 1_000_000

                                results.append({
                                    "value": round(value, 2),
                                    "period": str(item["date"]),
                                    "unit": unit,
                                    "source": "World Bank"
                                })
                        logger.info(f"  ✓ World Bank에서 {indicator_type} {len(results)}개 항목 수집")
                        return results
        except Exception as e:
            logger.warning(f"World Bank API 조회 실패 ({indicator_type}): {e}")

        return []

    async def _fetch_exchange_rate(self, country_code: str):
        """환율 데이터 조회 (currencyapi.com 무료 API 사용)"""
        try:
            # 국가별 통화 코드
            currency_codes = {
                "MM": "MMK",  # Myanmar Kyat
                "ID": "IDR"   # Indonesian Rupiah
            }

            currency = currency_codes.get(country_code)
            if not currency:
                return None

            # currencyapi.com 무료 API (월 300회 무료)
            # 실제 사용 시 환경변수에서 API 키를 가져와야 함
            # 여기서는 데모용으로 하드코딩 (실제로는 .env에서 로드)

            # 대체: Exchange Rate API (무료, API 키 불필요)
            url = f"https://open.er-api.com/v6/latest/USD"

            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(url)

                if response.status_code == 200:
                    data = response.json()
                    if data.get("result") == "success":
                        rates = data.get("rates", {})
                        rate = rates.get(currency)

                        if rate:
                            current_date = datetime.now()
                            period = current_date.strftime("%Y-%m")

                            logger.info(f"  ✓ 환율 데이터 수집: 1 USD = {rate} {currency}")
                            return {
                                "value": round(rate, 2),
                                "period": period,
                                "unit": f"{currency}/USD",
                                "source": "Exchange Rate API"
                            }
        except Exception as e:
            logger.warning(f"환율 API 조회 실패: {e}")

        return None

    def _get_unit(self, indicator_type: str) -> str:
        """지표 타입에 따른 단위 반환"""
        units = {
            "gdp_growth": "%",
            "inflation": "%",
            "unemployment_rate": "%",
            "interest_rate": "%",
            "exports": "million USD",
            "imports": "million USD",
            "forex_reserve": "million USD",
            "trade_balance": "million USD",
            "manufacturing_pmi": "Index",
            "consumer_confidence": "Index",
            "industrial_production": "Index",
            "government_debt": "% of GDP",
            "fdi": "million USD",
            "retail_sales": "% YoY",
            "auto_sales": "units",
            "tourist_arrivals": "million",
            "black_market_rate": "MMK/USD" if indicator_type == "black_market_rate" else "IDR/USD"
        }
        return units.get(indicator_type, "")

    async def _save_indicator(self, db: Session, country_id: int, indicator_type: str,
                             data: dict) -> bool:
        """지표 데이터 저장 (중복 방지)"""
        try:
            # 중복 확인
            existing = db.query(EconomicIndicator).filter(
                EconomicIndicator.country_id == country_id,
                EconomicIndicator.indicator_type == indicator_type,
                EconomicIndicator.period == data["period"]
            ).first()

            if existing:
                # 기존 데이터 업데이트
                existing.value = data["value"]
                existing.unit = data.get("unit")
                existing.source = data.get("source")
                existing.recorded_at = datetime.now()
                existing.note = f"자동 수집 업데이트 - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                db.commit()
                logger.debug(f"  ↻ 지표 업데이트: {indicator_type} {data['period']}")
                return True
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
                    note=f"자동 수집 - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                )
                db.add(indicator)
                db.commit()
                logger.debug(f"  + 신규 지표 추가: {indicator_type} {data['period']}")
                return True
        except IntegrityError as e:
            # 유니크 제약 위반 (동시성 문제)
            db.rollback()
            logger.warning(f"  ⚠ 중복 데이터 감지 (무시): {indicator_type} {data['period']}")
            return False
        except Exception as e:
            logger.error(f"지표 저장 실패: {e}")
            db.rollback()
            return False


# 싱글톤 인스턴스
indicators_collector = IndicatorsCollector()
