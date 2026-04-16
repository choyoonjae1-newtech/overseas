from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from core.database import get_db
from core.security import get_current_user, get_current_admin
from models.news import News
from models.country import Country
from models.user import User

router = APIRouter(prefix="/api", tags=["news"])


class NewsCreate(BaseModel):
    country_code: str
    title: str
    content: Optional[str] = None
    source: Optional[str] = None
    url: Optional[str] = None
    category: Optional[str] = "other"
    published_at: Optional[datetime] = None


class NewsUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    source: Optional[str] = None
    url: Optional[str] = None
    category: Optional[str] = None


class NewsResponse(BaseModel):
    id: int
    country_code: str
    title: str
    content: Optional[str]
    source: Optional[str]
    url: Optional[str]
    category: Optional[str]
    published_at: Optional[str]
    created_at: str
    source_type: str

    class Config:
        from_attributes = True


@router.get("/countries/{country_code}/news", response_model=List[NewsResponse])
def get_news_by_country(
    country_code: str,
    category: Optional[str] = Query(None),
    limit: int = Query(50, le=100),
    offset: int = Query(0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """국가별 뉴스 목록 조회"""
    # 국가 확인
    country = db.query(Country).filter(Country.code == country_code).first()
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    # 뉴스 조회
    query = db.query(News).filter(News.country_id == country.id)

    if category:
        query = query.filter(News.category == category)

    query = query.order_by(News.published_at.desc(), News.created_at.desc())
    news_list = query.offset(offset).limit(limit).all()

    return [
        {
            "id": n.id,
            "country_code": country_code,
            "title": n.title,
            "content": n.content,
            "source": n.source,
            "url": n.url,
            "category": n.category,
            "published_at": n.published_at.isoformat() if n.published_at else None,
            "created_at": n.created_at.isoformat() if n.created_at else "",
            "source_type": n.source_type
        }
        for n in news_list
    ]


@router.get("/news/{news_id}", response_model=NewsResponse)
def get_news_detail(
    news_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """뉴스 상세 조회"""
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")

    country = db.query(Country).filter(Country.id == news.country_id).first()

    return {
        "id": news.id,
        "country_code": country.code if country else "",
        "title": news.title,
        "content": news.content,
        "source": news.source,
        "url": news.url,
        "category": news.category,
        "published_at": news.published_at.isoformat() if news.published_at else None,
        "created_at": news.created_at.isoformat() if news.created_at else "",
        "source_type": news.source_type
    }


@router.post("/news", response_model=NewsResponse)
def create_news(
    request: NewsCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """뉴스 추가 (관리자 전용)"""
    # 국가 확인
    country = db.query(Country).filter(Country.code == request.country_code).first()
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    # 뉴스 생성
    new_news = News(
        country_id=country.id,
        title=request.title,
        content=request.content,
        source=request.source,
        url=request.url,
        category=request.category,
        published_at=request.published_at or datetime.utcnow(),
        created_by=admin.id,
        source_type="manual"
    )

    db.add(new_news)
    db.commit()
    db.refresh(new_news)

    return {
        "id": new_news.id,
        "country_code": request.country_code,
        "title": new_news.title,
        "content": new_news.content,
        "source": new_news.source,
        "url": new_news.url,
        "category": new_news.category,
        "published_at": new_news.published_at.isoformat() if new_news.published_at else None,
        "created_at": new_news.created_at.isoformat() if new_news.created_at else "",
        "source_type": new_news.source_type
    }


@router.put("/news/{news_id}", response_model=NewsResponse)
def update_news(
    news_id: int,
    request: NewsUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """뉴스 수정 (관리자 전용)"""
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")

    # 수정
    if request.title is not None:
        news.title = request.title
    if request.content is not None:
        news.content = request.content
    if request.source is not None:
        news.source = request.source
    if request.url is not None:
        news.url = request.url
    if request.category is not None:
        news.category = request.category

    db.commit()
    db.refresh(news)

    country = db.query(Country).filter(Country.id == news.country_id).first()

    return {
        "id": news.id,
        "country_code": country.code if country else "",
        "title": news.title,
        "content": news.content,
        "source": news.source,
        "url": news.url,
        "category": news.category,
        "published_at": news.published_at.isoformat() if news.published_at else None,
        "created_at": news.created_at.isoformat() if news.created_at else "",
        "source_type": news.source_type
    }


@router.delete("/news/{news_id}")
def delete_news(
    news_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """뉴스 삭제 (관리자 전용)"""
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")

    db.delete(news)
    db.commit()

    return {"message": "News deleted successfully"}
