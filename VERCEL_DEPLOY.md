# Vercel 프론트엔드 배포 가이드

## 📋 준비사항
- ✅ Railway 백엔드 URL: `https://web-production-76e97.up.railway.app`
- ✅ GitHub 리포지토리: `https://github.com/choyoonjae1-newtech/overseas`
- ✅ Vercel 계정 (GitHub로 로그인)

---

## 🚀 Vercel 배포 단계

### 1단계: Vercel 접속 및 프로젝트 생성

1. **Vercel 웹사이트 접속**
   - https://vercel.com 접속
   - **"Sign Up"** 또는 **"Login"** (GitHub 계정 사용)

2. **새 프로젝트 생성**
   - 대시보드에서 **"Add New..." → "Project"** 클릭
   - **"Import Git Repository"** 섹션에서
   - GitHub 리포지토리 검색: `overseas`
   - **"Import"** 클릭

---

### 2단계: 프로젝트 설정

**Configure Project** 화면에서:

#### Framework Preset
- **Framework Preset:** Vite (자동 감지됨)

#### Build & Development Settings
- **Root Directory:** `frontend` (중요!)
  - "Edit" 클릭 → `frontend` 입력

#### Build Command
```bash
npm run build
```

#### Output Directory
```bash
dist
```

#### Install Command
```bash
npm install
```

---

### 3단계: 환경 변수 설정

**Environment Variables** 섹션에서:

1. **"Add Environment Variable"** 클릭
2. 다음 변수 추가:

```
Key: VITE_API_URL
Value: https://web-production-76e97.up.railway.app
```

**Environment:** Production, Preview, Development 모두 체크

---

### 4단계: 배포 시작

1. 모든 설정 확인
2. **"Deploy"** 버튼 클릭
3. 배포 진행 상황 확인 (2-3분 소요)

---

## ✅ 배포 완료 후

### Vercel URL 확인
- 배포 완료 후 Vercel이 자동으로 도메인 생성
- 예: `https://overseas-abc123.vercel.app`
- 또는 `https://your-project.vercel.app`

### Railway CORS 설정 업데이트 필요!
Vercel URL을 받은 후 Railway에서 CORS 설정을 업데이트해야 합니다:

1. **Railway 대시보드** → 백엔드 서비스 → **Variables**
2. **CORS_ORIGINS** 변수 수정:
   ```
   https://overseas-abc123.vercel.app,http://localhost:5173,http://localhost:3000
   ```
   (Vercel URL을 앞에 추가)
3. Railway가 자동으로 재배포됩니다

---

## 🧪 배포 테스트

1. **Vercel URL 접속**
   - 예: `https://overseas-abc123.vercel.app`

2. **회원가입 테스트**
   - 새 계정으로 회원가입
   - "관리자 승인 대기" 메시지 확인

3. **관리자 로그인**
   - Username: `admin`
   - Password: `whdbswo12#`

4. **사용자 승인**
   - 관리자 대시보드에서 새 사용자 승인

5. **기능 테스트**
   - 미얀마/인도네시아 버튼 클릭
   - 뉴스 목록 확인
   - 경제 지표 확인
   - 캘린더 확인

---

## 🔧 문제 해결

### 빌드 실패 시
- Vercel 대시보드 → Deployments → 실패한 배포 클릭 → 로그 확인
- `npm install` 오류: `package.json` 확인
- TypeScript 오류: 코드 수정 후 다시 배포

### API 연결 실패 시
- 브라우저 콘솔(F12)에서 에러 확인
- CORS 에러: Railway CORS_ORIGINS에 Vercel URL 추가했는지 확인
- Network 에러: Railway 백엔드가 실행 중인지 확인

### Railway 백엔드 확인
```bash
# 브라우저에서 Railway API 테스트
https://web-production-76e97.up.railway.app/docs
```

---

## 📝 다음 단계

배포 완료 후:
1. ✅ Vercel URL 확인
2. ✅ Railway CORS 업데이트
3. ✅ 전체 기능 테스트
4. ✅ 관리자로 초기 데이터 입력
   - 미얀마/인도네시아 뉴스 수동 추가
   - 경제 지표 수집 트리거
   - 주요 일정 입력

---

## 🎉 완료!

배포가 완료되면:
- **프론트엔드:** https://your-project.vercel.app
- **백엔드:** https://web-production-76e97.up.railway.app
- **API 문서:** https://web-production-76e97.up.railway.app/docs

모든 서비스가 온라인 상태입니다! 🚀
