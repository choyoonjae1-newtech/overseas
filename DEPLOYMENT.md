# 🚀 AX Oversea 배포 가이드

JB우리캐피탈 해외사업 모니터링 플랫폼을 웹 호스팅하는 방법입니다.

## 📋 목차
1. [사전 준비](#사전-준비)
2. [백엔드 배포 (Railway)](#백엔드-배포-railway)
3. [프론트엔드 배포 (Vercel)](#프론트엔드-배포-vercel)
4. [초기 데이터 로드](#초기-데이터-로드)
5. [배포 확인](#배포-확인)

---

## 사전 준비

### 1. 필수 계정 생성
- **GitHub 계정** (코드 저장소)
- **Railway 계정** (백엔드 호스팅) - https://railway.app
- **Vercel 계정** (프론트엔드 호스팅) - https://vercel.com

### 2. API 키 발급
- **NewsAPI 키**: https://newsapi.org/register
- **Calendarific 키**: https://calendarific.com/account/api

### 3. GitHub 저장소 생성
```bash
cd /Users/cho/ai-platform/ax_oversea
git init
git add .
git commit -m "Initial commit: AX Oversea platform"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ax-oversea.git
git push -u origin main
```

---

## 백엔드 배포 (Railway)

### 1. Railway 프로젝트 생성
1. https://railway.app 접속 및 로그인
2. "New Project" → "Deploy from GitHub repo" 선택
3. `ax-oversea` 저장소 선택

### 2. 환경 변수 설정
Railway 대시보드 → Variables 탭에서 다음 설정:

```env
# Database (Railway가 자동 제공)
DATABASE_URL=${{Postgres.DATABASE_URL}}

# Security (반드시 변경!)
SECRET_KEY=랜덤_문자열_64자_이상_생성_필요
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# External APIs
NEWSAPI_KEY=your_actual_newsapi_key
CALENDARIFIC_API_KEY=your_actual_calendarific_key

# CORS (나중에 Vercel URL로 업데이트)
CORS_ORIGINS=https://your-app.vercel.app

# Admin Account
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@jbwooricapital.com
ADMIN_PASSWORD=whdbswo12#
```

**SECRET_KEY 생성 방법:**
```python
import secrets
print(secrets.token_urlsafe(64))
```

### 3. PostgreSQL 추가
1. Railway 대시보드 → "New" → "Database" → "PostgreSQL"
2. 자동으로 `DATABASE_URL` 환경변수 생성됨
3. 백엔드 서비스가 자동으로 연결됨

### 4. 배포 설정
Railway는 자동으로 다음 파일들을 감지:
- `Procfile`: 시작 명령어
- `railway.json`: 빌드/배포 설정
- `backend/requirements.txt`: Python 의존성

배포는 자동으로 시작되며, 5-10분 소요됩니다.

### 5. 배포 URL 확인
- Settings → Domains → "Generate Domain"
- 예: `ax-oversea-production.up.railway.app`
- 이 URL을 복사해두세요!

---

## 프론트엔드 배포 (Vercel)

### 1. Vercel 프로젝트 생성
1. https://vercel.com 접속 및 로그인
2. "Add New" → "Project" 선택
3. GitHub에서 `ax-oversea` 저장소 임포트

### 2. 빌드 설정
- **Framework Preset**: Vite
- **Root Directory**: `frontend` (중요!)
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm install`

### 3. 환경 변수 설정
Settings → Environment Variables:

```env
VITE_API_URL=https://ax-oversea-production.up.railway.app
```
(Railway에서 확인한 백엔드 URL 사용)

### 4. 배포
- "Deploy" 버튼 클릭
- 3-5분 후 배포 완료
- 배포 URL 확인: `https://ax-oversea.vercel.app`

### 5. Railway CORS 업데이트
Railway 대시보드 → Variables → `CORS_ORIGINS` 수정:
```env
CORS_ORIGINS=https://ax-oversea.vercel.app
```

서비스가 자동으로 재시작됩니다.

---

## 초기 데이터 로드

### 1. Railway CLI 설치 (선택)
```bash
npm i -g @railway/cli
railway login
railway link
```

### 2. 데이터베이스 초기화
Railway 대시보드 → 백엔드 서비스 → Terminal에서:

```bash
cd backend

# 초기 국가 데이터 로드
python services/init_db.py

# 뉴스/이벤트 데이터 로드
python services/data_loader.py

# 경제 지표 데이터 로드
python services/init_indicators.py
```

또는 로컬에서 Railway DB 연결:
```bash
# Railway DB URL 가져오기
railway variables get DATABASE_URL

# 로컬 .env에 Railway DB URL 설정 후
cd backend
python services/init_db.py
python services/data_loader.py
python services/init_indicators.py
```

---

## 배포 확인

### 1. 백엔드 헬스체크
```bash
curl https://ax-oversea-production.up.railway.app/health
# 응답: {"status":"healthy"}
```

### 2. 프론트엔드 접속
https://ax-oversea.vercel.app 접속

### 3. 로그인 테스트
- 관리자 계정: `admin` / `whdbswo12#`
- 로그인 → 미얀마/인도네시아 선택
- 뉴스, 일정, 경제 지표 확인

### 4. 자동 수집 확인
Railway 대시보드 → Logs에서 확인:
```
📰 MM 뉴스 수집 작업 추가됨 (간격: 3시간)
📰 ID 뉴스 수집 작업 추가됨 (간격: 3시간)
📊 경제 지표 수집 작업 추가됨 (매일 09:00)
```

---

## 🔧 트러블슈팅

### 백엔드 500 에러
1. Railway Logs 확인
2. 환경변수 누락 여부 확인
3. DATABASE_URL 연결 확인

### 프론트엔드 API 에러
1. `VITE_API_URL`이 올바른지 확인
2. Railway CORS 설정 확인
3. 브라우저 콘솔에서 네트워크 탭 확인

### 데이터베이스 연결 실패
```bash
# Railway PostgreSQL 재시작
railway service restart
```

---

## 📊 예상 비용

- **Railway**: 무료 $5 크레딧/월 (약 500시간 실행)
- **Vercel**: 무료 (Hobby 플랜)
- **NewsAPI**: 무료 (100 requests/day)
- **Calendarific**: 무료 (1000 requests/year)

**총 예상 비용: $0/월** (무료 티어 범위 내)

---

## 🔄 업데이트 배포

코드 수정 후:
```bash
git add .
git commit -m "Update: 변경사항 설명"
git push origin main
```

- **Railway**: 자동 배포 (2-5분)
- **Vercel**: 자동 배포 (1-3분)

---

## 🔐 보안 권장사항

1. **SECRET_KEY**: 반드시 강력한 랜덤 문자열 사용
2. **ADMIN_PASSWORD**: 배포 후 즉시 변경
3. **API 키**: 절대 GitHub에 커밋하지 않기
4. **HTTPS**: Railway와 Vercel 모두 자동 제공
5. **환경변수**: Railway/Vercel 대시보드에서만 관리

---

## 📞 지원

문제 발생 시:
1. Railway Logs 확인
2. Vercel Deployment Logs 확인
3. GitHub Issues 생성

**배포 완료 후 팀원들에게 공유:**
- 프론트엔드 URL: `https://ax-oversea.vercel.app`
- 관리자 계정 공유 (보안 메신저 사용)
