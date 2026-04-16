"""
관리자 전용 API 엔드포인트
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models import User, Country, News, Event, EconomicIndicator
from core.security import get_current_admin
import asyncio
from datetime import datetime, date
from services.indicators_collector import indicators_collector

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
