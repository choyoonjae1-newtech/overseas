from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from pydantic import BaseModel
from typing import List
from core.database import get_db
from core.security import get_current_admin
from models.user import User

router = APIRouter(prefix="/api/users", tags=["users"])


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    status: str
    created_at: str

    class Config:
        from_attributes = True


@router.get("/pending", response_model=List[UserResponse])
def get_pending_users(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """승인 대기 중인 사용자 목록 (관리자 전용)"""
    pending_users = db.query(User).filter(User.status == "pending").all()
    return [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "role": u.role,
            "status": u.status,
            "created_at": u.created_at.isoformat() if u.created_at else ""
        }
        for u in pending_users
    ]


@router.put("/{user_id}/approve")
def approve_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """사용자 승인 (관리자 전용)"""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not in pending status"
        )

    user.status = "approved"
    user.approved_at = func.now()
    user.approved_by = admin.id

    db.commit()

    return {"message": f"User {user.username} approved successfully"}


@router.put("/{user_id}/reject")
def reject_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """사용자 거절 (관리자 전용)"""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not in pending status"
        )

    user.status = "rejected"
    db.commit()

    return {"message": f"User {user.username} rejected"}
