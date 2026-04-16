# 🔧 GitHub 저장소 검색 안 될 때 해결 방법

## 문제: Railway/Vercel에서 저장소가 검색되지 않음

---

## ✅ 해결 방법 1: GitHub 앱 권한 부여 (권장)

### Railway에서:

1. **Railway 대시보드** → "New Project"
2. "Deploy from GitHub repo" 클릭
3. **"Configure GitHub App"** 링크 클릭
4. GitHub 페이지로 이동
5. **"Repository access"** 섹션에서:
   - "All repositories" 선택 (또는)
   - "Only select repositories" → **overseas** 선택
6. **"Save"** 클릭
7. Railway로 돌아가기
8. 새로고침하면 저장소 표시됨

### Vercel에서:

1. **Vercel 대시보드** → "Add New" → "Project"
2. **"Adjust GitHub App Permissions"** 클릭
3. GitHub 페이지로 이동
4. **"Repository access"** 섹션에서:
   - "All repositories" 선택 (또는)
   - "Only select repositories" → **overseas** 선택
5. **"Save"** 클릭
6. Vercel로 돌아가기
7. 저장소가 목록에 표시됨

---

## ✅ 해결 방법 2: 저장소를 Public으로 변경

### GitHub에서:

1. https://github.com/choyoonjae1-newtech/overseas 접속
2. **Settings** 탭 클릭
3. 맨 아래 **"Danger Zone"** 섹션
4. **"Change visibility"** 클릭
5. **"Make public"** 선택
6. 저장소 이름 입력하여 확인

**장점**: Railway/Vercel에서 바로 검색됨
**단점**: 코드가 공개됨 (민감한 정보는 환경변수로 관리하므로 안전)

---

## ✅ 해결 방법 3: 직접 URL로 임포트

### Railway:

현재 Railway는 GitHub 앱 권한 필요 (방법 1 사용)

### Vercel:

1. 프로젝트 대시보드
2. **Import Git Repository** 섹션
3. 저장소 URL 직접 입력:
   ```
   https://github.com/choyoonjae1-newtech/overseas
   ```
4. Import 클릭

---

## 🔍 현재 저장소 상태 확인

**저장소 URL**: https://github.com/choyoonjae1-newtech/overseas

**확인 방법**:
1. 위 URL 브라우저에서 열기
2. 로그인 필요하면 → Private 저장소
3. 바로 보이면 → Public 저장소

---

## 💡 권장 순서

1. **먼저 방법 1 시도** (GitHub 앱 권한)
   - 가장 간단하고 안전
   - Private 저장소 유지 가능

2. **안 되면 방법 2** (Public 전환)
   - 즉시 해결
   - 환경변수는 여전히 안전

3. **Vercel만 방법 3** (직접 URL)
   - Railway는 앱 권한 필수

---

## 🎯 빠른 해결 (Public 전환)

**GitHub에서 1분 안에 해결:**

```
1. https://github.com/choyoonjae1-newtech/overseas/settings
2. 맨 아래 "Change visibility" 클릭
3. "Make public" 선택
4. "overseas" 입력하여 확인
5. Railway/Vercel에서 새로고침
```

**완료!** 이제 저장소가 검색됩니다.

---

## 🔐 보안 참고사항

### 이미 안전하게 구성됨:

- ✅ `.gitignore`에 `.env` 파일 제외
- ✅ API 키는 환경변수로 관리
- ✅ 데이터베이스 파일 제외
- ✅ SECRET_KEY는 Railway에서 설정

### Public 저장소여도 안전:

- API 키는 Railway/Vercel 환경변수에만 있음
- 코드만 공개, 민감 정보는 비공개
- 오픈소스처럼 운영 가능

---

**저장소가 검색되지 않으면 위 방법 중 하나를 선택하세요!**
