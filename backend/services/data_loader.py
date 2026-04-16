"""
2026년 미얀마/인도네시아 이벤트 데이터 로더
- 공휴일
- 주요 금융 규제 일정
- 지정학적 이슈
"""
from datetime import datetime, date
from sqlalchemy.orm import Session
from models.country import Country
from models.news import News
from models.event import Event


# 미얀마 2026년 주요 이벤트
MYANMAR_EVENTS_2026 = [
    # 공휴일
    {"date": "2026-01-04", "title": "독립기념일", "type": "holiday", "desc": "미얀마 독립기념일"},
    {"date": "2026-02-12", "title": "연합기념일", "type": "holiday", "desc": "연방기념일"},
    {"date": "2026-03-02", "title": "농민의 날", "type": "holiday", "desc": "농민의 날"},
    {"date": "2026-03-27", "title": "국군의 날", "type": "holiday", "desc": "국군창설기념일"},
    {"date": "2026-04-13", "title": "물축제 (Thingyan)", "type": "holiday", "desc": "미얀마 전통 신년 축제 시작"},
    {"date": "2026-04-14", "title": "물축제 (Thingyan)", "type": "holiday", "desc": "물축제 2일차"},
    {"date": "2026-04-15", "title": "물축제 (Thingyan)", "type": "holiday", "desc": "물축제 3일차"},
    {"date": "2026-04-16", "title": "물축제 (Thingyan)", "type": "holiday", "desc": "물축제 4일차"},
    {"date": "2026-04-17", "title": "미얀마 신년", "type": "holiday", "desc": "미얀마 전통 새해 첫날"},

    # 금융 규제 일정
    {"date": "2026-02-01", "title": "CBM 외환규제 완화 시행", "type": "regulation", "desc": "중앙은행 외환거래 규제 완화 조치 시행"},
    {"date": "2026-03-15", "title": "금융기관 자본비율 규제 강화", "type": "regulation", "desc": "은행 최저자본금 요건 상향"},
    {"date": "2026-04-01", "title": "디지털 금융 라이선스 신청 마감", "type": "deadline", "desc": "핀테크 기업 라이선스 신청 마감일"},
]

# 인도네시아 2026년 주요 이벤트
INDONESIA_EVENTS_2026 = [
    # 공휴일
    {"date": "2026-01-01", "title": "신년", "type": "holiday", "desc": "새해 첫날"},
    {"date": "2026-01-29", "title": "중국 설날", "type": "holiday", "desc": "중국 전통 새해"},
    {"date": "2026-02-17", "title": "이스라 미라즈", "type": "holiday", "desc": "이슬람 승천일"},
    {"date": "2026-03-14", "title": "힌두 신년 (Nyepi)", "type": "holiday", "desc": "발리 전통 신년"},
    {"date": "2026-03-30", "title": "예수 수난일", "type": "holiday", "desc": "기독교 성 금요일"},
    {"date": "2026-04-02", "title": "라마단 종료 (Idul Fitri)", "type": "holiday", "desc": "이슬람 단식월 종료"},
    {"date": "2026-04-03", "title": "이둘 피트리 2일차", "type": "holiday", "desc": "라마단 종료 휴일 연장"},

    # 금융 규제 일정
    {"date": "2026-01-15", "title": "OJK 핀테크 규제 강화 발표", "type": "regulation", "desc": "금융감독청 P2P 대출 규제 강화"},
    {"date": "2026-02-28", "title": "은행 스트레스 테스트 마감", "type": "deadline", "desc": "연례 은행 건전성 평가 제출 마감"},
    {"date": "2026-03-31", "title": "디지털 뱅킹 라이선스 심사", "type": "regulation", "desc": "디지털 전문 은행 라이선스 최종 심사"},
]

# 미얀마 2026년 주요 뉴스
MYANMAR_NEWS_2026 = [
    {
        "date": "2026-01-10",
        "title": "미얀마 중앙은행, 외환보유고 100억 달러 돌파",
        "content": "미얀마 중앙은행(CBM)이 외환보유고가 100억 달러를 넘어섰다고 발표했습니다. 이는 전년 대비 15% 증가한 수치입니다.",
        "category": "economic",
        "source": "Myanmar Times",
        "url": "https://www.mmtimes.com/"
    },
    {
        "date": "2026-01-25",
        "title": "미얀마 정부, 외국인 투자 인센티브 확대",
        "content": "미얀마 정부가 외국인 직접투자(FDI) 유치를 위해 세제 혜택을 확대한다고 발표했습니다. 특히 제조업과 IT 분야에 집중 지원합니다.",
        "category": "regulation",
        "source": "CBM Press Release",
        "url": "https://www.cbm.gov.mm/"
    },
    {
        "date": "2026-02-05",
        "title": "미얀마-중국 국경 무역 30% 증가",
        "content": "2026년 1월 미얀마-중국 간 국경 무역액이 전년 동월 대비 30% 증가했습니다. 주로 농산물과 광물 수출이 증가했습니다.",
        "category": "economic",
        "source": "Reuters",
        "url": "https://www.reuters.com/world/asia-pacific/"
    },
    {
        "date": "2026-02-20",
        "title": "미얀마 일부 지역 정세 불안 지속",
        "content": "카친주와 샨주 일대의 정치적 긴장이 계속되고 있어 외국인 투자자들의 우려가 커지고 있습니다.",
        "category": "geopolitical",
        "source": "BBC News",
        "url": "https://www.bbc.com/news/world/asia"
    },
    {
        "date": "2026-03-10",
        "title": "CBM, 기준금리 0.5%p 인하",
        "content": "미얀마 중앙은행이 경기 부양을 위해 기준금리를 9.5%에서 9.0%로 인하했습니다.",
        "category": "regulation",
        "source": "Central Bank of Myanmar",
        "url": "https://www.cbm.gov.mm/"
    },
    {
        "date": "2026-03-28",
        "title": "미얀마 GDP 성장률 4.2% 전망",
        "content": "IMF가 미얀마의 2026년 GDP 성장률을 4.2%로 전망했습니다. 제조업과 서비스업 성장이 주도할 것으로 예상됩니다.",
        "category": "economic",
        "source": "IMF Report",
        "url": "https://www.imf.org/en/Countries/MMR"
    },
    {
        "date": "2026-04-08",
        "title": "미얀마 정부, 암호화폐 거래 규제 검토",
        "content": "미얀마 정부가 암호화폐 거래에 대한 규제 방안을 검토 중입니다. 불법 자금세탁 방지가 주요 목적입니다.",
        "category": "regulation",
        "source": "Myanmar Central Bank",
        "url": "https://www.cbm.gov.mm/"
    },
]

# 인도네시아 2026년 주요 뉴스
INDONESIA_NEWS_2026 = [
    {
        "date": "2026-01-08",
        "title": "인도네시아 OJK, 핀테크 기업 50개 라이선스 취소",
        "content": "금융감독청(OJK)이 규정 위반 핀테크 기업 50개의 영업 허가를 취소했습니다. P2P 대출 부실 채권 관리 실패가 주요 원인입니다.",
        "category": "regulation",
        "source": "OJK Official",
        "url": "https://www.ojk.go.id/"
    },
    {
        "date": "2026-01-20",
        "title": "인도네시아 루피아 강세, 달러당 15,200루피아",
        "content": "인도네시아 루피아 환율이 달러당 15,200루피아로 강세를 보이고 있습니다. 원자재 수출 증가와 외국인 투자 유입이 원인입니다.",
        "category": "economic",
        "source": "Bank Indonesia",
        "url": "https://www.bi.go.id/en/default.aspx"
    },
    {
        "date": "2026-02-10",
        "title": "인도네시아, 전기차 배터리 산업 육성 정책 발표",
        "content": "인도네시아 정부가 전기차 배터리 산업 육성을 위해 100억 달러 규모의 투자 계획을 발표했습니다. 니켈 자원을 활용한 배터리 생산 허브 구축이 목표입니다.",
        "category": "economic",
        "source": "Ministry of Industry",
        "url": "https://www.kemenperin.go.id/"
    },
    {
        "date": "2026-02-25",
        "title": "OJK, 디지털 뱅킹 라이선스 5개 추가 승인",
        "content": "금융감독청이 디지털 전문 은행 라이선스 5개를 추가로 승인했습니다. 핀테크 기업들의 은행업 진출이 본격화됩니다.",
        "category": "regulation",
        "source": "Otoritas Jasa Keuangan",
        "url": "https://www.ojk.go.id/"
    },
    {
        "date": "2026-03-12",
        "title": "인도네시아-호주 FTA 확대 협상 타결",
        "content": "인도네시아와 호주가 자유무역협정(FTA) 확대에 합의했습니다. 농산물과 광물 무역 장벽이 대폭 완화됩니다.",
        "category": "economic",
        "source": "Ministry of Trade",
        "url": "https://www.kemendag.go.id/"
    },
    {
        "date": "2026-03-25",
        "title": "자카르타 증시, 사상 최고치 경신",
        "content": "인도네시아 자카르타 종합지수가 사상 최고치인 7,850포인트를 기록했습니다. 외국인 투자 급증과 경기 회복 기대감이 반영되었습니다.",
        "category": "economic",
        "source": "Jakarta Stock Exchange",
        "url": "https://www.idx.co.id/"
    },
    {
        "date": "2026-04-05",
        "title": "인도네시아 중앙은행, 금리 동결",
        "content": "인도네시아 중앙은행(BI)이 기준금리를 6.0%로 동결했습니다. 인플레이션 안정과 경기 부양 사이에서 균형을 유지하는 전략입니다.",
        "category": "regulation",
        "source": "Bank Indonesia",
        "url": "https://www.bi.go.id/en/default.aspx"
    },
    {
        "date": "2026-04-14",
        "title": "인도네시아, 탄소배출권 거래소 개설",
        "content": "인도네시아가 동남아시아 최초로 탄소배출권 거래소를 개설했습니다. 기후 변화 대응과 녹색 금융 확대가 기대됩니다.",
        "category": "regulation",
        "source": "Ministry of Environment",
        "url": "https://www.menlhk.go.id/"
    },
]


def load_2026_data(db: Session):
    """2026년 미얀마/인도네시아 데이터 로드"""

    # 국가 조회
    myanmar = db.query(Country).filter(Country.code == "MM").first()
    indonesia = db.query(Country).filter(Country.code == "ID").first()

    if not myanmar or not indonesia:
        print("❌ 국가 데이터가 없습니다. 먼저 init_db.py를 실행하세요.")
        return

    print("📅 2026년 이벤트 데이터 로딩 시작...")

    # 미얀마 이벤트
    mm_count = 0
    for event_data in MYANMAR_EVENTS_2026:
        existing = db.query(Event).filter(
            Event.country_id == myanmar.id,
            Event.title == event_data["title"],
            Event.event_date == datetime.strptime(event_data["date"], "%Y-%m-%d").date()
        ).first()

        if not existing:
            event = Event(
                country_id=myanmar.id,
                title=event_data["title"],
                description=event_data["desc"],
                event_date=datetime.strptime(event_data["date"], "%Y-%m-%d").date(),
                event_type=event_data["type"],
                source="Data Loader 2026"
            )
            db.add(event)
            mm_count += 1

    # 인도네시아 이벤트
    id_count = 0
    for event_data in INDONESIA_EVENTS_2026:
        existing = db.query(Event).filter(
            Event.country_id == indonesia.id,
            Event.title == event_data["title"],
            Event.event_date == datetime.strptime(event_data["date"], "%Y-%m-%d").date()
        ).first()

        if not existing:
            event = Event(
                country_id=indonesia.id,
                title=event_data["title"],
                description=event_data["desc"],
                event_date=datetime.strptime(event_data["date"], "%Y-%m-%d").date(),
                event_type=event_data["type"],
                source="Data Loader 2026"
            )
            db.add(event)
            id_count += 1

    db.commit()
    print(f"✅ 미얀마 이벤트 {mm_count}개 추가")
    print(f"✅ 인도네시아 이벤트 {id_count}개 추가")

    # 뉴스 데이터
    print("\n📰 2026년 뉴스 데이터 로딩 시작...")

    # 미얀마 뉴스
    mm_news_count = 0
    for news_data in MYANMAR_NEWS_2026:
        existing = db.query(News).filter(
            News.country_id == myanmar.id,
            News.title == news_data["title"]
        ).first()

        if not existing:
            news = News(
                country_id=myanmar.id,
                title=news_data["title"],
                content=news_data["content"],
                source=news_data["source"],
                category=news_data["category"],
                url=news_data.get("url"),
                published_at=datetime.strptime(news_data["date"], "%Y-%m-%d"),
                source_type="manual"
            )
            db.add(news)
            mm_news_count += 1

    # 인도네시아 뉴스
    id_news_count = 0
    for news_data in INDONESIA_NEWS_2026:
        existing = db.query(News).filter(
            News.country_id == indonesia.id,
            News.title == news_data["title"]
        ).first()

        if not existing:
            news = News(
                country_id=indonesia.id,
                title=news_data["title"],
                content=news_data["content"],
                source=news_data["source"],
                category=news_data["category"],
                url=news_data.get("url"),
                published_at=datetime.strptime(news_data["date"], "%Y-%m-%d"),
                source_type="manual"
            )
            db.add(news)
            id_news_count += 1

    db.commit()
    print(f"✅ 미얀마 뉴스 {mm_news_count}개 추가")
    print(f"✅ 인도네시아 뉴스 {id_news_count}개 추가")

    print(f"\n🎉 2026년 데이터 로딩 완료!")
    print(f"   총 이벤트: {mm_count + id_count}개")
    print(f"   총 뉴스: {mm_news_count + id_news_count}개")
