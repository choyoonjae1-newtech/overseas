from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
from core.database import get_db
from core.security import get_current_user, get_current_admin
from models.event import Event
from models.country import Country
from models.user import User

router = APIRouter(prefix="/api", tags=["events"])


class EventCreate(BaseModel):
    country_code: str
    title: str
    description: Optional[str] = None
    event_date: date
    event_type: Optional[str] = "other"
    source: Optional[str] = None
    url: Optional[str] = None


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    event_date: Optional[date] = None
    event_type: Optional[str] = None


class EventResponse(BaseModel):
    id: int
    country_code: str
    title: str
    description: Optional[str]
    event_date: str
    event_type: Optional[str]
    source: Optional[str]
    url: Optional[str]

    class Config:
        from_attributes = True


@router.get("/countries/{country_code}/events", response_model=List[EventResponse])
def get_events_by_country(
    country_code: str,
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    event_type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """국가별 이벤트 목록 조회"""
    # 국가 확인
    country = db.query(Country).filter(Country.code == country_code).first()
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    # 이벤트 조회
    query = db.query(Event).filter(Event.country_id == country.id)

    if start_date:
        query = query.filter(Event.event_date >= start_date)
    if end_date:
        query = query.filter(Event.event_date <= end_date)
    if event_type:
        query = query.filter(Event.event_type == event_type)

    query = query.order_by(Event.event_date)
    events = query.all()

    return [
        {
            "id": e.id,
            "country_code": country_code,
            "title": e.title,
            "description": e.description,
            "event_date": e.event_date.isoformat(),
            "event_type": e.event_type,
            "source": e.source,
            "url": e.url
        }
        for e in events
    ]


@router.post("/events", response_model=EventResponse)
def create_event(
    request: EventCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """이벤트 추가 (관리자 전용)"""
    # 국가 확인
    country = db.query(Country).filter(Country.code == request.country_code).first()
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    # 이벤트 생성
    new_event = Event(
        country_id=country.id,
        title=request.title,
        description=request.description,
        event_date=request.event_date,
        event_type=request.event_type,
        source=request.source,
        url=request.url,
        created_by=admin.id
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return {
        "id": new_event.id,
        "country_code": request.country_code,
        "title": new_event.title,
        "description": new_event.description,
        "event_date": new_event.event_date.isoformat(),
        "event_type": new_event.event_type,
        "source": new_event.source,
        "url": new_event.url
    }


@router.put("/events/{event_id}", response_model=EventResponse)
def update_event(
    event_id: int,
    request: EventUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """이벤트 수정 (관리자 전용)"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # 수정
    if request.title is not None:
        event.title = request.title
    if request.description is not None:
        event.description = request.description
    if request.event_date is not None:
        event.event_date = request.event_date
    if request.event_type is not None:
        event.event_type = request.event_type

    db.commit()
    db.refresh(event)

    country = db.query(Country).filter(Country.id == event.country_id).first()

    return {
        "id": event.id,
        "country_code": country.code if country else "",
        "title": event.title,
        "description": event.description,
        "event_date": event.event_date.isoformat(),
        "event_type": event.event_type,
        "source": event.source,
        "url": event.url
    }


@router.delete("/events/{event_id}")
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """이벤트 삭제 (관리자 전용)"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    db.delete(event)
    db.commit()

    return {"message": "Event deleted successfully"}
