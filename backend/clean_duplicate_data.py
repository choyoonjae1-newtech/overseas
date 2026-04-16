"""
중복 데이터 제거 스크립트
- 뉴스 중복 제거 (제목 기준)
- 이벤트 중복 제거 (제목 + 날짜 기준)
- 경제 지표 중복 제거 (country_id + indicator_type + period 기준)
"""
from core.database import SessionLocal
from models import News, Event, EconomicIndicator, Country
from datetime import datetime


def remove_duplicate_news(db):
    """중복 뉴스 제거 (가장 최근 것만 유지)"""
    print("🔍 뉴스 중복 제거 중...")

    news_list = db.query(News).all()
    print(f"  총 뉴스: {len(news_list)}개")

    # 제목 + 국가 기준으로 그룹화
    seen = {}
    to_delete = []

    for news in news_list:
        key = (news.title, news.country_id)

        if key in seen:
            # 중복 발견 - 더 최근 것 유지
            existing = seen[key]
            if news.created_at > existing.created_at:
                to_delete.append(existing)
                seen[key] = news
            else:
                to_delete.append(news)
        else:
            seen[key] = news

    if to_delete:
        for news in to_delete:
            db.delete(news)
        db.commit()
        print(f"  ✅ 중복 뉴스 {len(to_delete)}개 제거")
    else:
        print("  ✅ 중복 없음")

    remaining = db.query(News).count()
    print(f"  남은 뉴스: {remaining}개")


def remove_duplicate_events(db):
    """중복 이벤트 제거 (가장 최근 것만 유지)"""
    print("\n🔍 이벤트 중복 제거 중...")

    events_list = db.query(Event).all()
    print(f"  총 이벤트: {len(events_list)}개")

    # 제목 + 날짜 + 국가 기준으로 그룹화
    seen = {}
    to_delete = []

    for event in events_list:
        key = (event.title, event.event_date, event.country_id)

        if key in seen:
            # 중복 발견 - 더 최근 것 유지
            existing = seen[key]
            if event.created_at > existing.created_at:
                to_delete.append(existing)
                seen[key] = event
            else:
                to_delete.append(event)
        else:
            seen[key] = event

    if to_delete:
        for event in to_delete:
            db.delete(event)
        db.commit()
        print(f"  ✅ 중복 이벤트 {len(to_delete)}개 제거")
    else:
        print("  ✅ 중복 없음")

    remaining = db.query(Event).count()
    print(f"  남은 이벤트: {remaining}개")


def remove_duplicate_indicators(db):
    """중복 경제 지표 제거 (가장 최근 것만 유지)"""
    print("\n🔍 경제 지표 중복 제거 중...")

    indicators_list = db.query(EconomicIndicator).all()
    print(f"  총 경제 지표: {len(indicators_list)}개")

    # country_id + indicator_type + period 기준으로 그룹화
    seen = {}
    to_delete = []

    for indicator in indicators_list:
        key = (indicator.country_id, indicator.indicator_type, indicator.period)

        if key in seen:
            # 중복 발견 - 더 최근 recorded_at 유지
            existing = seen[key]
            if indicator.recorded_at > existing.recorded_at:
                to_delete.append(existing)
                seen[key] = indicator
            else:
                to_delete.append(indicator)
        else:
            seen[key] = indicator

    if to_delete:
        for indicator in to_delete:
            db.delete(indicator)
        db.commit()
        print(f"  ✅ 중복 지표 {len(to_delete)}개 제거")
    else:
        print("  ✅ 중복 없음")

    remaining = db.query(EconomicIndicator).count()
    print(f"  남은 경제 지표: {remaining}개")

    # 최신 지표 확인
    if remaining > 0:
        latest = db.query(EconomicIndicator).order_by(
            EconomicIndicator.recorded_at.desc()
        ).first()
        country = db.query(Country).filter(Country.id == latest.country_id).first()
        print(f"  최신 지표: {country.name_ko if country else 'Unknown'} / {latest.indicator_type} / {latest.recorded_at}")


def clean_all_duplicates():
    """모든 중복 데이터 제거"""
    print("=" * 60)
    print("중복 데이터 제거 시작")
    print("=" * 60)

    db = SessionLocal()

    try:
        remove_duplicate_news(db)
        remove_duplicate_events(db)
        remove_duplicate_indicators(db)

        print("\n" + "=" * 60)
        print("🎉 중복 데이터 제거 완료!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    clean_all_duplicates()
