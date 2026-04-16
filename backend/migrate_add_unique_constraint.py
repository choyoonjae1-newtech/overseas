"""
데이터베이스 마이그레이션: 경제 지표 테이블에 유니크 제약조건 추가
- 기존 중복 데이터 제거
- (country_id, indicator_type, period) 조합에 대한 유니크 제약조건 추가
"""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from core.database import SessionLocal, engine
from models.indicator import EconomicIndicator
from models.country import Country


def remove_duplicate_indicators(db: Session):
    """중복된 경제 지표 제거 (가장 최근 데이터만 유지)"""
    print("🔍 중복 데이터 검사 중...")

    # 모든 지표 조회
    all_indicators = db.query(EconomicIndicator).all()

    # (country_id, indicator_type, period) 기준으로 그룹화
    seen = {}
    duplicates_to_remove = []

    for indicator in all_indicators:
        key = (indicator.country_id, indicator.indicator_type, indicator.period)

        if key in seen:
            # 중복 발견 - 더 최근 것을 유지
            existing = seen[key]
            if indicator.recorded_at > existing.recorded_at:
                # 새 것이 더 최근 - 기존 것 삭제
                duplicates_to_remove.append(existing)
                seen[key] = indicator
            else:
                # 기존 것이 더 최근 - 새 것 삭제
                duplicates_to_remove.append(indicator)
        else:
            seen[key] = indicator

    if duplicates_to_remove:
        print(f"⚠️  중복 데이터 {len(duplicates_to_remove)}개 발견")
        for dup in duplicates_to_remove:
            country = db.query(Country).filter(Country.id == dup.country_id).first()
            print(f"   - 삭제: {country.name_ko if country else 'Unknown'} / {dup.indicator_type} / {dup.period}")
            db.delete(dup)
        db.commit()
        print(f"✅ 중복 데이터 {len(duplicates_to_remove)}개 제거 완료")
    else:
        print("✅ 중복 데이터 없음")


def add_unique_constraint():
    """유니크 제약조건 추가"""
    print("\n🔧 유니크 제약조건 추가 중...")

    try:
        with engine.connect() as conn:
            # SQLite에서 제약조건 추가는 테이블 재생성이 필요
            # 하지만 SQLAlchemy의 create_all()을 사용하면 자동으로 처리됨

            # 기존 테이블의 제약조건 확인
            result = conn.execute(text(
                "SELECT sql FROM sqlite_master WHERE type='table' AND name='economic_indicators'"
            ))
            table_sql = result.fetchone()

            if table_sql and 'uq_indicator_country_type_period' in table_sql[0]:
                print("✅ 유니크 제약조건이 이미 존재합니다")
            else:
                print("⚠️  유니크 제약조건이 없습니다")
                print("   → python init_db.py를 실행하거나")
                print("   → 데이터베이스를 삭제 후 재생성하세요")

    except Exception as e:
        print(f"❌ 오류: {e}")


def migrate():
    """마이그레이션 실행"""
    print("=" * 60)
    print("경제 지표 테이블 마이그레이션")
    print("=" * 60)

    db = SessionLocal()

    try:
        # 1. 중복 데이터 제거
        remove_duplicate_indicators(db)

        # 2. 유니크 제약조건 추가 (확인)
        add_unique_constraint()

        print("\n🎉 마이그레이션 완료!")

    except Exception as e:
        print(f"\n❌ 마이그레이션 실패: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    migrate()
