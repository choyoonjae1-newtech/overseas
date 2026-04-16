"""경제 지표 관련 라우터"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user, get_current_admin
from models.user import User
from models.country import Country
from models.indicator import EconomicIndicator
from pydantic import BaseModel
from datetime import datetime


router = APIRouter(prefix="/api/indicators", tags=["indicators"])


# Pydantic 스키마
class IndicatorCreate(BaseModel):
    country_code: str
    indicator_type: str
    value: float
    unit: Optional[str] = None
    period: str
    recorded_at: str  # ISO format datetime string
    source: Optional[str] = None
    note: Optional[str] = None


class IndicatorResponse(BaseModel):
    id: int
    country_id: int
    indicator_type: str
    value: float
    unit: Optional[str]
    period: str
    recorded_at: str
    source: Optional[str]
    note: Optional[str]

    class Config:
        from_attributes = True


@router.get("/countries/{country_code}", response_model=List[IndicatorResponse])
async def get_indicators_by_country(
    country_code: str,
    indicator_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """국가별 경제 지표 조회"""
    # 국가 확인
    country = db.query(Country).filter(Country.code == country_code).first()
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    # 지표 조회
    query = db.query(EconomicIndicator).filter(
        EconomicIndicator.country_id == country.id
    )

    if indicator_type:
        query = query.filter(EconomicIndicator.indicator_type == indicator_type)

    indicators = query.order_by(EconomicIndicator.recorded_at.desc()).all()

    # datetime을 ISO 문자열로 변환
    result = []
    for ind in indicators:
        result.append(IndicatorResponse(
            id=ind.id,
            country_id=ind.country_id,
            indicator_type=ind.indicator_type,
            value=ind.value,
            unit=ind.unit,
            period=ind.period,
            recorded_at=ind.recorded_at.isoformat() if ind.recorded_at else None,
            source=ind.source,
            note=ind.note
        ))

    return result


@router.post("", response_model=IndicatorResponse)
async def create_indicator(
    data: IndicatorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """경제 지표 추가 (관리자 전용)"""
    # 국가 확인
    country = db.query(Country).filter(Country.code == data.country_code).first()
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    # datetime 변환
    try:
        recorded_at = datetime.fromisoformat(data.recorded_at.replace('Z', '+00:00'))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid datetime format")

    # 지표 생성
    indicator = EconomicIndicator(
        country_id=country.id,
        indicator_type=data.indicator_type,
        value=data.value,
        unit=data.unit,
        period=data.period,
        recorded_at=recorded_at,
        source=data.source,
        note=data.note
    )

    db.add(indicator)
    db.commit()
    db.refresh(indicator)

    return IndicatorResponse(
        id=indicator.id,
        country_id=indicator.country_id,
        indicator_type=indicator.indicator_type,
        value=indicator.value,
        unit=indicator.unit,
        period=indicator.period,
        recorded_at=indicator.recorded_at.isoformat(),
        source=indicator.source,
        note=indicator.note
    )


@router.delete("/{indicator_id}")
async def delete_indicator(
    indicator_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """경제 지표 삭제 (관리자 전용)"""
    indicator = db.query(EconomicIndicator).filter(
        EconomicIndicator.id == indicator_id
    ).first()

    if not indicator:
        raise HTTPException(status_code=404, detail="Indicator not found")

    db.delete(indicator)
    db.commit()

    return {"message": "Indicator deleted successfully"}
