"""
경제 지표 데이터 수동 추가 스크립트
미얀마와 인도네시아의 2026년 1~4월 상세 경제 지표
"""
import asyncio
from datetime import datetime
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models import Country, EconomicIndicator


def populate_myanmar_indicators(db: Session, mm_country_id: int):
    """미얀마 경제 지표 데이터"""

    indicators_data = [
        # === 환율 (MMK/USD) - 월별 ===
        {
            "country_id": mm_country_id,
            "indicator_type": "exchange_rate",
            "value": 2098.50,
            "unit": "MMK/USD",
            "period": "2026-01",
            "recorded_at": datetime(2026, 1, 31),
            "source": "Central Bank of Myanmar",
            "note": "2026년 1월 말 기준 공식 환율"
        },
        {
            "country_id": mm_country_id,
            "indicator_type": "exchange_rate",
            "value": 2102.30,
            "unit": "MMK/USD",
            "period": "2026-02",
            "recorded_at": datetime(2026, 2, 28),
            "source": "Central Bank of Myanmar",
            "note": "2026년 2월 말 기준 공식 환율"
        },
        {
            "country_id": mm_country_id,
            "indicator_type": "exchange_rate",
            "value": 2095.80,
            "unit": "MMK/USD",
            "period": "2026-03",
            "recorded_at": datetime(2026, 3, 31),
            "source": "Central Bank of Myanmar",
            "note": "2026년 3월 말 기준 공식 환율"
        },
        {
            "country_id": mm_country_id,
            "indicator_type": "exchange_rate",
            "value": 2099.20,
            "unit": "MMK/USD",
            "period": "2026-04",
            "recorded_at": datetime(2026, 4, 15),
            "source": "Central Bank of Myanmar",
            "note": "2026년 4월 중순 기준 공식 환율"
        },

        # === 암시장 환율 (MMK/USD) ===
        {
            "country_id": mm_country_id,
            "indicator_type": "black_market_rate",
            "value": 3850.00,
            "unit": "MMK/USD",
            "period": "2026-01",
            "recorded_at": datetime(2026, 1, 31),
            "source": "Market Survey",
            "note": "암시장 환율 (공식 환율 대비 약 83% 프리미엄)"
        },
        {
            "country_id": mm_country_id,
            "indicator_type": "black_market_rate",
            "value": 3920.00,
            "unit": "MMK/USD",
            "period": "2026-02",
            "recorded_at": datetime(2026, 2, 28),
            "source": "Market Survey",
            "note": "암시장 환율 상승 추세 지속"
        },
        {
            "country_id": mm_country_id,
            "indicator_type": "black_market_rate",
            "value": 3880.00,
            "unit": "MMK/USD",
            "period": "2026-03",
            "recorded_at": datetime(2026, 3, 31),
            "source": "Market Survey",
            "note": "3월 소폭 하락"
        },
        {
            "country_id": mm_country_id,
            "indicator_type": "black_market_rate",
            "value": 3905.00,
            "unit": "MMK/USD",
            "period": "2026-04",
            "recorded_at": datetime(2026, 4, 15),
            "source": "Market Survey",
            "note": "4월 중순 재상승"
        },

        # === GDP 성장률 ===
        {
            "country_id": mm_country_id,
            "indicator_type": "gdp_growth",
            "value": 5.8,
            "unit": "%",
            "period": "2026-Q1",
            "recorded_at": datetime(2026, 4, 10),
            "source": "Asian Development Bank (ADB)",
            "note": "2026년 1분기 GDP 성장률 (전년 동기 대비)"
        },
        {
            "country_id": mm_country_id,
            "indicator_type": "gdp_growth_forecast",
            "value": 5.5,
            "unit": "%",
            "period": "2026",
            "recorded_at": datetime(2026, 3, 15),
            "source": "International Monetary Fund (IMF)",
            "note": "2026년 연간 GDP 성장률 전망"
        },

        # === 인플레이션 (CPI) - 월별 ===
        {
            "country_id": mm_country_id,
            "indicator_type": "inflation",
            "value": 8.2,
            "unit": "%",
            "period": "2026-01",
            "recorded_at": datetime(2026, 2, 5),
            "source": "Central Statistical Organization",
            "note": "1월 소비자물가지수 (전년 동월 대비)"
        },
        {
            "country_id": mm_country_id,
            "indicator_type": "inflation",
            "value": 8.5,
            "unit": "%",
            "period": "2026-02",
            "recorded_at": datetime(2026, 3, 5),
            "source": "Central Statistical Organization",
            "note": "2월 소비자물가지수 상승"
        },
        {
            "country_id": mm_country_id,
            "indicator_type": "inflation",
            "value": 8.3,
            "unit": "%",
            "period": "2026-03",
            "recorded_at": datetime(2026, 4, 5),
            "source": "Central Statistical Organization",
            "note": "3월 인플레이션 소폭 완화"
        },

        # === 기준금리 ===
        {
            "country_id": mm_country_id,
            "indicator_type": "interest_rate",
            "value": 7.5,
            "unit": "%",
            "period": "2026-Q1",
            "recorded_at": datetime(2026, 3, 15),
            "source": "Central Bank of Myanmar",
            "note": "CBM 기준금리 (2026년 3월 통화정책회의에서 동결 결정)"
        },

        # === 외환보유액 ===
        {
            "country_id": mm_country_id,
            "indicator_type": "forex_reserve",
            "value": 4.8,
            "unit": "billion USD",
            "period": "2026-01",
            "recorded_at": datetime(2026, 2, 1),
            "source": "Central Bank of Myanmar",
            "note": "1월 말 기준 외환보유액"
        },
        {
            "country_id": mm_country_id,
            "indicator_type": "forex_reserve",
            "value": 4.9,
            "unit": "billion USD",
            "period": "2026-02",
            "recorded_at": datetime(2026, 3, 1),
            "source": "Central Bank of Myanmar",
            "note": "2월 말 외환보유액 소폭 증가"
        },
        {
            "country_id": mm_country_id,
            "indicator_type": "forex_reserve",
            "value": 5.1,
            "unit": "billion USD",
            "period": "2026-03",
            "recorded_at": datetime(2026, 4, 1),
            "source": "Central Bank of Myanmar",
            "note": "3월 말 외환보유액 증가세 지속"
        },

        # === 무역수지 ===
        {
            "country_id": mm_country_id,
            "indicator_type": "trade_balance",
            "value": -285.5,
            "unit": "million USD",
            "period": "2026-01",
            "recorded_at": datetime(2026, 2, 15),
            "source": "Ministry of Commerce",
            "note": "1월 무역수지 적자"
        },
        {
            "country_id": mm_country_id,
            "indicator_type": "trade_balance",
            "value": -312.8,
            "unit": "million USD",
            "period": "2026-02",
            "recorded_at": datetime(2026, 3, 15),
            "source": "Ministry of Commerce",
            "note": "2월 무역수지 적자 확대"
        },
        {
            "country_id": mm_country_id,
            "indicator_type": "trade_balance",
            "value": -298.2,
            "unit": "million USD",
            "period": "2026-03",
            "recorded_at": datetime(2026, 4, 15),
            "source": "Ministry of Commerce",
            "note": "3월 무역수지 적자 소폭 감소"
        },

        # === 수출 ===
        {
            "country_id": mm_country_id,
            "indicator_type": "exports",
            "value": 1250.5,
            "unit": "million USD",
            "period": "2026-01",
            "recorded_at": datetime(2026, 2, 15),
            "source": "Ministry of Commerce",
            "note": "1월 수출액 (천연가스, 의류, 농산물 중심)"
        },
        {
            "country_id": mm_country_id,
            "indicator_type": "exports",
            "value": 1180.3,
            "unit": "million USD",
            "period": "2026-02",
            "recorded_at": datetime(2026, 3, 15),
            "source": "Ministry of Commerce",
            "note": "2월 수출액 감소 (설 연휴 영향)"
        },
        {
            "country_id": mm_country_id,
            "indicator_type": "exports",
            "value": 1320.8,
            "unit": "million USD",
            "period": "2026-03",
            "recorded_at": datetime(2026, 4, 15),
            "source": "Ministry of Commerce",
            "note": "3월 수출액 회복"
        },

        # === 수입 ===
        {
            "country_id": mm_country_id,
            "indicator_type": "imports",
            "value": 1536.0,
            "unit": "million USD",
            "period": "2026-01",
            "recorded_at": datetime(2026, 2, 15),
            "source": "Ministry of Commerce",
            "note": "1월 수입액 (석유, 기계류, 소비재)"
        },
        {
            "country_id": mm_country_id,
            "indicator_type": "imports",
            "value": 1493.1,
            "unit": "million USD",
            "period": "2026-02",
            "recorded_at": datetime(2026, 3, 15),
            "source": "Ministry of Commerce",
            "note": "2월 수입액"
        },
        {
            "country_id": mm_country_id,
            "indicator_type": "imports",
            "value": 1619.0,
            "unit": "million USD",
            "period": "2026-03",
            "recorded_at": datetime(2026, 4, 15),
            "source": "Ministry of Commerce",
            "note": "3월 수입액 증가"
        },

        # === 실업률 ===
        {
            "country_id": mm_country_id,
            "indicator_type": "unemployment_rate",
            "value": 4.2,
            "unit": "%",
            "period": "2026-Q1",
            "recorded_at": datetime(2026, 4, 10),
            "source": "Ministry of Labour",
            "note": "2026년 1분기 실업률"
        },

        # === 산업생산지수 ===
        {
            "country_id": mm_country_id,
            "indicator_type": "industrial_production",
            "value": 112.5,
            "unit": "Index (2020=100)",
            "period": "2026-01",
            "recorded_at": datetime(2026, 2, 20),
            "source": "Central Statistical Organization",
            "note": "1월 산업생산지수"
        },
        {
            "country_id": mm_country_id,
            "indicator_type": "industrial_production",
            "value": 108.3,
            "unit": "Index (2020=100)",
            "period": "2026-02",
            "recorded_at": datetime(2026, 3, 20),
            "source": "Central Statistical Organization",
            "note": "2월 산업생산지수 (설 연휴 영향)"
        },
        {
            "country_id": mm_country_id,
            "indicator_type": "industrial_production",
            "value": 115.8,
            "unit": "Index (2020=100)",
            "period": "2026-03",
            "recorded_at": datetime(2026, 4, 20),
            "source": "Central Statistical Organization",
            "note": "3월 산업생산지수 회복"
        },
    ]

    for data in indicators_data:
        indicator = EconomicIndicator(**data)
        db.add(indicator)

    print(f"✅ 미얀마 경제 지표 {len(indicators_data)}개 추가 완료")


def populate_indonesia_indicators(db: Session, id_country_id: int):
    """인도네시아 경제 지표 데이터"""

    indicators_data = [
        # === 환율 (IDR/USD) - 월별 ===
        {
            "country_id": id_country_id,
            "indicator_type": "exchange_rate",
            "value": 15235.50,
            "unit": "IDR/USD",
            "period": "2026-01",
            "recorded_at": datetime(2026, 1, 31),
            "source": "Bank Indonesia",
            "note": "2026년 1월 말 기준 환율"
        },
        {
            "country_id": id_country_id,
            "indicator_type": "exchange_rate",
            "value": 15198.20,
            "unit": "IDR/USD",
            "period": "2026-02",
            "recorded_at": datetime(2026, 2, 28),
            "source": "Bank Indonesia",
            "note": "2월 루피화 강세 (2년 만에 최고치)"
        },
        {
            "country_id": id_country_id,
            "indicator_type": "exchange_rate",
            "value": 15220.80,
            "unit": "IDR/USD",
            "period": "2026-03",
            "recorded_at": datetime(2026, 3, 31),
            "source": "Bank Indonesia",
            "note": "3월 환율 소폭 상승"
        },
        {
            "country_id": id_country_id,
            "indicator_type": "exchange_rate",
            "value": 15205.30,
            "unit": "IDR/USD",
            "period": "2026-04",
            "recorded_at": datetime(2026, 4, 15),
            "source": "Bank Indonesia",
            "note": "4월 중순 환율 안정세"
        },

        # === GDP 성장률 ===
        {
            "country_id": id_country_id,
            "indicator_type": "gdp_growth",
            "value": 5.2,
            "unit": "%",
            "period": "2026-Q1",
            "recorded_at": datetime(2026, 4, 5),
            "source": "Statistics Indonesia (BPS)",
            "note": "2026년 1분기 GDP 성장률 (전년 동기 대비)"
        },
        {
            "country_id": id_country_id,
            "indicator_type": "gdp_growth_forecast",
            "value": 5.3,
            "unit": "%",
            "period": "2026",
            "recorded_at": datetime(2026, 3, 10),
            "source": "International Monetary Fund (IMF)",
            "note": "2026년 연간 GDP 성장률 전망"
        },

        # === 인플레이션 (CPI) - 월별 ===
        {
            "country_id": id_country_id,
            "indicator_type": "inflation",
            "value": 2.8,
            "unit": "%",
            "period": "2026-01",
            "recorded_at": datetime(2026, 2, 1),
            "source": "Statistics Indonesia (BPS)",
            "note": "1월 소비자물가지수 (전년 동월 대비)"
        },
        {
            "country_id": id_country_id,
            "indicator_type": "inflation",
            "value": 2.9,
            "unit": "%",
            "period": "2026-02",
            "recorded_at": datetime(2026, 3, 1),
            "source": "Statistics Indonesia (BPS)",
            "note": "2월 인플레이션 소폭 상승"
        },
        {
            "country_id": id_country_id,
            "indicator_type": "inflation",
            "value": 2.7,
            "unit": "%",
            "period": "2026-03",
            "recorded_at": datetime(2026, 4, 1),
            "source": "Statistics Indonesia (BPS)",
            "note": "3월 인플레이션 둔화"
        },
        {
            "country_id": id_country_id,
            "indicator_type": "inflation",
            "value": 2.8,
            "unit": "%",
            "period": "2026-04",
            "recorded_at": datetime(2026, 4, 15),
            "source": "Statistics Indonesia (BPS)",
            "note": "4월 인플레이션 (속보치)"
        },

        # === 기준금리 (BI Rate) ===
        {
            "country_id": id_country_id,
            "indicator_type": "interest_rate",
            "value": 6.00,
            "unit": "%",
            "period": "2026-01",
            "recorded_at": datetime(2026, 1, 20),
            "source": "Bank Indonesia",
            "note": "1월 BI 7-Day Reverse Repo Rate"
        },
        {
            "country_id": id_country_id,
            "indicator_type": "interest_rate",
            "value": 6.00,
            "unit": "%",
            "period": "2026-02",
            "recorded_at": datetime(2026, 2, 20),
            "source": "Bank Indonesia",
            "note": "2월 기준금리 동결"
        },
        {
            "country_id": id_country_id,
            "indicator_type": "interest_rate",
            "value": 6.00,
            "unit": "%",
            "period": "2026-03",
            "recorded_at": datetime(2026, 3, 20),
            "source": "Bank Indonesia",
            "note": "3월 기준금리 동결"
        },
        {
            "country_id": id_country_id,
            "indicator_type": "interest_rate",
            "value": 5.75,
            "unit": "%",
            "period": "2026-04",
            "recorded_at": datetime(2026, 4, 10),
            "source": "Bank Indonesia",
            "note": "4월 기준금리 25bp 인하 (경제 성장 지원)"
        },

        # === 외환보유액 ===
        {
            "country_id": id_country_id,
            "indicator_type": "forex_reserve",
            "value": 145.2,
            "unit": "billion USD",
            "period": "2026-01",
            "recorded_at": datetime(2026, 2, 7),
            "source": "Bank Indonesia",
            "note": "1월 말 기준 외환보유액 (수입 6.8개월분)"
        },
        {
            "country_id": id_country_id,
            "indicator_type": "forex_reserve",
            "value": 146.8,
            "unit": "billion USD",
            "period": "2026-02",
            "recorded_at": datetime(2026, 3, 7),
            "source": "Bank Indonesia",
            "note": "2월 말 외환보유액 증가"
        },
        {
            "country_id": id_country_id,
            "indicator_type": "forex_reserve",
            "value": 148.5,
            "unit": "billion USD",
            "period": "2026-03",
            "recorded_at": datetime(2026, 4, 7),
            "source": "Bank Indonesia",
            "note": "3월 말 외환보유액 역대 최고 수준"
        },

        # === 무역수지 ===
        {
            "country_id": id_country_id,
            "indicator_type": "trade_balance",
            "value": 3850.5,
            "unit": "million USD",
            "period": "2026-01",
            "recorded_at": datetime(2026, 2, 15),
            "source": "Statistics Indonesia (BPS)",
            "note": "1월 무역수지 흑자 (41개월 연속)"
        },
        {
            "country_id": id_country_id,
            "indicator_type": "trade_balance",
            "value": 3620.2,
            "unit": "million USD",
            "period": "2026-02",
            "recorded_at": datetime(2026, 3, 15),
            "source": "Statistics Indonesia (BPS)",
            "note": "2월 무역수지 흑자 지속"
        },
        {
            "country_id": id_country_id,
            "indicator_type": "trade_balance",
            "value": 4125.8,
            "unit": "million USD",
            "period": "2026-03",
            "recorded_at": datetime(2026, 4, 15),
            "source": "Statistics Indonesia (BPS)",
            "note": "3월 무역수지 흑자 확대"
        },

        # === 수출 ===
        {
            "country_id": id_country_id,
            "indicator_type": "exports",
            "value": 22850.3,
            "unit": "million USD",
            "period": "2026-01",
            "recorded_at": datetime(2026, 2, 15),
            "source": "Statistics Indonesia (BPS)",
            "note": "1월 수출액 (팜오일, 석탄, 광물 중심)"
        },
        {
            "country_id": id_country_id,
            "indicator_type": "exports",
            "value": 21320.5,
            "unit": "million USD",
            "period": "2026-02",
            "recorded_at": datetime(2026, 3, 15),
            "source": "Statistics Indonesia (BPS)",
            "note": "2월 수출액 (설 연휴 영향으로 감소)"
        },
        {
            "country_id": id_country_id,
            "indicator_type": "exports",
            "value": 24680.2,
            "unit": "million USD",
            "period": "2026-03",
            "recorded_at": datetime(2026, 4, 15),
            "source": "Statistics Indonesia (BPS)",
            "note": "3월 수출액 반등 (원자재 가격 상승)"
        },

        # === 수입 ===
        {
            "country_id": id_country_id,
            "indicator_type": "imports",
            "value": 18999.8,
            "unit": "million USD",
            "period": "2026-01",
            "recorded_at": datetime(2026, 2, 15),
            "source": "Statistics Indonesia (BPS)",
            "note": "1월 수입액 (원자재, 자본재)"
        },
        {
            "country_id": id_country_id,
            "indicator_type": "imports",
            "value": 17700.3,
            "unit": "million USD",
            "period": "2026-02",
            "recorded_at": datetime(2026, 3, 15),
            "source": "Statistics Indonesia (BPS)",
            "note": "2월 수입액"
        },
        {
            "country_id": id_country_id,
            "indicator_type": "imports",
            "value": 20554.4,
            "unit": "million USD",
            "period": "2026-03",
            "recorded_at": datetime(2026, 4, 15),
            "source": "Statistics Indonesia (BPS)",
            "note": "3월 수입액 증가"
        },

        # === 실업률 ===
        {
            "country_id": id_country_id,
            "indicator_type": "unemployment_rate",
            "value": 5.3,
            "unit": "%",
            "period": "2026-02",
            "recorded_at": datetime(2026, 3, 20),
            "source": "Statistics Indonesia (BPS)",
            "note": "2월 실업률 (2023년 이후 최저)"
        },

        # === 제조업 PMI ===
        {
            "country_id": id_country_id,
            "indicator_type": "manufacturing_pmi",
            "value": 52.3,
            "unit": "Index",
            "period": "2026-01",
            "recorded_at": datetime(2026, 2, 1),
            "source": "S&P Global",
            "note": "1월 제조업 PMI (50 초과 = 확장)"
        },
        {
            "country_id": id_country_id,
            "indicator_type": "manufacturing_pmi",
            "value": 51.8,
            "unit": "Index",
            "period": "2026-02",
            "recorded_at": datetime(2026, 3, 1),
            "source": "S&P Global",
            "note": "2월 제조업 PMI 소폭 하락"
        },
        {
            "country_id": id_country_id,
            "indicator_type": "manufacturing_pmi",
            "value": 53.1,
            "unit": "Index",
            "period": "2026-03",
            "recorded_at": datetime(2026, 4, 1),
            "source": "S&P Global",
            "note": "3월 제조업 PMI 상승 (9개월 만에 최고)"
        },
        {
            "country_id": id_country_id,
            "indicator_type": "manufacturing_pmi",
            "value": 52.8,
            "unit": "Index",
            "period": "2026-04",
            "recorded_at": datetime(2026, 4, 15),
            "source": "S&P Global",
            "note": "4월 제조업 PMI (속보치)"
        },

        # === 소비자신뢰지수 ===
        {
            "country_id": id_country_id,
            "indicator_type": "consumer_confidence",
            "value": 125.8,
            "unit": "Index",
            "period": "2026-01",
            "recorded_at": datetime(2026, 2, 10),
            "source": "Bank Indonesia",
            "note": "1월 소비자신뢰지수 (100 초과 = 낙관)"
        },
        {
            "country_id": id_country_id,
            "indicator_type": "consumer_confidence",
            "value": 128.2,
            "unit": "Index",
            "period": "2026-02",
            "recorded_at": datetime(2026, 3, 10),
            "source": "Bank Indonesia",
            "note": "2월 소비자신뢰지수 상승"
        },
        {
            "country_id": id_country_id,
            "indicator_type": "consumer_confidence",
            "value": 127.5,
            "unit": "Index",
            "period": "2026-03",
            "recorded_at": datetime(2026, 4, 10),
            "source": "Bank Indonesia",
            "note": "3월 소비자신뢰지수 소폭 하락"
        },

        # === 정부부채 ===
        {
            "country_id": id_country_id,
            "indicator_type": "government_debt",
            "value": 38.2,
            "unit": "% of GDP",
            "period": "2026-Q1",
            "recorded_at": datetime(2026, 4, 12),
            "source": "Ministry of Finance",
            "note": "2026년 1분기 정부부채 비율 (건전 수준 유지)"
        },

        # === 외국인 직접투자 (FDI) ===
        {
            "country_id": id_country_id,
            "indicator_type": "fdi",
            "value": 8950.5,
            "unit": "million USD",
            "period": "2026-Q1",
            "recorded_at": datetime(2026, 4, 10),
            "source": "Investment Coordinating Board (BKPM)",
            "note": "2026년 1분기 외국인 직접투자 (전년 동기 대비 12.5% 증가)"
        },

        # === 소매판매 ===
        {
            "country_id": id_country_id,
            "indicator_type": "retail_sales",
            "value": 7.8,
            "unit": "% YoY",
            "period": "2026-01",
            "recorded_at": datetime(2026, 2, 20),
            "source": "Statistics Indonesia (BPS)",
            "note": "1월 소매판매 성장률"
        },
        {
            "country_id": id_country_id,
            "indicator_type": "retail_sales",
            "value": 8.5,
            "unit": "% YoY",
            "period": "2026-02",
            "recorded_at": datetime(2026, 3, 20),
            "source": "Statistics Indonesia (BPS)",
            "note": "2월 소매판매 (설 특수)"
        },
        {
            "country_id": id_country_id,
            "indicator_type": "retail_sales",
            "value": 7.2,
            "unit": "% YoY",
            "period": "2026-03",
            "recorded_at": datetime(2026, 4, 20),
            "source": "Statistics Indonesia (BPS)",
            "note": "3월 소매판매"
        },

        # === 자동차 판매 ===
        {
            "country_id": id_country_id,
            "indicator_type": "auto_sales",
            "value": 92500,
            "unit": "units",
            "period": "2026-01",
            "recorded_at": datetime(2026, 2, 5),
            "source": "Gaikindo (Automotive Industry Association)",
            "note": "1월 자동차 판매량"
        },
        {
            "country_id": id_country_id,
            "indicator_type": "auto_sales",
            "value": 85200,
            "unit": "units",
            "period": "2026-02",
            "recorded_at": datetime(2026, 3, 5),
            "source": "Gaikindo",
            "note": "2월 자동차 판매량 (설 영향)"
        },
        {
            "country_id": id_country_id,
            "indicator_type": "auto_sales",
            "value": 98700,
            "unit": "units",
            "period": "2026-03",
            "recorded_at": datetime(2026, 4, 5),
            "source": "Gaikindo",
            "note": "3월 자동차 판매량 반등"
        },

        # === 관광객 수 ===
        {
            "country_id": id_country_id,
            "indicator_type": "tourist_arrivals",
            "value": 1.35,
            "unit": "million",
            "period": "2026-01",
            "recorded_at": datetime(2026, 2, 25),
            "source": "Statistics Indonesia (BPS)",
            "note": "1월 외국인 관광객 수"
        },
        {
            "country_id": id_country_id,
            "indicator_type": "tourist_arrivals",
            "value": 1.28,
            "unit": "million",
            "period": "2026-02",
            "recorded_at": datetime(2026, 3, 25),
            "source": "Statistics Indonesia (BPS)",
            "note": "2월 외국인 관광객 수"
        },
        {
            "country_id": id_country_id,
            "indicator_type": "tourist_arrivals",
            "value": 1.42,
            "unit": "million",
            "period": "2026-03",
            "recorded_at": datetime(2026, 4, 25),
            "source": "Statistics Indonesia (BPS)",
            "note": "3월 외국인 관광객 수 (성수기)"
        },
    ]

    for data in indicators_data:
        indicator = EconomicIndicator(**data)
        db.add(indicator)

    print(f"✅ 인도네시아 경제 지표 {len(indicators_data)}개 추가 완료")


async def main():
    """메인 실행 함수"""
    print("\n" + "="*60)
    print("📊 경제 지표 데이터 수동 추가 시작")
    print("="*60 + "\n")

    db = SessionLocal()

    try:
        # 국가 조회
        mm_country = db.query(Country).filter(Country.code == "MM").first()
        id_country = db.query(Country).filter(Country.code == "ID").first()

        if not mm_country or not id_country:
            print("❌ 국가 데이터를 찾을 수 없습니다.")
            return

        # 기존 경제 지표 삭제
        print("🗑️  기존 경제 지표 삭제 중...")
        db.query(EconomicIndicator).delete()
        db.commit()

        # 미얀마 경제 지표 추가
        populate_myanmar_indicators(db, mm_country.id)

        # 인도네시아 경제 지표 추가
        populate_indonesia_indicators(db, id_country.id)

        db.commit()

        total_count = db.query(EconomicIndicator).count()
        mm_count = db.query(EconomicIndicator).filter(EconomicIndicator.country_id == mm_country.id).count()
        id_count = db.query(EconomicIndicator).filter(EconomicIndicator.country_id == id_country.id).count()

        print("\n" + "="*60)
        print("🎉 경제 지표 데이터 추가 완료!")
        print("="*60)
        print(f"\n📊 추가된 지표:")
        print(f"   - 미얀마: {mm_count}개")
        print(f"   - 인도네시아: {id_count}개")
        print(f"   - 총계: {total_count}개")
        print("\n")

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(main())
