from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base


class EconomicIndicator(Base):
    """거시경제 지표 모델"""
    __tablename__ = "economic_indicators"
    __table_args__ = (
        UniqueConstraint('country_id', 'indicator_type', 'period', name='uq_indicator_country_type_period'),
    )

    id = Column(Integer, primary_key=True, index=True)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    indicator_type = Column(String(50), nullable=False)  # exchange_rate, gdp_growth, inflation, interest_rate, forex_reserve
    value = Column(Float, nullable=False)
    unit = Column(String(20), nullable=True)  # USD, %, billion USD 등
    period = Column(String(20), nullable=False)  # 2026-Q1, 2026-01 등
    recorded_at = Column(DateTime, nullable=False)  # 지표 기준일
    source = Column(String(200), nullable=True)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    country = relationship("Country", back_populates="indicators")
