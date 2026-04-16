# ⚡ 빠른 배포 가이드 (5분 완성)

## 📦 준비물
1. GitHub 계정
2. Railway 계정 (https://railway.app - GitHub로 가입)
3. Vercel 계정 (https://vercel.com - GitHub로 가입)

---

## 🚀 배포 3단계

### 1️⃣ GitHub에 코드 업로드 (1분)

```bash
cd /Users/cho/ai-platform/ax_oversea

# 배포 스크립트 실행
./deploy.sh
```

프롬프트에 따라:
- GitHub 저장소 URL 입력
- 푸시 확인

---

### 2️⃣ Railway 백엔드 배포 (2분)

1. https://railway.app → **New Project**
2. **Deploy from GitHub repo** → `ax-oversea` 선택
3. **Add PostgreSQL** 클릭
4. **Variables** 탭에서 환경변수 추가:

```env
SECRET_KEY=임의의_긴_문자열_64자_이상
NEWSAPI_KEY=52f1437842d34a1fa605b53e55756206
CALENDARIFIC_API_KEY=gHEWujx7hZ5k0lFuwEtaDnxgMSAwAWdo
CORS_ORIGINS=https://your-app.vercel.app
ADMIN_USERNAME=admin
ADMIN_PASSWORD=whdbswo12#
```

5. **Settings** → **Generate Domain** 클릭
6. 생성된 URL 복사 (예: `ax-oversea-production.up.railway.app`)

---

### 3️⃣ Vercel 프론트엔드 배포 (2분)

1. https://vercel.com → **Add New** → **Project**
2. `ax-oversea` 저장소 선택
3. **Root Directory**: `frontend` 입력
4. **Environment Variables** 추가:

```env
VITE_API_URL=https://ax-oversea-production.up.railway.app
```
(Railway에서 복사한 URL 사용)

5. **Deploy** 클릭
6. 배포 완료 후 URL 확인 (예: `ax-oversea.vercel.app`)

---

### 4️⃣ CORS 설정 업데이트

Railway 대시보드 → **Variables** → `CORS_ORIGINS` 수정:

```env
CORS_ORIGINS=https://ax-oversea.vercel.app
```

---

### 5️⃣ 초기 데이터 로드

Railway → 백엔드 서비스 → **Terminal**:

```bash
cd backend
python services/init_db.py
python services/data_loader.py
python services/init_indicators.py
```

---

## ✅ 배포 완료!

**프론트엔드**: https://ax-oversea.vercel.app
**백엔드**: https://ax-oversea-production.up.railway.app

**관리자 로그인**:
- ID: `admin`
- PW: `whdbswo12#`

---

## 🔄 코드 수정 후 재배포

```bash
./deploy.sh
```

자동으로:
- 변경사항 커밋
- GitHub 푸시
- Railway/Vercel 자동 배포 (2-5분)

---

## 💰 비용

- **Railway**: 무료 $5/월
- **Vercel**: 무료
- **총 비용**: $0/월

---

## 🆘 문제 해결

### Railway 500 에러
→ Railway Logs 확인 → 환경변수 누락 확인

### Vercel API 연결 안됨
→ `VITE_API_URL` 확인 → Railway CORS 설정 확인

### 데이터 없음
→ Railway Terminal에서 초기 데이터 로드 스크립트 재실행

---

## 📞 상세 가이드

자세한 내용은 [DEPLOYMENT.md](./DEPLOYMENT.md) 참고
