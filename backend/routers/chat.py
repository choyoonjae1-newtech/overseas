"""
Claude 기반 채팅 API
- 해외사업 모니터링 전문 AI 어시스턴트
- 실시간 질의응답
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from core.security import get_current_user
from models import User
import logging
from anthropic import Anthropic
from core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatMessage(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str


class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []


class ChatResponse(BaseModel):
    response: str
    usage: Optional[dict] = None


def get_claude_client():
    """Claude API 클라이언트 생성"""
    api_key = getattr(settings, 'CLAUDE_API_KEY', None)
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="Claude API가 설정되지 않았습니다. 관리자에게 문의하세요."
        )
    return Anthropic(api_key=api_key)


SYSTEM_PROMPT = """당신은 JB우리캐피탈의 해외사업 모니터링 전문 AI 어시스턴트입니다.

**역할 및 전문 분야:**
- 미얀마와 인도네시아의 금융 시장 전문가
- 해외 금융규제 및 정책 분석가
- 지정학적 리스크 평가 전문가
- 경제 지표 해석 및 비즈니스 인사이트 제공

**제공 서비스:**
1. 금융규제 및 정책 변화 해석
2. 경제 지표 분석 및 전망
3. 지정학적 리스크 평가
4. 투자 및 운영 전략 조언
5. 국가별 시장 동향 분석
6. 리스크 관리 권장사항

**대화 원칙:**
- 전문적이고 정확한 정보 제공
- 금융 전문 용어를 쉽게 설명
- 구체적인 데이터와 근거 제시
- 리스크와 기회를 균형있게 평가
- 한국어로 명확하게 소통

**주의사항:**
- 투자 결정은 항상 전문가와 상담 권장
- 불확실한 정보는 명확히 표시
- 법적/규제적 조언은 전문가 확인 필요

사용자의 질문에 친절하고 전문적으로 답변해주세요."""


@router.post("/message", response_model=ChatResponse)
async def chat_message(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Claude 채팅 메시지 전송
    """
    try:
        client = get_claude_client()

        # 대화 히스토리 구성
        messages = []

        # 이전 대화 히스토리 추가
        for msg in request.history[-10:]:  # 최근 10개 메시지만 유지
            messages.append({
                "role": msg.role,
                "content": msg.content
            })

        # 현재 사용자 메시지 추가
        messages.append({
            "role": "user",
            "content": request.message
        })

        # Claude API 호출
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            temperature=0.7,
            system=SYSTEM_PROMPT,
            messages=messages
        )

        # 응답 추출
        assistant_message = response.content[0].text

        # 사용량 정보
        usage = {
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens
        }

        logger.info(f"✅ 채팅 응답 생성 완료 (사용자: {current_user.username}, 토큰: {usage['input_tokens']}+{usage['output_tokens']})")

        return ChatResponse(
            response=assistant_message,
            usage=usage
        )

    except Exception as e:
        logger.error(f"❌ 채팅 오류: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"채팅 서비스 오류: {str(e)}"
        )


@router.get("/status")
async def chat_status(current_user: User = Depends(get_current_user)):
    """
    채팅 서비스 상태 확인
    """
    try:
        api_key = getattr(settings, 'CLAUDE_API_KEY', None)

        return {
            "available": bool(api_key),
            "model": "claude-3-5-sonnet-20241022",
            "features": [
                "금융규제 분석",
                "경제 지표 해석",
                "리스크 평가",
                "시장 동향 분석",
                "전략 조언"
            ]
        }
    except Exception as e:
        logger.error(f"❌ 상태 확인 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))
