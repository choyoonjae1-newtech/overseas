# 🚀 지금 바로 배포하기

## ✅ 준비 완료
- [x] GitHub 업로드: https://github.com/choyoonjae1-newtech/overseas
- [x] SECRET_KEY 생성 완료
- [x] 환경변수 준비 완료

---

## 📋 배포 단계

### 1️⃣ Railway 백엔드 배포 (5분)

**1. Railway 접속 및 프로젝트 생성**
```
1) https://railway.app 접속
2) "Login with GitHub" 클릭
3) "New Project" 클릭
4) "Deploy from GitHub repo" 선택
5) "overseas" 저장소 클릭
```

**2. PostgreSQL 데이터베이스 추가**
```
1) 프로젝트 대시보드에서 "+ New" 클릭
2) "Database" → "Add PostgreSQL" 선택
3) 자동으로 연결됨
```

**3. 환경변수 설정**
```
1) 백엔드 서비스 클릭 → "Variables" 탭
2) "New Variable" 클릭하여 아래 변수들 추가:
```

**복사해서 사용:**
```env
SECRET_KEY=THYW2RmYLYJwYD7OKlONdv4FakE0upQcB08ccO7ssY3vkgFOm_zroAR4PpnEsih-a7WfntFOeUOqWcqIIlgT7g
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
NEWSAPI_KEY=52f1437842d34a1fa605b53e55756206
CALENDARIFIC_API_KEY=gHEWujx7hZ5k0lFuwEtaDnxgMSAwAWdo
CORS_ORIGINS=https://overseas.vercel.app
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@jbwooricapital.com
ADMIN_PASSWORD=whdbswo12#
```

**4. 배포 URL 확인**
```
1) "Settings" 탭 클릭
2) "Domains" 섹션에서 "Generate Domain" 클릭
3) 생성된 URL 복사 (예: overseas-production.up.railway.app)
```

---

### 2️⃣ Vercel 프론트엔드 배포 (3분)

**1. Vercel 접속 및 프로젝트 생성**
```
1) https://vercel.com 접속
2) "Login with GitHub" 클릭
3) "Add New..." → "Project" 클릭
4) "overseas" 저장소에서 "Import" 클릭
```

**2. 프로젝트 설정**
```
Framework Preset: Vite
Root Directory: frontend  ⚠️ 반드시 입력!
Build Command: npm run build (자동)
Output Directory: dist (자동)
Install Command: npm install (자동)
```

**3. 환경변수 설정**
```
Environment Variables 섹션에서:
```

**복사해서 사용:**
```
Name: VITE_API_URL
Value: https://overseas-production.up.railway.app
```
(Railway에서 복사한 URL 사용)

**4. 배포**
```
1) "Deploy" 버튼 클릭
2) 3-5분 대기
3) 배포 완료 후 URL 확인 (예: overseas.vercel.app)
```

---

### 3️⃣ CORS 업데이트 (1분)

**Railway 돌아가기:**
```
1) Railway 대시보드 → 백엔드 서비스
2) "Variables" 탭
3) CORS_ORIGINS 찾기
4) 값을 Vercel URL로 변경
   예: https://overseas.vercel.app
5) 자동 재배포 (1-2분)
```

---

### 4️⃣ 초기 데이터 로드 (2분)

**Railway Terminal 사용:**
```
1) Railway → 백엔드 서비스
2) Deploy Logs 오른쪽 상단 "..." 메뉴
3) "View Logs" 클릭
4) "Terminal" 탭 선택
```

**실행할 명령어:**
```bash
cd backend
python services/init_db.py
python services/data_loader.py
python services/init_indicators.py
```

---

## ✅ 배포 완료 확인

### 접속 테스트
1. **백엔드**: https://overseas-production.up.railway.app/health
   - 응답: `{"status":"healthy"}`

2. **프론트엔드**: https://overseas.vercel.app
   - 로그인 페이지 표시 확인

### 로그인 테스트
- **ID**: admin
- **PW**: whdbswo12#

### 기능 확인
- [x] 로그인 성공
- [x] 미얀마/인도네시아 선택
- [x] 뉴스 표시
- [x] 일정 캘린더 표시
- [x] 경제 지표 표시
- [x] 관리자 페이지 접근

---

## 🆘 문제 해결

### Railway 배포 실패
- Deploy Logs 확인
- 환경변수 누락 여부 확인
- PostgreSQL 연결 확인

### Vercel 빌드 실패
- Root Directory가 "frontend"인지 확인
- 환경변수 VITE_API_URL 확인

### CORS 에러
- Railway CORS_ORIGINS에 Vercel URL 추가 확인
- https:// 포함 확인

---

## 📞 다음 단계

배포 완료 후:
1. 팀원들에게 URL 공유
2. 회원가입 테스트
3. 관리자가 사용자 승인
4. 자동 수집 동작 확인

**배포 성공을 기원합니다! 🎉**
