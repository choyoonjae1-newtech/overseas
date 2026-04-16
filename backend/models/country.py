from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, nullable=False, index=True)  # 'MM', 'ID'
    name_en = Column(String(100), nullable=False)
    name_ko = Column(String(100), nullable=False)
    flag_emoji = Column(String(10), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    indicators = relationship("EconomicIndicator", back_populates="country")

    def __repr__(self):
        return f"<Country(code='{self.code}', name_ko='{self.name_ko}')>"
