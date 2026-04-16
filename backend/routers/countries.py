from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from core.database import get_db
from models.country import Country

router = APIRouter(prefix="/api/countries", tags=["countries"])


class CountryResponse(BaseModel):
    id: int
    code: str
    name_en: str
    name_ko: str
    flag_emoji: Optional[str]

    class Config:
        from_attributes = True


@router.get("", response_model=List[CountryResponse])
def get_countries(db: Session = Depends(get_db)):
    """국가 목록 조회"""
    countries = db.query(Country).all()
    return countries
