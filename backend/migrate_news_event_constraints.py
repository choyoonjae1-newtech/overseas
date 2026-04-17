"""
뉴스 및 이벤트 테이블에 유니크 제약조건 추가
- News: UNIQUE(country_id, title)
- Event: UNIQUE(country_id, title, event_date)
"""
from core.database import SessionLocal, engine
from models import News, Event
from sqlalchemy import inspect, text
import sys


def check_and_remove_duplicates(db):
    """중복 데이터 제거"""
    print("=" * 60)
    print("1단계: 중복 데이터 확인 및 제거")
    print("=" * 60)

    # 뉴스 중복 제거
    print("\n📰 뉴스 중복 확인 중...")
    news_list = db.query(News).all()
    print(f"  총 뉴스: {len(news_list)}개")

    news_seen = {}
    news_to_delete = []

    for news in news_list:
        key = (news.country_id, news.title)
        if key in news_seen:
            existing = news_seen[key]
            if news.created_at > existing.created_at:
                news_to_delete.append(existing)
                news_seen[key] = news
            else:
                news_to_delete.append(news)
        else:
            news_seen[key] = news

    if news_to_delete:
        for news in news_to_delete:
            db.delete(news)
        db.commit()
        print(f"  ✅ 중복 뉴스 {len(news_to_delete)}개 제거")
    else:
        print("  ✅ 중복 없음")

    remaining_news = db.query(News).count()
    print(f"  남은 뉴스: {remaining_news}개")

    # 이벤트 중복 제거
    print("\n📅 이벤트 중복 확인 중...")
    events_list = db.query(Event).all()
    print(f"  총 이벤트: {len(events_list)}개")

    event_seen = {}
    event_to_delete = []

    for event in events_list:
        key = (event.country_id, event.title, event.event_date)
        if key in event_seen:
            existing = event_seen[key]
            if event.created_at > existing.created_at:
                event_to_delete.append(existing)
                event_seen[key] = event
            else:
                event_to_delete.append(event)
        else:
            event_seen[key] = event

    if event_to_delete:
        for event in event_to_delete:
            db.delete(event)
        db.commit()
        print(f"  ✅ 중복 이벤트 {len(event_to_delete)}개 제거")
    else:
        print("  ✅ 중복 없음")

    remaining_events = db.query(Event).count()
    print(f"  남은 이벤트: {remaining_events}개")


def add_unique_constraints(db):
    """유니크 제약조건 추가"""
    print("\n" + "=" * 60)
    print("2단계: 유니크 제약조건 추가")
    print("=" * 60)

    inspector = inspect(engine)

    # News 테이블 제약조건 확인
    print("\n📰 뉴스 테이블 제약조건 확인 중...")
    news_constraints = inspector.get_unique_constraints('news')
    news_has_constraint = any(
        set(c.get('column_names', [])) == {'country_id', 'title'}
        for c in news_constraints
    )

    if news_has_constraint:
        print("  ✅ 뉴스 유니크 제약조건이 이미 존재합니다")
    else:
        print("  ⚙️  뉴스 유니크 제약조건 추가 중...")
        try:
            # SQLite
            db.execute(text(
                "CREATE UNIQUE INDEX IF NOT EXISTS uq_news_country_title "
                "ON news(country_id, title)"
            ))
            db.commit()
            print("  ✅ 뉴스 유니크 제약조건 추가 완료")
        except Exception as e:
            print(f"  ⚠️  제약조건 추가 실패 (이미 존재할 수 있음): {e}")
            db.rollback()

    # Event 테이블 제약조건 확인
    print("\n📅 이벤트 테이블 제약조건 확인 중...")
    event_constraints = inspector.get_unique_constraints('events')
    event_has_constraint = any(
        set(c.get('column_names', [])) == {'country_id', 'title', 'event_date'}
        for c in event_constraints
    )

    if event_has_constraint:
        print("  ✅ 이벤트 유니크 제약조건이 이미 존재합니다")
    else:
        print("  ⚙️  이벤트 유니크 제약조건 추가 중...")
        try:
            # SQLite
            db.execute(text(
                "CREATE UNIQUE INDEX IF NOT EXISTS uq_event_country_title_date "
                "ON events(country_id, title, event_date)"
            ))
            db.commit()
            print("  ✅ 이벤트 유니크 제약조건 추가 완료")
        except Exception as e:
            print(f"  ⚠️  제약조건 추가 실패 (이미 존재할 수 있음): {e}")
            db.rollback()


def verify_constraints(db):
    """제약조건 검증"""
    print("\n" + "=" * 60)
    print("3단계: 제약조건 검증")
    print("=" * 60)

    inspector = inspect(engine)

    # News 제약조건 검증
    print("\n📰 뉴스 테이블 제약조건:")
    news_constraints = inspector.get_unique_constraints('news')
    news_indexes = inspector.get_indexes('news')

    for constraint in news_constraints:
        print(f"  - {constraint.get('name')}: {constraint.get('column_names')}")

    for index in news_indexes:
        if index.get('unique'):
            print(f"  - {index.get('name')}: {index.get('column_names')} (index)")

    # Event 제약조건 검증
    print("\n📅 이벤트 테이블 제약조건:")
    event_constraints = inspector.get_unique_constraints('events')
    event_indexes = inspector.get_indexes('events')

    for constraint in event_constraints:
        print(f"  - {constraint.get('name')}: {constraint.get('column_names')}")

    for index in event_indexes:
        if index.get('unique'):
            print(f"  - {index.get('name')}: {index.get('column_names')} (index)")


def main():
    print("=" * 60)
    print("뉴스/이벤트 유니크 제약조건 마이그레이션")
    print("=" * 60)

    db = SessionLocal()

    try:
        # 1. 중복 제거
        check_and_remove_duplicates(db)

        # 2. 제약조건 추가
        add_unique_constraints(db)

        # 3. 검증
        verify_constraints(db)

        print("\n" + "=" * 60)
        print("🎉 마이그레이션 완료!")
        print("=" * 60)
        print("\n💡 이제 뉴스/이벤트 중복 데이터가 자동으로 방지됩니다.")
        print("   - News: 같은 국가의 같은 제목은 하나만 저장")
        print("   - Event: 같은 국가, 같은 제목, 같은 날짜는 하나만 저장")
        print()

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
