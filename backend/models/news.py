from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from core.database import Base


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=True)
    source = Column(String(200), nullable=True)  # 출처
    url = Column(Text, nullable=True)
    category = Column(String(50), nullable=True, index=True)  # 'regulation', 'geopolitical', 'economic', 'other'
    published_at = Column(DateTime(timezone=True), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # 수동 입력 시
    source_type = Column(String(20), nullable=False, index=True)  # 'api', 'crawl', 'manual'

    # 중복 방지: 같은 국가의 같은 제목의 뉴스는 하나만 유지
    __table_args__ = (
        UniqueConstraint('country_id', 'title', name='uq_news_country_title'),
    )

    def __repr__(self):
        return f"<News(id={self.id}, title='{self.title[:30]}...', source_type='{self.source_type}')>"
