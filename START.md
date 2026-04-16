# 🚀 AX Oversea 시작 가이드

## 빠른 시작

### 1. 백엔드 서버 실행

```bash
cd /Users/cho/ai-platform/ax_oversea/backend
source venv/bin/activate
uvicorn main:app --reload
```

백엔드 서버: http://localhost:8000
API 문서: http://localhost:8000/docs

### 2. 프론트엔드 서버 실행 (새 터미널)

```bash
cd /Users/cho/ai-platform/ax_oversea/frontend
npm run dev
```

프론트엔드: http://localhost:5173

## 관리자 로그인 정보

- **Username**: `admin`
- **Password**: `whdbswo12#`

## 테스트 시나리오

### 1단계: 일반 사용자 회원가입
1. http://localhost:5173 접속
2. "회원가입" 클릭
3. 사용자명, 이메일, 비밀번호 입력
4. "관리자 승인 대기" 메시지 확인

### 2단계: 관리자 승인
1. 관리자로 로그인 (admin / whdbswo12#)
2. "관리자 페이지" 버튼 클릭
3. "사용자 관리" 탭에서 승인 대기 목록 확인
4. "승인" 버튼 클릭

### 3단계: 일반 사용자 로그인
1. 로그아웃 후 일반 사용자로 로그인
2. 메인 페이지에서 미얀마 또는 인도네시아 선택
3. 주요 소식 및 일정 확인

### 4단계: 관리자 뉴스 추가
1. 관리자로 로그인
2. "관리자 페이지" → "뉴스 관리"
3. 뉴스 수동 추가
4. 국가 대시보드에서 추가된 뉴스 확인

## 데이터베이스 초기화 (필요시)

```bash
cd /Users/cho/ai-platform/ax_oversea/backend
rm ax_oversea.db
source venv/bin/activate
python init_db.py
```

## 샘플 데이터

- **국가**: 미얀마 (MM), 인도네시아 (ID)
- **샘플 뉴스**: 3개
- **샘플 이벤트**: 3개

## API 엔드포인트

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

## 문제 해결

### 포트 충돌
- 백엔드: 8000번 포트 사용 중인 경우 `uvicorn main:app --port 8001`
- 프론트엔드: 5173번 포트 사용 중인 경우 `npm run dev -- --port 3000`

### CORS 오류
- backend/.env에서 CORS_ORIGINS 확인

### 데이터베이스 오류
- ax_oversea.db 파일 삭제 후 init_db.py 재실행

## 다음 단계

1. **뉴스 API 통합**: NewsAPI 또는 GNews API 키 발급 후 .env에 추가
2. **공휴일 API**: Calendarific API 키 발급
3. **크롤링 구현**: services/news_crawler.py에 크롤링 로직 추가
4. **배포**: Vercel (프론트) + Railway (백엔드)
