"""
스케줄러 설정 초기화
"""
from core.database import SessionLocal
from models.scheduler_config import SchedulerConfig
import json


def init_scheduler_configs():
    """스케줄러 설정 초기화"""
    db = SessionLocal()

    try:
        # 미얀마 설정
        mm_config = db.query(SchedulerConfig).filter(
            SchedulerConfig.country_code == "MM"
        ).first()

        if not mm_config:
            mm_keywords = [
                "financial regulation",
                "central bank",
                "CBM",
                "Myanmar economy",
                "investment",
                "trade"
            ]
            mm_config = SchedulerConfig(
                country_code="MM",
                enabled=True,
                interval_hours=3,
                keywords=json.dumps(mm_keywords, ensure_ascii=False),
                status="idle"
            )
            db.add(mm_config)
            print("✅ 미얀마 스케줄러 설정 생성")

        # 인도네시아 설정
        id_config = db.query(SchedulerConfig).filter(
            SchedulerConfig.country_code == "ID"
        ).first()

        if not id_config:
            id_keywords = [
                "financial regulation",
                "OJK",
                "Bank Indonesia",
                "Indonesian economy",
                "investment",
                "trade"
            ]
            id_config = SchedulerConfig(
                country_code="ID",
                enabled=True,
                interval_hours=3,
                keywords=json.dumps(id_keywords, ensure_ascii=False),
                status="idle"
            )
            db.add(id_config)
            print("✅ 인도네시아 스케줄러 설정 생성")

        db.commit()
        print("🎉 스케줄러 설정 초기화 완료!")

    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("📅 스케줄러 설정 초기화 시작...\n")
    init_scheduler_configs()
