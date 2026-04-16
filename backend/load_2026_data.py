"""
2026년 데이터 로딩 스크립트
실행: python load_2026_data.py
"""
from core.database import SessionLocal
from services.data_loader import load_2026_data


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 2026년 미얀마/인도네시아 데이터 로더")
    print("=" * 60)

    db = SessionLocal()
    try:
        load_2026_data(db)
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        db.rollback()
    finally:
        db.close()

    print("\n✅ 완료!")
