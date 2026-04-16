"""
APScheduler를 사용한 뉴스 및 경제 지표 수집 스케줄러
"""
import asyncio
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session

from core.database import SessionLocal
from models.scheduler_config import SchedulerConfig
from services.news_collector import NewsCollector
from services.indicators_collector import indicators_collector


class NewsSchedulerService:
    """뉴스 수집 스케줄러 서비스"""

    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        print("📅 뉴스 수집 스케줄러 시작됨")

    def initialize_jobs(self):
        """초기 작업 설정"""
        db = SessionLocal()
        try:
            # 뉴스 수집 작업
            configs = db.query(SchedulerConfig).filter(SchedulerConfig.enabled == True).all()

            for config in configs:
                self.add_job(config.country_code, config.interval_hours)
                print(f"✅ {config.country_code} 스케줄 추가 (간격: {config.interval_hours}시간)")

            # 경제 지표 수집 작업 (매일 오전 9시)
            self.add_indicators_job()
            print(f"✅ 경제 지표 수집 스케줄 추가 (매일 오전 9시)")

        finally:
            db.close()

    def add_job(self, country_code: str, interval_hours: int = 3):
        """특정 국가의 수집 작업 추가"""
        job_id = f"collect_news_{country_code}"

        # 기존 작업 제거
        if self.scheduler.get_job(job_id):
            self.scheduler.remove_job(job_id)

        # 새 작업 추가
        self.scheduler.add_job(
            func=self._collect_news_job,
            trigger=IntervalTrigger(hours=interval_hours),
            id=job_id,
            args=[country_code],
            replace_existing=True,
            next_run_time=datetime.now() + timedelta(seconds=10)  # 10초 후 첫 실행
        )
        print(f"📰 {country_code} 뉴스 수집 작업 추가됨 (간격: {interval_hours}시간)")

    def remove_job(self, country_code: str):
        """작업 제거"""
        job_id = f"collect_news_{country_code}"
        if self.scheduler.get_job(job_id):
            self.scheduler.remove_job(job_id)
            print(f"🗑️ {country_code} 뉴스 수집 작업 제거됨")

    def _collect_news_job(self, country_code: str):
        """뉴스 수집 작업 (동기 래퍼)"""
        print(f"\n🔄 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {country_code} 뉴스 수집 시작...")

        db = SessionLocal()
        try:
            # 상태 업데이트
            config = db.query(SchedulerConfig).filter(
                SchedulerConfig.country_code == country_code
            ).first()

            if config:
                config.status = "running"
                db.commit()

            # 뉴스 수집
            collector = NewsCollector(db)
            result = asyncio.run(collector.collect_news(country_code))

            if result["success"]:
                print(f"✅ {country_code} 뉴스 {result['collected_count']}개 수집 완료")
            else:
                print(f"❌ {country_code} 뉴스 수집 실패: {result.get('error')}")

        except Exception as e:
            print(f"❌ {country_code} 뉴스 수집 중 에러: {e}")
        finally:
            db.close()

    def add_indicators_job(self):
        """경제 지표 수집 작업 추가 (매일 오전 9시)"""
        job_id = "collect_indicators_daily"

        # 기존 작업 제거
        if self.scheduler.get_job(job_id):
            self.scheduler.remove_job(job_id)

        # 매일 오전 9시 실행
        self.scheduler.add_job(
            func=self._collect_indicators_job,
            trigger=CronTrigger(hour=9, minute=0),
            id=job_id,
            replace_existing=True,
            next_run_time=datetime.now() + timedelta(seconds=30)  # 30초 후 첫 실행
        )
        print(f"📊 경제 지표 수집 작업 추가됨 (매일 09:00)")

    def _collect_indicators_job(self):
        """경제 지표 수집 작업"""
        print(f"\n📊 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 경제 지표 수집 시작...")

        try:
            # 비동기 수집 실행
            asyncio.run(indicators_collector.collect_all_indicators())
            print(f"✅ 경제 지표 수집 완료")
        except Exception as e:
            print(f"❌ 경제 지표 수집 중 에러: {e}")

    def trigger_manual_collection(self, country_code: str) -> dict:
        """수동 뉴스 수집 트리거"""
        db = SessionLocal()
        try:
            collector = NewsCollector(db)
            result = asyncio.run(collector.collect_news(country_code))
            return result
        finally:
            db.close()

    def trigger_manual_indicators_collection(self) -> dict:
        """수동 경제 지표 수집 트리거"""
        try:
            asyncio.run(indicators_collector.collect_all_indicators())
            return {"success": True, "message": "경제 지표 수집 완료"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def shutdown(self):
        """스케줄러 종료"""
        self.scheduler.shutdown()
        print("🛑 뉴스 수집 스케줄러 종료됨")


# 싱글톤 인스턴스
scheduler_service = NewsSchedulerService()
