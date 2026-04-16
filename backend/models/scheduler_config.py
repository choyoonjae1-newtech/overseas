from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from core.database import Base


class SchedulerConfig(Base):
    """스케줄러 설정 모델"""
    __tablename__ = "scheduler_configs"

    id = Column(Integer, primary_key=True, index=True)
    country_code = Column(String(10), unique=True, nullable=False)  # MM, ID
    enabled = Column(Boolean, default=True, nullable=False)
    interval_hours = Column(Integer, default=3, nullable=False)  # 수집 간격 (시간)
    keywords = Column(Text, nullable=True)  # JSON 형태로 저장
    last_run_at = Column(DateTime, nullable=True)
    next_run_at = Column(DateTime, nullable=True)
    status = Column(String(20), default="idle")  # idle, running, error
    last_error = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
