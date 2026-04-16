"""
데이터베이스 초기화 및 데이터 수집 스크립트
- 사용자 계정 제외 전체 데이터 삭제
- 2026년 1월~4월 경제 지표, 뉴스, 이벤트 수집
"""
import asyncio
from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session
from core.database import SessionLocal, engine
from models import Country, News, Event, EconomicIndicator
from services.indicators_collector import indicators_collector
import httpx

def clear_data(db: Session):
    """사용자 계정 제외 모든 데이터 삭제"""
    print("🗑️  기존 데이터 삭제 중...")

    # 뉴스, 이벤트, 경제 지표 삭제
    db.query(News).delete()
    db.query(Event).delete()
    db.query(EconomicIndicator).delete()

    db.commit()
    print("✅ 기존 데이터 삭제 완료")


def ensure_countries(db: Session):
    """국가 데이터 확인 및 생성"""
    print("🌍 국가 데이터 확인 중...")

    countries_data = [
        {"code": "MM", "name_en": "Myanmar", "name_ko": "미얀마", "flag_emoji": "🇲🇲"},
        {"code": "ID", "name_en": "Indonesia", "name_ko": "인도네시아", "flag_emoji": "🇮🇩"}
    ]

    for country_data in countries_data:
        exists = db.query(Country).filter(Country.code == country_data["code"]).first()
        if not exists:
            country = Country(**country_data)
            db.add(country)
            print(f"✅ 국가 추가: {country_data['name_ko']}")
        else:
            print(f"ℹ️  국가 이미 존재: {country_data['name_ko']}")

    db.commit()


def populate_sample_news(db: Session):
    """2026년 1월~4월 샘플 뉴스 데이터 생성"""
    print("📰 뉴스 데이터 생성 중...")

    mm_country = db.query(Country).filter(Country.code == "MM").first()
    id_country = db.query(Country).filter(Country.code == "ID").first()

    # 미얀마 뉴스 (2026.1~4)
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

    # 인도네시아 뉴스 (2026.1~4)
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

    all_news = myanmar_news + indonesia_news
    for news_data in all_news:
        news = News(**news_data)
        db.add(news)

    db.commit()
    print(f"✅ 뉴스 {len(all_news)}개 생성 완료")


def populate_events(db: Session):
    """2026년 1월~12월 주요 일정 생성"""
    print("📅 주요 일정 생성 중...")

    mm_country = db.query(Country).filter(Country.code == "MM").first()
    id_country = db.query(Country).filter(Country.code == "ID").first()

    events = [
        # 미얀마 공휴일 및 주요 일정
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
            "title": "노동절",
            "description": "근로자의 날",
            "event_date": date(2026, 5, 1),
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

        # 인도네시아 공휴일 및 주요 일정
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
            "title": "노동절",
            "description": "근로자의 날",
            "event_date": date(2026, 5, 1),
            "event_type": "holiday",
            "source": "Indonesia Public Holidays"
        },
        {
            "country_id": id_country.id,
            "title": "라마단 종료 (Idul Fitri)",
            "description": "이슬람 최대 명절",
            "event_date": date(2026, 5, 13),
            "event_type": "holiday",
            "source": "Indonesia Public Holidays"
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
    print(f"✅ 일정 {len(events)}개 생성 완료")


async def collect_economic_indicators():
    """경제 지표 수집"""
    print("📊 경제 지표 수집 중...")
    try:
        await indicators_collector.collect_all_indicators()
        print("✅ 경제 지표 수집 완료")
    except Exception as e:
        print(f"⚠️  경제 지표 수집 실패: {e}")
        print("   (World Bank API 제한 또는 네트워크 문제일 수 있습니다)")


async def main():
    """메인 실행 함수"""
    print("\n" + "="*60)
    print("🔄 데이터베이스 초기화 및 데이터 수집 시작")
    print("="*60 + "\n")

    db = SessionLocal()

    try:
        # 1. 기존 데이터 삭제 (사용자 계정 제외)
        clear_data(db)

        # 2. 국가 데이터 확인
        ensure_countries(db)

        # 3. 샘플 뉴스 데이터 생성 (2026.1~4)
        populate_sample_news(db)

        # 4. 주요 일정 생성 (2026년 전체)
        populate_events(db)

        # 5. 경제 지표 수집 (실시간 API)
        await collect_economic_indicators()

        print("\n" + "="*60)
        print("🎉 데이터 수집 완료!")
        print("="*60)
        print("\n📊 수집된 데이터:")
        print(f"   - 뉴스: {db.query(News).count()}개")
        print(f"   - 일정/이벤트: {db.query(Event).count()}개")
        print(f"   - 경제 지표: {db.query(EconomicIndicator).count()}개")
        print(f"   - 국가: {db.query(Country).count()}개")
        print("\n")

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(main())
