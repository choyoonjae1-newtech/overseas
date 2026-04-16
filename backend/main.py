from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.database import engine, Base
from routers import auth, users, countries, news, events, scheduler, indicators
from services.scheduler_service import scheduler_service

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# FastAPI 앱 생성
app = FastAPI(
    title="AX Oversea API",
    description="해외사업 모니터링 플랫폼 API",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    """서버 시작 시 실행"""
    print("🚀 서버 시작 중...")
    scheduler_service.initialize_jobs()
    print("✅ 스케줄러 초기화 완료")


@app.on_event("shutdown")
async def shutdown_event():
    """서버 종료 시 실행"""
    print("🛑 서버 종료 중...")
    scheduler_service.shutdown()
    print("✅ 스케줄러 종료 완료")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(countries.router)
app.include_router(news.router)
app.include_router(events.router)
app.include_router(scheduler.router)
app.include_router(indicators.router)


@app.get("/")
def root():
    """헬스체크"""
    return {
        "message": "AX Oversea API Server",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health_check():
    """헬스체크"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
