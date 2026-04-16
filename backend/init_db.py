"""
데이터베이스 초기화 스크립트
- 관리자 계정 생성
- 국가 데이터 삽입
- 샘플 뉴스/이벤트 데이터 생성
"""
from sqlalchemy.orm import Session
from core.database import SessionLocal, engine, Base
from core.security import get_password_hash
from core.config import settings
from models import User, Country, News, Event
from datetime import datetime, timedelta


def init_database():
    """데이터베이스 초기화"""
    print("🔧 데이터베이스 초기화 시작...")

    # 테이블 생성
    Base.metadata.create_all(bind=engine)
    print("✅ 테이블 생성 완료")

    db = SessionLocal()

    try:
        # 1. 관리자 계정 생성
        admin_exists = db.query(User).filter(User.username == settings.ADMIN_USERNAME).first()
        if not admin_exists:
            # bcrypt는 72바이트까지만 지원하므로 비밀번호를 자름
            password = settings.ADMIN_PASSWORD[:72]
            admin = User(
                username=settings.ADMIN_USERNAME,
                email=settings.ADMIN_EMAIL,
                hashed_password=get_password_hash(password),
                role="admin",
                status="approved"
            )
            db.add(admin)
            db.commit()
            print(f"✅ 관리자 계정 생성 완료: {settings.ADMIN_USERNAME}")
        else:
            print(f"ℹ️  관리자 계정 이미 존재: {settings.ADMIN_USERNAME}")

        # 2. 국가 데이터 삽입
        countries_data = [
            {"code": "MM", "name_en": "Myanmar", "name_ko": "미얀마", "flag_emoji": "🇲🇲"},
            {"code": "ID", "name_en": "Indonesia", "name_ko": "인도네시아", "flag_emoji": "🇮🇩"}
        ]

        for country_data in countries_data:
            exists = db.query(Country).filter(Country.code == country_data["code"]).first()
            if not exists:
                country = Country(**country_data)
                db.add(country)
                print(f"✅ 국가 추가: {country_data['name_ko']} ({country_data['code']})")
            else:
                print(f"ℹ️  국가 이미 존재: {country_data['name_ko']}")

        db.commit()

        # 3. 샘플 뉴스 데이터 생성
        mm_country = db.query(Country).filter(Country.code == "MM").first()
        id_country = db.query(Country).filter(Country.code == "ID").first()

        sample_news = [
            {
                "country_id": mm_country.id,
                "title": "미얀마 중앙은행, 외환 규제 완화 발표",
                "content": "미얀마 중앙은행(CBM)이 외환 거래 규제를 일부 완화한다고 발표했습니다. 이는 외국인 투자 유치를 위한 조치로 해석됩니다.",
                "source": "Central Bank of Myanmar",
                "url": "https://www.cbm.gov.mm/",
                "category": "regulation",
                "published_at": datetime.utcnow() - timedelta(days=1),
                "source_type": "manual"
            },
            {
                "country_id": id_country.id,
                "title": "인도네시아 OJK, 핀테크 라이선스 요건 강화",
                "content": "인도네시아 금융감독청(OJK)이 핀테크 기업에 대한 라이선스 요건을 강화하기로 했습니다.",
                "source": "Otoritas Jasa Keuangan (OJK)",
                "url": "https://www.ojk.go.id/",
                "category": "regulation",
                "published_at": datetime.utcnow() - timedelta(days=2),
                "source_type": "manual"
            },
            {
                "country_id": mm_country.id,
                "title": "미얀마 정세 불안정, 외국인 투자 감소",
                "content": "미얀마의 정치적 불안정으로 인해 외국인 직접 투자가 전년 대비 30% 감소했습니다.",
                "source": "Reuters",
                "url": "https://www.reuters.com/",
                "category": "geopolitical",
                "published_at": datetime.utcnow() - timedelta(days=3),
                "source_type": "api"
            },
        ]

        for news_data in sample_news:
            news = News(**news_data)
            db.add(news)

        db.commit()
        print(f"✅ 샘플 뉴스 {len(sample_news)}개 생성 완료")

        # 4. 샘플 이벤트 (공휴일) 데이터 생성
        sample_events = [
            {
                "country_id": mm_country.id,
                "title": "미얀마 독립기념일",
                "description": "미얀마의 국경일",
                "event_date": datetime(2026, 1, 4).date(),
                "event_type": "holiday",
                "source": "Myanmar Public Holidays"
            },
            {
                "country_id": id_country.id,
                "title": "인도네시아 독립기념일",
                "description": "인도네시아의 국경일",
                "event_date": datetime(2026, 8, 17).date(),
                "event_type": "holiday",
                "source": "Indonesia Public Holidays"
            },
            {
                "country_id": mm_country.id,
                "title": "CBM 신규 규제 시행일",
                "description": "미얀마 중앙은행 외환 규제 시행",
                "event_date": datetime(2026, 6, 1).date(),
                "event_type": "regulation",
                "source": "CBM"
            },
        ]

        for event_data in sample_events:
            event = Event(**event_data)
            db.add(event)

        db.commit()
        print(f"✅ 샘플 이벤트 {len(sample_events)}개 생성 완료")

        print("\n🎉 데이터베이스 초기화 완료!")
        print(f"\n📌 관리자 로그인 정보:")
        print(f"   Username: {settings.ADMIN_USERNAME}")
        print(f"   Password: {settings.ADMIN_PASSWORD}")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
