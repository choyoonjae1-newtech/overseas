from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
import json
from datetime import datetime, timedelta

from core.database import get_db
from core.security import get_current_admin
from models.user import User
from models.scheduler_config import SchedulerConfig
from services.scheduler_service import scheduler_service


router = APIRouter(prefix="/api/scheduler", tags=["scheduler"])


class SchedulerConfigResponse(BaseModel):
    id: int
    country_code: str
    enabled: bool
    interval_hours: int
    keywords: Optional[List[str]]
    last_run_at: Optional[datetime]
    next_run_at: Optional[datetime]
    status: str
    last_error: Optional[str]

    class Config:
        from_attributes = True


class SchedulerConfigUpdate(BaseModel):
    enabled: Optional[bool] = None
    interval_hours: Optional[int] = None
    keywords: Optional[List[str]] = None


class TriggerResponse(BaseModel):
    success: bool
    message: str
    collected_count: Optional[int] = None


@router.get("/configs", response_model=List[SchedulerConfigResponse])
def get_scheduler_configs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """스케줄러 설정 목록 조회 (관리자 전용)"""
    configs = db.query(SchedulerConfig).all()

    # keywords JSON 파싱
    result = []
    for config in configs:
        config_dict = {
            "id": config.id,
            "country_code": config.country_code,
            "enabled": config.enabled,
            "interval_hours": config.interval_hours,
            "keywords": json.loads(config.keywords) if config.keywords else [],
            "last_run_at": config.last_run_at,
            "next_run_at": config.next_run_at,
            "status": config.status,
            "last_error": config.last_error
        }
        result.append(SchedulerConfigResponse(**config_dict))

    return result


@router.put("/configs/{config_id}", response_model=SchedulerConfigResponse)
def update_scheduler_config(
    config_id: int,
    update_data: SchedulerConfigUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """스케줄러 설정 수정 (관리자 전용)"""
    config = db.query(SchedulerConfig).filter(SchedulerConfig.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="Config not found")

    # 업데이트
    if update_data.enabled is not None:
        config.enabled = update_data.enabled

        if update_data.enabled:
            # 활성화: 스케줄러에 작업 추가
            interval = update_data.interval_hours if update_data.interval_hours else config.interval_hours
            scheduler_service.add_job(config.country_code, interval)
            config.next_run_at = datetime.utcnow() + timedelta(hours=interval)
        else:
            # 비활성화: 스케줄러에서 작업 제거
            scheduler_service.remove_job(config.country_code)
            config.next_run_at = None

    if update_data.interval_hours is not None:
        config.interval_hours = update_data.interval_hours
        if config.enabled:
            # 간격 변경 시 스케줄러 재설정
            scheduler_service.add_job(config.country_code, update_data.interval_hours)
            config.next_run_at = datetime.utcnow() + timedelta(hours=update_data.interval_hours)

    if update_data.keywords is not None:
        config.keywords = json.dumps(update_data.keywords, ensure_ascii=False)

    db.commit()
    db.refresh(config)

    return SchedulerConfigResponse(
        id=config.id,
        country_code=config.country_code,
        enabled=config.enabled,
        interval_hours=config.interval_hours,
        keywords=json.loads(config.keywords) if config.keywords else [],
        last_run_at=config.last_run_at,
        next_run_at=config.next_run_at,
        status=config.status,
        last_error=config.last_error
    )


@router.post("/trigger/{country_code}", response_model=TriggerResponse)
async def trigger_manual_collection(
    country_code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """수동으로 뉴스 수집 트리거 (관리자 전용)"""
    config = db.query(SchedulerConfig).filter(
        SchedulerConfig.country_code == country_code
    ).first()

    if not config:
        raise HTTPException(status_code=404, detail="Config not found")

    result = scheduler_service.trigger_manual_collection(country_code)

    if result["success"]:
        return TriggerResponse(
            success=True,
            message=f"{country_code} 뉴스 수집 완료",
            collected_count=result.get("collected_count", 0)
        )
    else:
        raise HTTPException(
            status_code=500,
            detail=result.get("error", "Collection failed")
        )


@router.post("/trigger-indicators", response_model=TriggerResponse)
async def trigger_indicators_collection(
    current_user: User = Depends(get_current_admin)
):
    """수동으로 경제 지표 수집 트리거 (관리자 전용)"""
    result = scheduler_service.trigger_manual_indicators_collection()

    if result["success"]:
        return TriggerResponse(
            success=True,
            message="경제 지표 수집 완료"
        )
    else:
        raise HTTPException(
            status_code=500,
            detail=result.get("error", "Indicators collection failed")
        )
