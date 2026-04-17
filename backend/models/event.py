from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from core.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    event_date = Column(Date, nullable=False, index=True)
    event_type = Column(String(50), nullable=True, index=True)  # 'holiday', 'regulation', 'deadline', 'other'
    source = Column(String(200), nullable=True)
    url = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    # 중복 방지: 같은 국가의 같은 제목의 이벤트가 같은 날짜에 발생하는 경우 하나만 유지
    __table_args__ = (
        UniqueConstraint('country_id', 'title', 'event_date', name='uq_event_country_title_date'),
    )

    def __repr__(self):
        return f"<Event(id={self.id}, title='{self.title[:30]}...', event_type='{self.event_type}')>"
