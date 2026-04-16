"""
초기 경제 지표 데이터 로드 (2026년)
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from core.database import SessionLocal
from models.country import Country
from models.indicator import EconomicIndicator


# 미얀마 경제 지표 (2026년)
MYANMAR_INDICATORS_2026 = [
    # 환율 (USD/MMK)
    {"type": "exchange_rate", "value": 2100.0, "unit": "MMK/USD", "period": "2026-01", "date": "2026-01-15", "source": "Central Bank of Myanmar"},
    {"type": "exchange_rate", "value": 2095.0, "unit": "MMK/USD", "period": "2026-02", "date": "2026-02-15", "source": "Central Bank of Myanmar"},
    {"type": "exchange_rate", "value": 2080.0, "unit": "MMK/USD", "period": "2026-03", "date": "2026-03-15", "source": "Central Bank of Myanmar"},
    {"type": "exchange_rate", "value": 2070.0, "unit": "MMK/USD", "period": "2026-04", "date": "2026-04-15", "source": "Central Bank of Myanmar"},

    # GDP 성장률
    {"type": "gdp_growth", "value": 4.2, "unit": "%", "period": "2026-Q1", "date": "2026-03-31", "source": "IMF"},

    # 인플레이션율
    {"type": "inflation", "value": 6.5, "unit": "%", "period": "2026-01", "date": "2026-01-31", "source": "Central Statistical Organization"},
    {"type": "inflation", "value": 6.3, "unit": "%", "period": "2026-02", "date": "2026-02-28", "source": "Central Statistical Organization"},
    {"type": "inflation", "value": 6.1, "unit": "%", "period": "2026-03", "date": "2026-03-31", "source": "Central Statistical Organization"},

    # 기준금리
    {"type": "interest_rate", "value": 9.0, "unit": "%", "period": "2026-Q1", "date": "2026-03-10", "source": "Central Bank of Myanmar", "note": "기준금리 0.5%p 인하"},

    # 외환보유고
    {"type": "forex_reserve", "value": 10.2, "unit": "billion USD", "period": "2026-01", "date": "2026-01-31", "source": "Central Bank of Myanmar"},
]

# 인도네시아 경제 지표 (2026년)
INDONESIA_INDICATORS_2026 = [
    # 환율 (USD/IDR)
    {"type": "exchange_rate", "value": 15200.0, "unit": "IDR/USD", "period": "2026-01", "date": "2026-01-15", "source": "Bank Indonesia"},
    {"type": "exchange_rate", "value": 15180.0, "unit": "IDR/USD", "period": "2026-02", "date": "2026-02-15", "source": "Bank Indonesia"},
    {"type": "exchange_rate", "value": 15150.0, "unit": "IDR/USD", "period": "2026-03", "date": "2026-03-15", "source": "Bank Indonesia"},
    {"type": "exchange_rate", "value": 15120.0, "unit": "IDR/USD", "period": "2026-04", "date": "2026-04-15", "source": "Bank Indonesia"},

    # GDP 성장률
    {"type": "gdp_growth", "value": 5.1, "unit": "%", "period": "2026-Q1", "date": "2026-03-31", "source": "BPS Statistics Indonesia"},

    # 인플레이션율
    {"type": "inflation", "value": 2.8, "unit": "%", "period": "2026-01", "date": "2026-01-31", "source": "BPS Statistics Indonesia"},
    {"type": "inflation", "value": 2.7, "unit": "%", "period": "2026-02", "date": "2026-02-28", "source": "BPS Statistics Indonesia"},
    {"type": "inflation", "value": 2.9, "unit": "%", "period": "2026-03", "date": "2026-03-31", "source": "BPS Statistics Indonesia"},

    # 기준금리
    {"type": "interest_rate", "value": 6.0, "unit": "%", "period": "2026-Q1", "date": "2026-04-05", "source": "Bank Indonesia", "note": "기준금리 동결"},

    # 외환보유고
    {"type": "forex_reserve", "value": 145.8, "unit": "billion USD", "period": "2026-03", "date": "2026-03-31", "source": "Bank Indonesia"},
]


def load_indicators():
    """경제 지표 데이터 로드"""
    db = SessionLocal()

    try:
        # 국가 조회
        myanmar = db.query(Country).filter(Country.code == "MM").first()
        indonesia = db.query(Country).filter(Country.code == "ID").first()

        if not myanmar or not indonesia:
            print("❌ 국가 데이터가 없습니다. 먼저 init_db.py를 실행하세요.")
            return

        print("📊 경제 지표 데이터 로딩 시작...\n")

        # 미얀마 지표
        mm_count = 0
        for ind_data in MYANMAR_INDICATORS_2026:
            existing = db.query(EconomicIndicator).filter(
                EconomicIndicator.country_id == myanmar.id,
                EconomicIndicator.indicator_type == ind_data["type"],
                EconomicIndicator.period == ind_data["period"]
            ).first()

            if not existing:
                indicator = EconomicIndicator(
                    country_id=myanmar.id,
                    indicator_type=ind_data["type"],
                    value=ind_data["value"],
                    unit=ind_data["unit"],
                    period=ind_data["period"],
                    recorded_at=datetime.strptime(ind_data["date"], "%Y-%m-%d"),
                    source=ind_data["source"],
                    note=ind_data.get("note")
                )
                db.add(indicator)
                mm_count += 1

        # 인도네시아 지표
        id_count = 0
        for ind_data in INDONESIA_INDICATORS_2026:
            existing = db.query(EconomicIndicator).filter(
                EconomicIndicator.country_id == indonesia.id,
                EconomicIndicator.indicator_type == ind_data["type"],
                EconomicIndicator.period == ind_data["period"]
            ).first()

            if not existing:
                indicator = EconomicIndicator(
                    country_id=indonesia.id,
                    indicator_type=ind_data["type"],
                    value=ind_data["value"],
                    unit=ind_data["unit"],
                    period=ind_data["period"],
                    recorded_at=datetime.strptime(ind_data["date"], "%Y-%m-%d"),
                    source=ind_data["source"],
                    note=ind_data.get("note")
                )
                db.add(indicator)
                id_count += 1

        db.commit()
        print(f"✅ 미얀마 경제 지표 {mm_count}개 추가")
        print(f"✅ 인도네시아 경제 지표 {id_count}개 추가")
        print(f"\n🎉 경제 지표 데이터 로딩 완료! (총 {mm_count + id_count}개)")

    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    load_indicators()
