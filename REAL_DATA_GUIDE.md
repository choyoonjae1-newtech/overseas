# 실제 데이터 수집 가이드

## 개요

이 시스템은 이제 **실제 데이터**와 **샘플 데이터**를 명확히 구분하여 관리합니다.

- **실제 데이터**: World Bank API, Exchange Rate API 등 공신력 있는 출처에서 자동 수집
- **샘플 데이터**: 하드코딩된 데모/테스트용 데이터 (⚠️ 프로덕션 사용 비권장)

---

## 🔧 데이터 중복 방지 장치

### 1. 데이터베이스 레벨

`economic_indicators` 테이블에 유니크 제약조건 추가:
```sql
UNIQUE(country_id, indicator_type, period)
```

동일한 국가, 지표 타입, 기간 조합은 중복 저장이 불가능합니다.

### 2. 애플리케이션 레벨

`indicators_collector.py`의 `_save_indicator()` 메서드:
- 신규 데이터: INSERT
- 기존 데이터: UPDATE (자동 업데이트)
- 중복 감지 시: 무시 (로그 기록)

---

## 📊 실제 데이터 수집 방법

### 방법 1: 관리자 대시보드 사용 (권장)

1. 관리자로 로그인 (`admin` / `whdbswo12#`)
2. 관리자 페이지 접속
3. **"실제 경제 지표 수집"** 버튼 클릭
4. 수집 완료 알림 확인

### 방법 2: API 호출

```bash
# 로그인하여 토큰 발급
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "whdbswo12#"}' | jq -r '.access_token')

# 실제 경제 지표 수집
curl -X POST http://localhost:8000/api/admin/collect-real-indicators \
  -H "Authorization: Bearer $TOKEN"
```

### 방법 3: Python 스크립트

```python
import asyncio
from services.indicators_collector import indicators_collector

async def main():
    count = await indicators_collector.collect_all_indicators()
    print(f"수집 완료: {count}개 지표")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 📡 실제 데이터 출처

### 현재 연동된 API

| 지표 | 데이터 출처 | 업데이트 주기 |
|------|------------|-------------|
| GDP 성장률 | World Bank API | 연간 |
| 인플레이션 | World Bank API | 연간 |
| 실업률 | World Bank API | 연간 |
| 수출 | World Bank API | 연간 |
| 수입 | World Bank API | 연간 |
| 외환보유액 | World Bank API | 연간 |
| 무역수지 | World Bank API | 연간 |
| 환율 (MMK, IDR) | Exchange Rate API | 일일 |

### 추가 가능한 데이터 출처 (향후 확장)

- **IMF API**: 더 자세한 경제 지표
- **Bank Indonesia API**: 인도네시아 중앙은행 실시간 데이터
- **FRED API**: 미국 연방준비은행 경제 데이터
- **Trading Economics API** (유료): 광범위한 실시간 데이터

---

## ⚠️ 샘플 데이터 (데모용)

### 언제 사용하나요?

- 개발/테스트 환경
- 데이터 시각화 데모
- API 연동 전 임시 사용

### 사용 방법

```bash
curl -X POST http://localhost:8000/api/admin/populate-sample-indicators \
  -H "Authorization: Bearer $TOKEN"
```

### 주의사항

⚠️ **샘플 데이터는 실제 데이터가 아닙니다!**

- 2026년 1~4월 데이터로 하드코딩됨
- 실제 경제 상황을 반영하지 않음
- 프로덕션 환경에서 사용 금지
- 업무 담당자에게 보여줄 때는 반드시 실제 데이터 사용

---

## 🚀 배포 환경 설정

### Railway (백엔드) 환경변수

```env
# 필수
DATABASE_URL=postgresql://...  # PostgreSQL 권장 (SQLite는 동시성 문제)
SECRET_KEY=your-secret-key

# 선택 (API 키가 있으면 더 많은 데이터 수집 가능)
WORLDBANK_API_KEY=  # 불필요 (공개 API)
EXCHANGE_RATE_API_KEY=  # 불필요 (무료 tier)
```

### 자동 데이터 수집 (Scheduler)

`init_scheduler.py`에서 자동 수집 설정 가능:

```python
# 매일 오전 9시 실제 데이터 수집
scheduler.add_job(
    indicators_collector.collect_all_indicators,
    'cron',
    hour=9,
    minute=0
)
```

---

## 🔍 데이터 품질 확인

### 1. 중복 확인

```bash
python migrate_add_unique_constraint.py
```

### 2. 데이터 출처 확인

관리자 대시보드에서:
- 각 지표의 `source` 필드 확인
- "World Bank", "Exchange Rate API" 등이 표시되어야 함
- "자동 수집" 노트가 있어야 함

### 3. 수동 데이터 vs 자동 데이터

```sql
-- 자동 수집 데이터
SELECT * FROM economic_indicators WHERE note LIKE '%자동 수집%';

-- 수동 입력 데이터 (샘플)
SELECT * FROM economic_indicators WHERE created_by IS NOT NULL;
```

---

## 📝 실제 데이터로 전환 체크리스트

### 프로덕션 배포 전

- [ ] 기존 샘플 데이터 모두 삭제
  ```bash
  curl -X POST http://localhost:8000/api/admin/collect-real-indicators
  ```

- [ ] 실제 데이터 수집 확인
  - 미얀마 환율: MMK/USD
  - 인도네시아 환율: IDR/USD
  - 양국 GDP, 인플레이션 등

- [ ] 데이터 출처 표시 확인
  - 프론트엔드에서 "출처: World Bank" 등이 보이는지 확인

- [ ] 최종 업데이트 시간 확인
  - "최종 업데이트" 타임스탬프가 최근인지 확인

- [ ] 중복 데이터 없음 확인
  ```bash
  python migrate_add_unique_constraint.py
  ```

### 업무 담당자 피드백 세션 전

- [ ] **샘플 데이터 완전 제거**
- [ ] 실제 데이터로만 채워진 상태 확인
- [ ] 모든 지표에 실제 출처 표시 확인
- [ ] 데이터 업데이트 시간이 최신인지 확인

---

## 🆘 문제 해결

### Q: "중복 데이터" 오류가 발생합니다

```bash
# 마이그레이션 스크립트 실행하여 중복 제거
python migrate_add_unique_constraint.py
```

### Q: 일부 지표만 수집됩니다

- World Bank API는 연간 데이터만 제공 (월별 데이터 없음)
- 월별 데이터가 필요한 경우 다른 API 추가 필요
- 또는 수동 입력 사용

### Q: 환율 데이터가 업데이트되지 않습니다

- Exchange Rate API는 일일 업데이트
- API 요청 제한 확인 (무료 tier: 1500 requests/month)
- 로그 확인: `logger.info` 메시지 확인

### Q: 샘플 데이터와 실제 데이터가 섞여 있습니다

```bash
# 모든 경제 지표 삭제 후 실제 데이터만 수집
curl -X DELETE http://localhost:8000/api/admin/indicators  # 삭제 endpoint 필요
curl -X POST http://localhost:8000/api/admin/collect-real-indicators
```

---

## 🎯 다음 단계

### 즉시 가능한 개선

1. **더 많은 API 연동**
   - IMF API (GDP, 인플레이션 상세 데이터)
   - Bank Indonesia API (기준금리, 외환보유액)

2. **웹 스크래핑 추가**
   - Myanmar Central Bank 웹사이트
   - OJK (Indonesia) 공시 페이지

3. **자동화 강화**
   - 매일 자동 데이터 업데이트
   - 데이터 이상 감지 알림

### 중장기 개선

1. **데이터 검증**
   - 이상치 탐지 (급격한 변화 감지)
   - 데이터 소스 간 교차 검증

2. **데이터 시각화**
   - 시계열 차트 (과거 데이터 트렌드)
   - 국가 간 비교 차트

3. **AI 분석**
   - Claude API 연동하여 경제 지표 자동 해석
   - 리스크 평가 및 인사이트 생성

---

**작성일**: 2026-04-16
**작성자**: Claude (AI Assistant)
**문의**: 프로젝트 관리자에게 연락하세요
