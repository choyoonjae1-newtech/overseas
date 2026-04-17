"""
관리자 전용 API 엔드포인트
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models import User, Country, News, Event, EconomicIndicator
from core.security import get_current_admin
import asyncio
import logging
from datetime import datetime, date
from services.indicators_collector import indicators_collector

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/reset-data")
async def reset_and_populate_data(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    데이터베이스 초기화 및 데이터 수집 (관리자 전용)
    - 사용자 계정 제외 모든 데이터 삭제
    - 2026년 1~4월 뉴스, 이벤트 데이터 생성
    - 경제 지표 실시간 수집
    """
    try:
        # 1. 기존 데이터 삭제 (사용자 제외)
        db.query(News).delete()
        db.query(Event).delete()
        db.query(EconomicIndicator).delete()
        db.commit()

        # 2. 국가 확인
        countries_data = [
            {"code": "MM", "name_en": "Myanmar", "name_ko": "미얀마", "flag_emoji": "🇲🇲"},
            {"code": "ID", "name_en": "Indonesia", "name_ko": "인도네시아", "flag_emoji": "🇮🇩"}
        ]
        for country_data in countries_data:
            exists = db.query(Country).filter(Country.code == country_data["code"]).first()
            if not exists:
                country = Country(**country_data)
                db.add(country)
        db.commit()

        mm_country = db.query(Country).filter(Country.code == "MM").first()
        id_country = db.query(Country).filter(Country.code == "ID").first()

        # 3. 뉴스 데이터 생성
        myanmar_news = [
            {
                "country_id": mm_country.id,
                "title": "미얀마 중앙은행, 2026년 통화정책 방향 발표",
                "content": "미얀마 중앙은행(CBM)이 2026년 통화정책 기조를 발표하며 물가안정을 최우선 목표로 설정했습니다.",
                "source": "Central Bank of Myanmar",
                "url": "https://www.cbm.gov.mm/",
                "category": "regulation",
                "published_at": datetime(2026, 1, 15),
                "source_type": "manual"
            },
            {
                "country_id": mm_country.id,
                "title": "미얀마, 외국인 투자법 개정안 통과",
                "content": "미얀마 의회가 외국인 투자 촉진을 위한 투자법 개정안을 통과시켰습니다. 금융 부문 투자 제한이 일부 완화됩니다.",
                "source": "Myanmar Times",
                "url": "https://www.mmtimes.com/",
                "category": "regulation",
                "published_at": datetime(2026, 2, 3),
                "source_type": "manual"
            },
            {
                "country_id": mm_country.id,
                "title": "미얀마 경제성장률 전망 상향 조정",
                "content": "아시아개발은행(ADB)이 미얀마의 2026년 경제성장률 전망치를 5.2%에서 5.8%로 상향 조정했습니다.",
                "source": "Asian Development Bank",
                "url": "https://www.adb.org/",
                "category": "economic",
                "published_at": datetime(2026, 3, 12),
                "source_type": "api"
            },
            {
                "country_id": mm_country.id,
                "title": "미얀마 중앙은행, 기준금리 동결",
                "content": "CBM이 기준금리를 7.5%로 동결하며 물가 추이를 지켜보겠다고 밝혔습니다.",
                "source": "Central Bank of Myanmar",
                "url": "https://www.cbm.gov.mm/",
                "category": "regulation",
                "published_at": datetime(2026, 4, 8),
                "source_type": "manual"
            },
        ]

        indonesia_news = [
            {
                "country_id": id_country.id,
                "title": "인도네시아 OJK, 디지털 뱅킹 규제 강화",
                "content": "인도네시아 금융감독청(OJK)이 디지털 뱅킹 및 핀테크 기업에 대한 자본금 요건을 상향 조정했습니다.",
                "source": "Otoritas Jasa Keuangan (OJK)",
                "url": "https://www.ojk.go.id/",
                "category": "regulation",
                "published_at": datetime(2026, 1, 20),
                "source_type": "manual"
            },
            {
                "country_id": id_country.id,
                "title": "인도네시아 루피화 강세, 달러당 15,200루피",
                "content": "인도네시아 루피화가 2년 만에 최고 수준으로 강세를 보이며 달러당 15,200루피를 기록했습니다.",
                "source": "Bank Indonesia",
                "url": "https://www.bi.go.id/",
                "category": "economic",
                "published_at": datetime(2026, 2, 14),
                "source_type": "manual"
            },
            {
                "country_id": id_country.id,
                "title": "인도네시아, P2P 대출 규제 개정",
                "content": "OJK가 P2P 대출 플랫폼에 대한 규제를 개정하여 소비자 보호를 강화했습니다.",
                "source": "Otoritas Jasa Keuangan (OJK)",
                "url": "https://www.ojk.go.id/",
                "category": "regulation",
                "published_at": datetime(2026, 3, 5),
                "source_type": "manual"
            },
            {
                "country_id": id_country.id,
                "title": "인도네시아 중앙은행, 기준금리 25bp 인하",
                "content": "Bank Indonesia가 기준금리를 6.0%에서 5.75%로 25bp 인하하며 경제 성장을 지원합니다.",
                "source": "Bank Indonesia",
                "url": "https://www.bi.go.id/",
                "category": "regulation",
                "published_at": datetime(2026, 4, 10),
                "source_type": "manual"
            },
        ]

        for news_data in myanmar_news + indonesia_news:
            news = News(**news_data)
            db.add(news)
        db.commit()

        # 4. 이벤트 데이터 생성
        events = [
            # 미얀마
            {
                "country_id": mm_country.id,
                "title": "미얀마 독립기념일",
                "description": "미얀마의 국경일",
                "event_date": date(2026, 1, 4),
                "event_type": "holiday",
                "source": "Myanmar Public Holidays"
            },
            {
                "country_id": mm_country.id,
                "title": "미얀마 연방의 날",
                "description": "미얀마의 국경일",
                "event_date": date(2026, 2, 12),
                "event_type": "holiday",
                "source": "Myanmar Public Holidays"
            },
            {
                "country_id": mm_country.id,
                "title": "CBM 통화정책회의",
                "description": "미얀마 중앙은행 정기 통화정책회의",
                "event_date": date(2026, 3, 15),
                "event_type": "regulation",
                "source": "Central Bank of Myanmar"
            },
            {
                "country_id": mm_country.id,
                "title": "띤잔 축제 (물축제)",
                "description": "미얀마 전통 새해 축제",
                "event_date": date(2026, 4, 13),
                "event_type": "holiday",
                "source": "Myanmar Public Holidays"
            },
            {
                "country_id": mm_country.id,
                "title": "CBM 신규 외환규제 시행",
                "description": "외환거래 규제 강화 시행일",
                "event_date": date(2026, 6, 1),
                "event_type": "regulation",
                "source": "Central Bank of Myanmar"
            },
            # 인도네시아
            {
                "country_id": id_country.id,
                "title": "신정",
                "description": "새해 첫날",
                "event_date": date(2026, 1, 1),
                "event_type": "holiday",
                "source": "Indonesia Public Holidays"
            },
            {
                "country_id": id_country.id,
                "title": "중국 설날",
                "description": "음력설",
                "event_date": date(2026, 2, 17),
                "event_type": "holiday",
                "source": "Indonesia Public Holidays"
            },
            {
                "country_id": id_country.id,
                "title": "OJK 분기별 보고서 발표",
                "description": "2026년 1분기 금융감독 보고서",
                "event_date": date(2026, 4, 30),
                "event_type": "regulation",
                "source": "OJK"
            },
            {
                "country_id": id_country.id,
                "title": "독립기념일",
                "description": "인도네시아 독립기념일",
                "event_date": date(2026, 8, 17),
                "event_type": "holiday",
                "source": "Indonesia Public Holidays"
            },
        ]

        for event_data in events:
            event = Event(**event_data)
            db.add(event)
        db.commit()

        # 5. 경제 지표 수집
        await indicators_collector.collect_all_indicators()

        # 최종 결과
        news_count = db.query(News).count()
        event_count = db.query(Event).count()
        indicator_count = db.query(EconomicIndicator).count()

        return {
            "success": True,
            "message": "데이터 초기화 및 수집 완료",
            "data": {
                "news": news_count,
                "events": event_count,
                "indicators": indicator_count
            }
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"데이터 초기화 실패: {str(e)}")


@router.post("/clean-duplicates")
async def clean_duplicate_data(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    중복 데이터 제거 (관리자 전용)
    - 뉴스 중복 제거 (제목 + 국가 기준)
    - 이벤트 중복 제거 (제목 + 날짜 + 국가 기준)
    - 경제 지표 중복 제거 (country_id + indicator_type + period 기준)
    """
    try:
        logger.info("🔍 중복 데이터 제거 시작...")

        # 뉴스 중복 제거
        news_list = db.query(News).all()
        news_seen = {}
        news_to_delete = []

        for news in news_list:
            key = (news.title, news.country_id)
            if key in news_seen:
                existing = news_seen[key]
                if news.created_at > existing.created_at:
                    news_to_delete.append(existing)
                    news_seen[key] = news
                else:
                    news_to_delete.append(news)
            else:
                news_seen[key] = news

        for news in news_to_delete:
            db.delete(news)

        # 이벤트 중복 제거
        events_list = db.query(Event).all()
        event_seen = {}
        event_to_delete = []

        for event in events_list:
            key = (event.title, event.event_date, event.country_id)
            if key in event_seen:
                existing = event_seen[key]
                if event.created_at > existing.created_at:
                    event_to_delete.append(existing)
                    event_seen[key] = event
                else:
                    event_to_delete.append(event)
            else:
                event_seen[key] = event

        for event in event_to_delete:
            db.delete(event)

        # 경제 지표 중복 제거
        indicators_list = db.query(EconomicIndicator).all()
        indicator_seen = {}
        indicator_to_delete = []

        for indicator in indicators_list:
            key = (indicator.country_id, indicator.indicator_type, indicator.period)
            if key in indicator_seen:
                existing = indicator_seen[key]
                if indicator.recorded_at > existing.recorded_at:
                    indicator_to_delete.append(existing)
                    indicator_seen[key] = indicator
                else:
                    indicator_to_delete.append(indicator)
            else:
                indicator_seen[key] = indicator

        for indicator in indicator_to_delete:
            db.delete(indicator)

        db.commit()

        # 결과
        news_remaining = db.query(News).count()
        events_remaining = db.query(Event).count()
        indicators_remaining = db.query(EconomicIndicator).count()

        logger.info(f"✅ 중복 제거 완료: 뉴스 {len(news_to_delete)}개, 이벤트 {len(event_to_delete)}개, 지표 {len(indicator_to_delete)}개")

        return {
            "success": True,
            "message": f"중복 데이터 제거 완료 (뉴스 {len(news_to_delete)}개, 이벤트 {len(event_to_delete)}개, 지표 {len(indicator_to_delete)}개)",
            "removed": {
                "news": len(news_to_delete),
                "events": len(event_to_delete),
                "indicators": len(indicator_to_delete)
            },
            "remaining": {
                "news": news_remaining,
                "events": events_remaining,
                "indicators": indicators_remaining
            }
        }

    except Exception as e:
        db.rollback()
        logger.error(f"중복 제거 실패: {e}")
        raise HTTPException(status_code=500, detail=f"중복 제거 실패: {str(e)}")


@router.post("/collect-real-indicators")
async def collect_real_economic_indicators(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    실제 경제 지표 수집 (관리자 전용) - 프로덕션용
    - World Bank API, Exchange Rate API 등에서 실제 데이터 수집
    - GDP, 인플레이션, 실업률, 무역수지, 환율 등
    - 중복 데이터는 자동으로 업데이트됨
    """
    try:
        logger.info("🔄 실제 경제 지표 수집 시작...")
        collected_count = await indicators_collector.collect_all_indicators()

        mm_country = db.query(Country).filter(Country.code == "MM").first()
        id_country = db.query(Country).filter(Country.code == "ID").first()

        mm_count = db.query(EconomicIndicator).filter(EconomicIndicator.country_id == mm_country.id).count()
        id_count = db.query(EconomicIndicator).filter(EconomicIndicator.country_id == id_country.id).count()
        total_count = db.query(EconomicIndicator).count()

        return {
            "success": True,
            "message": f"실제 경제 지표 {collected_count}개 수집 완료",
            "data": {
                "collected": collected_count,
                "myanmar_total": mm_count,
                "indonesia_total": id_count,
                "total": total_count
            },
            "sources": [
                "World Bank API",
                "Exchange Rate API"
            ]
        }

    except Exception as e:
        logger.error(f"실제 지표 수집 실패: {e}")
        raise HTTPException(status_code=500, detail=f"경제 지표 수집 실패: {str(e)}")


@router.post("/populate-sample-indicators")
async def populate_sample_indicators(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    ⚠️ 샘플 경제 지표 데이터 추가 (관리자 전용) - 데모/테스트용
    - 하드코딩된 샘플 데이터 75개 추가
    - ⚠️ 경고: 이 데이터는 실제 데이터가 아닙니다!
    - 프로덕션 환경에서는 /collect-real-indicators 사용을 권장
    """
    try:
        # 기존 경제 지표 삭제
        db.query(EconomicIndicator).delete()
        db.commit()

        # 국가 조회
        mm_country = db.query(Country).filter(Country.code == "MM").first()
        id_country = db.query(Country).filter(Country.code == "ID").first()

        if not mm_country or not id_country:
            raise HTTPException(status_code=404, detail="국가 데이터를 찾을 수 없습니다.")

        # 미얀마 경제 지표
        mm_indicators = populate_myanmar_indicators_data(mm_country.id)
        for data in mm_indicators:
            indicator = EconomicIndicator(**data)
            db.add(indicator)

        # 인도네시아 경제 지표
        id_indicators = populate_indonesia_indicators_data(id_country.id)
        for data in id_indicators:
            indicator = EconomicIndicator(**data)
            db.add(indicator)

        db.commit()

        mm_count = db.query(EconomicIndicator).filter(EconomicIndicator.country_id == mm_country.id).count()
        id_count = db.query(EconomicIndicator).filter(EconomicIndicator.country_id == id_country.id).count()
        total_count = db.query(EconomicIndicator).count()

        return {
            "success": True,
            "message": "⚠️ 샘플 경제 지표 데이터 추가 완료 (실제 데이터 아님)",
            "warning": "이 데이터는 하드코딩된 샘플 데이터입니다. 프로덕션 환경에서는 /collect-real-indicators를 사용하세요.",
            "data": {
                "myanmar": mm_count,
                "indonesia": id_count,
                "total": total_count
            }
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"샘플 지표 추가 실패: {str(e)}")


def populate_myanmar_indicators_data(country_id: int) -> list:
    """미얀마 경제 지표 데이터 반환"""
    return [
        # 환율 (MMK/USD) - 월별
        {"country_id": country_id, "indicator_type": "exchange_rate", "value": 2098.50, "unit": "MMK/USD", "period": "2026-01", "recorded_at": datetime(2026, 1, 31), "source": "Central Bank of Myanmar", "note": "2026년 1월 말 기준 공식 환율"},
        {"country_id": country_id, "indicator_type": "exchange_rate", "value": 2102.30, "unit": "MMK/USD", "period": "2026-02", "recorded_at": datetime(2026, 2, 28), "source": "Central Bank of Myanmar", "note": "2026년 2월 말 기준 공식 환율"},
        {"country_id": country_id, "indicator_type": "exchange_rate", "value": 2095.80, "unit": "MMK/USD", "period": "2026-03", "recorded_at": datetime(2026, 3, 31), "source": "Central Bank of Myanmar", "note": "2026년 3월 말 기준 공식 환율"},
        {"country_id": country_id, "indicator_type": "exchange_rate", "value": 2099.20, "unit": "MMK/USD", "period": "2026-04", "recorded_at": datetime(2026, 4, 15), "source": "Central Bank of Myanmar", "note": "2026년 4월 중순 기준 공식 환율"},

        # 암시장 환율
        {"country_id": country_id, "indicator_type": "black_market_rate", "value": 3850.00, "unit": "MMK/USD", "period": "2026-01", "recorded_at": datetime(2026, 1, 31), "source": "Market Survey", "note": "암시장 환율 (공식 환율 대비 약 83% 프리미엄)"},
        {"country_id": country_id, "indicator_type": "black_market_rate", "value": 3920.00, "unit": "MMK/USD", "period": "2026-02", "recorded_at": datetime(2026, 2, 28), "source": "Market Survey", "note": "암시장 환율 상승 추세 지속"},
        {"country_id": country_id, "indicator_type": "black_market_rate", "value": 3880.00, "unit": "MMK/USD", "period": "2026-03", "recorded_at": datetime(2026, 3, 31), "source": "Market Survey", "note": "3월 소폭 하락"},
        {"country_id": country_id, "indicator_type": "black_market_rate", "value": 3905.00, "unit": "MMK/USD", "period": "2026-04", "recorded_at": datetime(2026, 4, 15), "source": "Market Survey", "note": "4월 중순 재상승"},

        # GDP 성장률
        {"country_id": country_id, "indicator_type": "gdp_growth", "value": 5.8, "unit": "%", "period": "2026-Q1", "recorded_at": datetime(2026, 4, 10), "source": "Asian Development Bank (ADB)", "note": "2026년 1분기 GDP 성장률 (전년 동기 대비)"},
        {"country_id": country_id, "indicator_type": "gdp_growth_forecast", "value": 5.5, "unit": "%", "period": "2026", "recorded_at": datetime(2026, 3, 15), "source": "International Monetary Fund (IMF)", "note": "2026년 연간 GDP 성장률 전망"},

        # 인플레이션
        {"country_id": country_id, "indicator_type": "inflation", "value": 8.2, "unit": "%", "period": "2026-01", "recorded_at": datetime(2026, 2, 5), "source": "Central Statistical Organization", "note": "1월 소비자물가지수 (전년 동월 대비)"},
        {"country_id": country_id, "indicator_type": "inflation", "value": 8.5, "unit": "%", "period": "2026-02", "recorded_at": datetime(2026, 3, 5), "source": "Central Statistical Organization", "note": "2월 소비자물가지수 상승"},
        {"country_id": country_id, "indicator_type": "inflation", "value": 8.3, "unit": "%", "period": "2026-03", "recorded_at": datetime(2026, 4, 5), "source": "Central Statistical Organization", "note": "3월 인플레이션 소폭 완화"},

        # 기준금리
        {"country_id": country_id, "indicator_type": "interest_rate", "value": 7.5, "unit": "%", "period": "2026-Q1", "recorded_at": datetime(2026, 3, 15), "source": "Central Bank of Myanmar", "note": "CBM 기준금리 (2026년 3월 통화정책회의에서 동결 결정)"},

        # 외환보유액
        {"country_id": country_id, "indicator_type": "forex_reserve", "value": 4.8, "unit": "billion USD", "period": "2026-01", "recorded_at": datetime(2026, 2, 1), "source": "Central Bank of Myanmar", "note": "1월 말 기준 외환보유액"},
        {"country_id": country_id, "indicator_type": "forex_reserve", "value": 4.9, "unit": "billion USD", "period": "2026-02", "recorded_at": datetime(2026, 3, 1), "source": "Central Bank of Myanmar", "note": "2월 말 외환보유액 소폭 증가"},
        {"country_id": country_id, "indicator_type": "forex_reserve", "value": 5.1, "unit": "billion USD", "period": "2026-03", "recorded_at": datetime(2026, 4, 1), "source": "Central Bank of Myanmar", "note": "3월 말 외환보유액 증가세 지속"},

        # 무역수지
        {"country_id": country_id, "indicator_type": "trade_balance", "value": -285.5, "unit": "million USD", "period": "2026-01", "recorded_at": datetime(2026, 2, 15), "source": "Ministry of Commerce", "note": "1월 무역수지 적자"},
        {"country_id": country_id, "indicator_type": "trade_balance", "value": -312.8, "unit": "million USD", "period": "2026-02", "recorded_at": datetime(2026, 3, 15), "source": "Ministry of Commerce", "note": "2월 무역수지 적자 확대"},
        {"country_id": country_id, "indicator_type": "trade_balance", "value": -298.2, "unit": "million USD", "period": "2026-03", "recorded_at": datetime(2026, 4, 15), "source": "Ministry of Commerce", "note": "3월 무역수지 적자 소폭 감소"},

        # 수출
        {"country_id": country_id, "indicator_type": "exports", "value": 1250.5, "unit": "million USD", "period": "2026-01", "recorded_at": datetime(2026, 2, 15), "source": "Ministry of Commerce", "note": "1월 수출액 (천연가스, 의류, 농산물 중심)"},
        {"country_id": country_id, "indicator_type": "exports", "value": 1180.3, "unit": "million USD", "period": "2026-02", "recorded_at": datetime(2026, 3, 15), "source": "Ministry of Commerce", "note": "2월 수출액 감소 (설 연휴 영향)"},
        {"country_id": country_id, "indicator_type": "exports", "value": 1320.8, "unit": "million USD", "period": "2026-03", "recorded_at": datetime(2026, 4, 15), "source": "Ministry of Commerce", "note": "3월 수출액 회복"},

        # 수입
        {"country_id": country_id, "indicator_type": "imports", "value": 1536.0, "unit": "million USD", "period": "2026-01", "recorded_at": datetime(2026, 2, 15), "source": "Ministry of Commerce", "note": "1월 수입액 (석유, 기계류, 소비재)"},
        {"country_id": country_id, "indicator_type": "imports", "value": 1493.1, "unit": "million USD", "period": "2026-02", "recorded_at": datetime(2026, 3, 15), "source": "Ministry of Commerce", "note": "2월 수입액"},
        {"country_id": country_id, "indicator_type": "imports", "value": 1619.0, "unit": "million USD", "period": "2026-03", "recorded_at": datetime(2026, 4, 15), "source": "Ministry of Commerce", "note": "3월 수입액 증가"},

        # 실업률
        {"country_id": country_id, "indicator_type": "unemployment_rate", "value": 4.2, "unit": "%", "period": "2026-Q1", "recorded_at": datetime(2026, 4, 10), "source": "Ministry of Labour", "note": "2026년 1분기 실업률"},

        # 산업생산지수
        {"country_id": country_id, "indicator_type": "industrial_production", "value": 112.5, "unit": "Index (2020=100)", "period": "2026-01", "recorded_at": datetime(2026, 2, 20), "source": "Central Statistical Organization", "note": "1월 산업생산지수"},
        {"country_id": country_id, "indicator_type": "industrial_production", "value": 108.3, "unit": "Index (2020=100)", "period": "2026-02", "recorded_at": datetime(2026, 3, 20), "source": "Central Statistical Organization", "note": "2월 산업생산지수 (설 연휴 영향)"},
        {"country_id": country_id, "indicator_type": "industrial_production", "value": 115.8, "unit": "Index (2020=100)", "period": "2026-03", "recorded_at": datetime(2026, 4, 20), "source": "Central Statistical Organization", "note": "3월 산업생산지수 회복"},
    ]


def populate_indonesia_indicators_data(country_id: int) -> list:
    """인도네시아 경제 지표 데이터 반환"""
    return [
        # 환율 (IDR/USD) - 월별
        {"country_id": country_id, "indicator_type": "exchange_rate", "value": 15235.50, "unit": "IDR/USD", "period": "2026-01", "recorded_at": datetime(2026, 1, 31), "source": "Bank Indonesia", "note": "2026년 1월 말 기준 환율"},
        {"country_id": country_id, "indicator_type": "exchange_rate", "value": 15198.20, "unit": "IDR/USD", "period": "2026-02", "recorded_at": datetime(2026, 2, 28), "source": "Bank Indonesia", "note": "2월 루피화 강세 (2년 만에 최고치)"},
        {"country_id": country_id, "indicator_type": "exchange_rate", "value": 15220.80, "unit": "IDR/USD", "period": "2026-03", "recorded_at": datetime(2026, 3, 31), "source": "Bank Indonesia", "note": "3월 환율 소폭 상승"},
        {"country_id": country_id, "indicator_type": "exchange_rate", "value": 15205.30, "unit": "IDR/USD", "period": "2026-04", "recorded_at": datetime(2026, 4, 15), "source": "Bank Indonesia", "note": "4월 중순 환율 안정세"},

        # GDP 성장률
        {"country_id": country_id, "indicator_type": "gdp_growth", "value": 5.2, "unit": "%", "period": "2026-Q1", "recorded_at": datetime(2026, 4, 5), "source": "Statistics Indonesia (BPS)", "note": "2026년 1분기 GDP 성장률 (전년 동기 대비)"},
        {"country_id": country_id, "indicator_type": "gdp_growth_forecast", "value": 5.3, "unit": "%", "period": "2026", "recorded_at": datetime(2026, 3, 10), "source": "International Monetary Fund (IMF)", "note": "2026년 연간 GDP 성장률 전망"},

        # 인플레이션 (CPI) - 월별
        {"country_id": country_id, "indicator_type": "inflation", "value": 2.8, "unit": "%", "period": "2026-01", "recorded_at": datetime(2026, 2, 1), "source": "Statistics Indonesia (BPS)", "note": "1월 소비자물가지수 (전년 동월 대비)"},
        {"country_id": country_id, "indicator_type": "inflation", "value": 2.9, "unit": "%", "period": "2026-02", "recorded_at": datetime(2026, 3, 1), "source": "Statistics Indonesia (BPS)", "note": "2월 인플레이션 소폭 상승"},
        {"country_id": country_id, "indicator_type": "inflation", "value": 2.7, "unit": "%", "period": "2026-03", "recorded_at": datetime(2026, 4, 1), "source": "Statistics Indonesia (BPS)", "note": "3월 인플레이션 둔화"},
        {"country_id": country_id, "indicator_type": "inflation", "value": 2.8, "unit": "%", "period": "2026-04", "recorded_at": datetime(2026, 4, 15), "source": "Statistics Indonesia (BPS)", "note": "4월 인플레이션 (속보치)"},

        # 기준금리 (BI Rate)
        {"country_id": country_id, "indicator_type": "interest_rate", "value": 6.00, "unit": "%", "period": "2026-01", "recorded_at": datetime(2026, 1, 20), "source": "Bank Indonesia", "note": "1월 BI 7-Day Reverse Repo Rate"},
        {"country_id": country_id, "indicator_type": "interest_rate", "value": 6.00, "unit": "%", "period": "2026-02", "recorded_at": datetime(2026, 2, 20), "source": "Bank Indonesia", "note": "2월 기준금리 동결"},
        {"country_id": country_id, "indicator_type": "interest_rate", "value": 6.00, "unit": "%", "period": "2026-03", "recorded_at": datetime(2026, 3, 20), "source": "Bank Indonesia", "note": "3월 기준금리 동결"},
        {"country_id": country_id, "indicator_type": "interest_rate", "value": 5.75, "unit": "%", "period": "2026-04", "recorded_at": datetime(2026, 4, 10), "source": "Bank Indonesia", "note": "4월 기준금리 25bp 인하 (경제 성장 지원)"},

        # 외환보유액
        {"country_id": country_id, "indicator_type": "forex_reserve", "value": 145.2, "unit": "billion USD", "period": "2026-01", "recorded_at": datetime(2026, 2, 7), "source": "Bank Indonesia", "note": "1월 말 기준 외환보유액 (수입 6.8개월분)"},
        {"country_id": country_id, "indicator_type": "forex_reserve", "value": 146.8, "unit": "billion USD", "period": "2026-02", "recorded_at": datetime(2026, 3, 7), "source": "Bank Indonesia", "note": "2월 말 외환보유액 증가"},
        {"country_id": country_id, "indicator_type": "forex_reserve", "value": 148.5, "unit": "billion USD", "period": "2026-03", "recorded_at": datetime(2026, 4, 7), "source": "Bank Indonesia", "note": "3월 말 외환보유액 역대 최고 수준"},

        # 무역수지
        {"country_id": country_id, "indicator_type": "trade_balance", "value": 3850.5, "unit": "million USD", "period": "2026-01", "recorded_at": datetime(2026, 2, 15), "source": "Statistics Indonesia (BPS)", "note": "1월 무역수지 흑자 (41개월 연속)"},
        {"country_id": country_id, "indicator_type": "trade_balance", "value": 3620.2, "unit": "million USD", "period": "2026-02", "recorded_at": datetime(2026, 3, 15), "source": "Statistics Indonesia (BPS)", "note": "2월 무역수지 흑자 지속"},
        {"country_id": country_id, "indicator_type": "trade_balance", "value": 4125.8, "unit": "million USD", "period": "2026-03", "recorded_at": datetime(2026, 4, 15), "source": "Statistics Indonesia (BPS)", "note": "3월 무역수지 흑자 확대"},

        # 수출
        {"country_id": country_id, "indicator_type": "exports", "value": 22850.3, "unit": "million USD", "period": "2026-01", "recorded_at": datetime(2026, 2, 15), "source": "Statistics Indonesia (BPS)", "note": "1월 수출액 (팜오일, 석탄, 광물 중심)"},
        {"country_id": country_id, "indicator_type": "exports", "value": 21320.5, "unit": "million USD", "period": "2026-02", "recorded_at": datetime(2026, 3, 15), "source": "Statistics Indonesia (BPS)", "note": "2월 수출액 (설 연휴 영향으로 감소)"},
        {"country_id": country_id, "indicator_type": "exports", "value": 24680.2, "unit": "million USD", "period": "2026-03", "recorded_at": datetime(2026, 4, 15), "source": "Statistics Indonesia (BPS)", "note": "3월 수출액 반등 (원자재 가격 상승)"},

        # 수입
        {"country_id": country_id, "indicator_type": "imports", "value": 18999.8, "unit": "million USD", "period": "2026-01", "recorded_at": datetime(2026, 2, 15), "source": "Statistics Indonesia (BPS)", "note": "1월 수입액 (원자재, 자본재)"},
        {"country_id": country_id, "indicator_type": "imports", "value": 17700.3, "unit": "million USD", "period": "2026-02", "recorded_at": datetime(2026, 3, 15), "source": "Statistics Indonesia (BPS)", "note": "2월 수입액"},
        {"country_id": country_id, "indicator_type": "imports", "value": 20554.4, "unit": "million USD", "period": "2026-03", "recorded_at": datetime(2026, 4, 15), "source": "Statistics Indonesia (BPS)", "note": "3월 수입액 증가"},

        # 실업률
        {"country_id": country_id, "indicator_type": "unemployment_rate", "value": 5.3, "unit": "%", "period": "2026-02", "recorded_at": datetime(2026, 3, 20), "source": "Statistics Indonesia (BPS)", "note": "2월 실업률 (2023년 이후 최저)"},

        # 제조업 PMI
        {"country_id": country_id, "indicator_type": "manufacturing_pmi", "value": 52.3, "unit": "Index", "period": "2026-01", "recorded_at": datetime(2026, 2, 1), "source": "S&P Global", "note": "1월 제조업 PMI (50 초과 = 확장)"},
        {"country_id": country_id, "indicator_type": "manufacturing_pmi", "value": 51.8, "unit": "Index", "period": "2026-02", "recorded_at": datetime(2026, 3, 1), "source": "S&P Global", "note": "2월 제조업 PMI 소폭 하락"},
        {"country_id": country_id, "indicator_type": "manufacturing_pmi", "value": 53.1, "unit": "Index", "period": "2026-03", "recorded_at": datetime(2026, 4, 1), "source": "S&P Global", "note": "3월 제조업 PMI 상승 (9개월 만에 최고)"},
        {"country_id": country_id, "indicator_type": "manufacturing_pmi", "value": 52.8, "unit": "Index", "period": "2026-04", "recorded_at": datetime(2026, 4, 15), "source": "S&P Global", "note": "4월 제조업 PMI (속보치)"},

        # 소비자신뢰지수
        {"country_id": country_id, "indicator_type": "consumer_confidence", "value": 125.8, "unit": "Index", "period": "2026-01", "recorded_at": datetime(2026, 2, 10), "source": "Bank Indonesia", "note": "1월 소비자신뢰지수 (100 초과 = 낙관)"},
        {"country_id": country_id, "indicator_type": "consumer_confidence", "value": 128.2, "unit": "Index", "period": "2026-02", "recorded_at": datetime(2026, 3, 10), "source": "Bank Indonesia", "note": "2월 소비자신뢰지수 상승"},
        {"country_id": country_id, "indicator_type": "consumer_confidence", "value": 127.5, "unit": "Index", "period": "2026-03", "recorded_at": datetime(2026, 4, 10), "source": "Bank Indonesia", "note": "3월 소비자신뢰지수 소폭 하락"},

        # 정부부채
        {"country_id": country_id, "indicator_type": "government_debt", "value": 38.2, "unit": "% of GDP", "period": "2026-Q1", "recorded_at": datetime(2026, 4, 12), "source": "Ministry of Finance", "note": "2026년 1분기 정부부채 비율 (건전 수준 유지)"},

        # 외국인 직접투자 (FDI)
        {"country_id": country_id, "indicator_type": "fdi", "value": 8950.5, "unit": "million USD", "period": "2026-Q1", "recorded_at": datetime(2026, 4, 10), "source": "Investment Coordinating Board (BKPM)", "note": "2026년 1분기 외국인 직접투자 (전년 동기 대비 12.5% 증가)"},

        # 소매판매
        {"country_id": country_id, "indicator_type": "retail_sales", "value": 7.8, "unit": "% YoY", "period": "2026-01", "recorded_at": datetime(2026, 2, 20), "source": "Statistics Indonesia (BPS)", "note": "1월 소매판매 성장률"},
        {"country_id": country_id, "indicator_type": "retail_sales", "value": 8.5, "unit": "% YoY", "period": "2026-02", "recorded_at": datetime(2026, 3, 20), "source": "Statistics Indonesia (BPS)", "note": "2월 소매판매 (설 특수)"},
        {"country_id": country_id, "indicator_type": "retail_sales", "value": 7.2, "unit": "% YoY", "period": "2026-03", "recorded_at": datetime(2026, 4, 20), "source": "Statistics Indonesia (BPS)", "note": "3월 소매판매"},

        # 자동차 판매
        {"country_id": country_id, "indicator_type": "auto_sales", "value": 92500, "unit": "units", "period": "2026-01", "recorded_at": datetime(2026, 2, 5), "source": "Gaikindo (Automotive Industry Association)", "note": "1월 자동차 판매량"},
        {"country_id": country_id, "indicator_type": "auto_sales", "value": 85200, "unit": "units", "period": "2026-02", "recorded_at": datetime(2026, 3, 5), "source": "Gaikindo", "note": "2월 자동차 판매량 (설 영향)"},
        {"country_id": country_id, "indicator_type": "auto_sales", "value": 98700, "unit": "units", "period": "2026-03", "recorded_at": datetime(2026, 4, 5), "source": "Gaikindo", "note": "3월 자동차 판매량 반등"},

        # 관광객 수
        {"country_id": country_id, "indicator_type": "tourist_arrivals", "value": 1.35, "unit": "million", "period": "2026-01", "recorded_at": datetime(2026, 2, 25), "source": "Statistics Indonesia (BPS)", "note": "1월 외국인 관광객 수"},
        {"country_id": country_id, "indicator_type": "tourist_arrivals", "value": 1.28, "unit": "million", "period": "2026-02", "recorded_at": datetime(2026, 3, 25), "source": "Statistics Indonesia (BPS)", "note": "2월 외국인 관광객 수"},
        {"country_id": country_id, "indicator_type": "tourist_arrivals", "value": 1.42, "unit": "million", "period": "2026-03", "recorded_at": datetime(2026, 4, 25), "source": "Statistics Indonesia (BPS)", "note": "3월 외국인 관광객 수 (성수기)"},
    ]


@router.post("/crawl-news")
async def crawl_news_from_websites(
    country_code: str = None,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    웹 크롤링으로 뉴스/공시 수집 (관리자 전용)
    - country_code: 'MM' (미얀마만), 'ID' (인도네시아만), None (전체)
    """
    try:
        from services.news_crawler import news_crawler

        logger.info(f"🌐 웹 크롤링 시작 (country_code: {country_code or 'all'})")

        if country_code == 'MM':
            # 미얀마만
            count = await news_crawler.crawl_cbm_news(db)
            return {
                "success": True,
                "message": f"미얀마 CBM 뉴스 수집 완료",
                "count": count,
                "source": "Central Bank of Myanmar"
            }
        elif country_code == 'ID':
            # 인도네시아만
            count = await news_crawler.crawl_ojk_announcements(db)
            return {
                "success": True,
                "message": f"인도네시아 OJK 공시 수집 완료",
                "count": count,
                "source": "Otoritas Jasa Keuangan"
            }
        else:
            # 전체
            results = await news_crawler.crawl_all(db)
            return {
                "success": True,
                "message": f"전체 웹 크롤링 완료",
                "cbm_count": results['cbm'],
                "ojk_count": results['ojk'],
                "total_count": results['total'],
                "sources": ["CBM", "OJK"]
            }

    except Exception as e:
        logger.error(f"❌ 웹 크롤링 실패: {e}")
        raise HTTPException(status_code=500, detail=f"웹 크롤링 실패: {str(e)}")


@router.post("/test-email")
async def send_test_email(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    이메일 알림 테스트 (관리자 전용)
    - SMTP 설정이 올바른지 확인
    """
    try:
        from services.email_notifier import email_notifier

        if not email_notifier.enabled:
            return {
                "success": False,
                "message": "이메일 알림이 비활성화되어 있습니다.",
                "error": "SMTP 설정을 확인하세요 (.env 파일의 SMTP_* 환경변수)"
            }

        # 테스트 이메일 발송
        success = email_notifier.send_email(
            subject="[테스트] JB우리캐피탈 모니터링 시스템 알림",
            body=f"이메일 알림 시스템이 정상적으로 작동하고 있습니다.\n\n테스트 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            to_emails=email_notifier.admin_emails,
            html=False
        )

        if success:
            return {
                "success": True,
                "message": f"테스트 이메일 발송 완료",
                "recipients": email_notifier.admin_emails
            }
        else:
            return {
                "success": False,
                "message": "이메일 발송 실패",
                "error": "SMTP 연결 또는 인증 실패"
            }

    except Exception as e:
        logger.error(f"❌ 이메일 테스트 실패: {e}")
        raise HTTPException(status_code=500, detail=f"이메일 테스트 실패: {str(e)}")


@router.post("/ai-summarize-news")
async def ai_summarize_news(
    country_code: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    AI 뉴스 요약 (Claude API) - 관리자 전용
    """
    try:
        from services.ai_summarizer import ai_summarizer

        if not ai_summarizer.enabled:
            return {
                "success": False,
                "message": "AI 요약이 비활성화되어 있습니다.",
                "error": "CLAUDE_API_KEY를 설정하세요 (.env 파일)"
            }

        # 국가 정보 조회
        country = db.query(Country).filter(Country.code == country_code).first()
        if not country:
            raise HTTPException(status_code=404, detail="국가를 찾을 수 없습니다")

        # 최근 뉴스 조회 (최대 10개)
        news_list = db.query(News).filter(
            News.country_id == country.id
        ).order_by(
            News.published_at.desc()
        ).limit(10).all()

        if not news_list:
            return {
                "success": False,
                "message": f"{country.name_ko}의 뉴스가 없습니다."
            }

        # AI 요약 생성
        summary = ai_summarizer.summarize_news(news_list, country.name_ko)

        return {
            "success": True,
            "message": f"{country.name_ko} 뉴스 AI 요약 완료",
            "country": country.name_ko,
            "news_count": len(news_list),
            "summary": summary
        }

    except Exception as e:
        logger.error(f"❌ AI 뉴스 요약 실패: {e}")
        raise HTTPException(status_code=500, detail=f"AI 요약 실패: {str(e)}")


@router.post("/ai-analyze-indicators")
async def ai_analyze_indicators(
    country_code: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    AI 경제 지표 분석 (Claude API) - 관리자 전용
    """
    try:
        from services.ai_summarizer import ai_summarizer

        if not ai_summarizer.enabled:
            return {
                "success": False,
                "message": "AI 분석이 비활성화되어 있습니다.",
                "error": "CLAUDE_API_KEY를 설정하세요 (.env 파일)"
            }

        # 국가 정보 조회
        country = db.query(Country).filter(Country.code == country_code).first()
        if not country:
            raise HTTPException(status_code=404, detail="국가를 찾을 수 없습니다")

        # 경제 지표 조회
        indicators = db.query(EconomicIndicator).filter(
            EconomicIndicator.country_id == country.id
        ).all()

        if not indicators:
            return {
                "success": False,
                "message": f"{country.name_ko}의 경제 지표가 없습니다."
            }

        # AI 분석 생성
        analysis = ai_summarizer.analyze_indicators(indicators, country.name_ko)

        return {
            "success": True,
            "message": f"{country.name_ko} 경제 지표 AI 분석 완료",
            "country": country.name_ko,
            "indicators_count": len(indicators),
            "analysis": analysis
        }

    except Exception as e:
        logger.error(f"❌ AI 지표 분석 실패: {e}")
        raise HTTPException(status_code=500, detail=f"AI 분석 실패: {str(e)}")


@router.post("/ai-compare-countries")
async def ai_compare_countries(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    AI 국가 비교 분석 (미얀마 vs 인도네시아) - 관리자 전용
    """
    try:
        from services.ai_summarizer import ai_summarizer

        if not ai_summarizer.enabled:
            return {
                "success": False,
                "message": "AI 분석이 비활성화되어 있습니다.",
                "error": "CLAUDE_API_KEY를 설정하세요 (.env 파일)"
            }

        # 양국 정보 조회
        myanmar = db.query(Country).filter(Country.code == 'MM').first()
        indonesia = db.query(Country).filter(Country.code == 'ID').first()

        if not myanmar or not indonesia:
            raise HTTPException(status_code=404, detail="국가 정보를 찾을 수 없습니다")

        # 양국 경제 지표 조회
        mm_indicators = db.query(EconomicIndicator).filter(
            EconomicIndicator.country_id == myanmar.id
        ).all()

        id_indicators = db.query(EconomicIndicator).filter(
            EconomicIndicator.country_id == indonesia.id
        ).all()

        if not mm_indicators or not id_indicators:
            return {
                "success": False,
                "message": "경제 지표 데이터가 부족합니다."
            }

        # AI 비교 분석 생성
        insight = ai_summarizer.generate_comparison_insight(mm_indicators, id_indicators)

        return {
            "success": True,
            "message": "미얀마 vs 인도네시아 AI 비교 분석 완료",
            "myanmar_indicators": len(mm_indicators),
            "indonesia_indicators": len(id_indicators),
            "insight": insight
        }

    except Exception as e:
        logger.error(f"❌ AI 비교 분석 실패: {e}")
        raise HTTPException(status_code=500, detail=f"AI 분석 실패: {str(e)}")
