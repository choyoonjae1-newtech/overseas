"""
기존 뉴스 데이터에 URL 추가
"""
from core.database import SessionLocal
from models.news import News

# 뉴스별 URL 매핑
NEWS_URLS = {
    # 미얀마 뉴스
    "미얀마 중앙은행, 외환보유고 100억 달러 돌파": "https://www.mmtimes.com/",
    "미얀마 정부, 외국인 투자 인센티브 확대": "https://www.cbm.gov.mm/",
    "미얀마-중국 국경 무역 30% 증가": "https://www.reuters.com/world/asia-pacific/",
    "미얀마 일부 지역 정세 불안 지속": "https://www.bbc.com/news/world/asia",
    "CBM, 기준금리 0.5%p 인하": "https://www.cbm.gov.mm/",
    "미얀마 GDP 성장률 4.2% 전망": "https://www.imf.org/en/Countries/MMR",
    "미얀마 정부, 암호화폐 거래 규제 검토": "https://www.cbm.gov.mm/",

    # 인도네시아 뉴스
    "인도네시아 OJK, 핀테크 기업 50개 라이선스 취소": "https://www.ojk.go.id/",
    "인도네시아 루피아 강세, 달러당 15,200루피아": "https://www.bi.go.id/en/default.aspx",
    "인도네시아, 전기차 배터리 산업 육성 정책 발표": "https://www.kemenperin.go.id/",
    "OJK, 디지털 뱅킹 라이선스 5개 추가 승인": "https://www.ojk.go.id/",
    "인도네시아-호주 FTA 확대 협상 타결": "https://www.kemendag.go.id/",
    "자카르타 증시, 사상 최고치 경신": "https://www.idx.co.id/",
    "인도네시아 중앙은행, 금리 동결": "https://www.bi.go.id/en/default.aspx",
    "인도네시아, 탄소배출권 거래소 개설": "https://www.menlhk.go.id/",
}


def update_news_urls():
    """뉴스 URL 업데이트"""
    db = SessionLocal()

    try:
        updated_count = 0
        for title, url in NEWS_URLS.items():
            news = db.query(News).filter(News.title == title).first()
            if news:
                news.url = url
                updated_count += 1
                print(f"✅ Updated: {title[:50]}...")

        db.commit()
        print(f"\n🎉 총 {updated_count}개 뉴스 URL 업데이트 완료!")

    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("📰 뉴스 URL 업데이트 시작...\n")
    update_news_urls()
