# AX Oversea - 해외사업 모니터링 플랫폼

대한민국 여신전문금융회사의 해외사업 관리를 위한 정보 통합 플랫폼입니다.

## 🚀 빠른 시작

### 로컬 개발
```bash
# 백엔드 실행
cd backend
python -m uvicorn main:app --reload

# 프론트엔드 실행 (새 터미널)
cd frontend
npm run dev
```

### 웹 호스팅 배포
```bash
./deploy.sh
```

📘 **빠른 배포 가이드**: [QUICKSTART.md](./QUICKSTART.md) (5분 완성)
📖 **상세 배포 문서**: [DEPLOYMENT.md](./DEPLOYMENT.md)
✅ **설정 요약**: [SETUP_SUMMARY.md](./SETUP_SUMMARY.md)

## 📋 프로젝트 개요

미얀마와 인도네시아 법인을 관리하며, 해당 국가의 정세, 금융기관 규제 변화 등을 실시간으로 모니터링합니다.

### 주요 기능

- 🌍 **국가별 대시보드**: 미얀마, 인도네시아 법인 관리
- 📰 **주요 소식**: 금융 규제, 지정학적 리스크, 경제 뉴스
- 📅 **캘린더**: 공휴일, 규제 일정, 주요 이벤트
- 👥 **사용자 관리**: 관리자 승인 기반 접근 제어
- 🤖 **자동 데이터 수집**: 뉴스 API + 웹 크롤링 + 수동 입력

## 🛠 기술 스택

### Backend
- FastAPI 0.109.0
- SQLite (또는 PostgreSQL)
- SQLAlchemy 2.0.25
- JWT 인증
- APScheduler (자동 크롤링)

### Frontend
- React 19
- TypeScript 5.9
- Vite 7
- React Router
- React Query
- FullCalendar
- TailwindCSS

## 🚀 시작하기

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn

### 백엔드 설정

```bash
cd backend

# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env
# .env 파일을 열어 필요한 값 수정

# 데이터베이스 초기화
python init_db.py

# 서버 실행
uvicorn main:app --reload
```

백엔드 서버: http://localhost:8000
API 문서: http://localhost:8000/docs

### 프론트엔드 설정

```bash
cd frontend

# 의존성 설치
npm install

# 환경변수 설정
cp .env.example .env.local
# .env.local에서 VITE_API_URL 설정

# 개발 서버 실행
npm run dev
```

프론트엔드: http://localhost:5173

## 📖 사용법

### 관리자 계정
- **Username**: admin
- **Password**: whdbswo12#

### 사용자 플로우
1. 회원가입 → 관리자 승인 대기
2. 관리자가 승인 후 로그인 가능
3. 국가 선택 (미얀마/인도네시아)
4. 뉴스 조회 및 캘린더 확인

### 관리자 기능
- 사용자 승인/거절
- 뉴스 수동 추가/수정/삭제
- 크롤링 수동 트리거
- 공휴일 데이터 갱신

## 🗄 데이터베이스 스키마

### users
- id, username, email, hashed_password
- role (admin/user)
- status (pending/approved/rejected)

### countries
- id, code (MM/ID), name_en, name_ko, flag_emoji

### news
- id, country_id, title, content, source, url
- category (regulation/geopolitical/economic/other)
- source_type (api/crawl/manual)

### events
- id, country_id, title, description, event_date
- event_type (holiday/regulation/deadline/other)

## 🌐 API 엔드포인트

### 인증
- `POST /api/auth/register` - 회원가입
- `POST /api/auth/login` - 로그인
- `GET /api/auth/me` - 현재 사용자

### 뉴스
- `GET /api/countries/{code}/news` - 국가별 뉴스
- `POST /api/news` - 뉴스 추가 (관리자)

### 이벤트
- `GET /api/countries/{code}/events` - 국가별 이벤트

### 관리자
- `GET /api/users/pending` - 승인 대기 목록
- `PUT /api/users/{id}/approve` - 승인
- `POST /api/admin/crawl/{code}` - 크롤링 트리거

## 🚢 배포

### Vercel (프론트엔드)
```bash
cd frontend
npm run build
# Vercel CLI 또는 GitHub 연동으로 배포
```

### Railway (백엔드)
```bash
# railway.json 또는 Procfile 사용
# Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

## 📊 데이터 소스

- **NewsAPI**: 글로벌 뉴스 (무료: 100 requests/day)
- **Calendarific API**: 공휴일 (무료: 1000 requests/year)
- **웹 크롤링**:
  - 미얀마 중앙은행 (CBM)
  - 인도네시아 OJK

## 🔒 보안

- JWT 기반 인증 (24시간 토큰)
- bcrypt 비밀번호 해싱
- HTTPS 필수 (프로덕션)
- CORS 설정
- 관리자 승인 기반 사용자 관리

## 📝 라이선스

Private - Internal Use Only

## 👥 개발자

JB우리캐피탈 해외사업팀

---

**Version**: 1.0.0
**Last Updated**: 2026-04-16
