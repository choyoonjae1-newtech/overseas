"""
AI 요약 및 분석 서비스
- Claude API를 사용하여 뉴스 자동 요약
- 경제 지표 자동 해석
- 리스크 평가 및 인사이트 생성
"""
from anthropic import Anthropic
from typing import List, Dict, Optional
import logging
from core.config import settings
from models import News, EconomicIndicator

logger = logging.getLogger(__name__)


class AISummarizer:
    """Claude API 기반 AI 요약 및 분석 서비스"""

    def __init__(self):
        # Claude API 설정
        self.api_key = getattr(settings, 'CLAUDE_API_KEY', None)
        self.enabled = bool(self.api_key)

        if self.enabled:
            self.client = Anthropic(api_key=self.api_key)
            self.model = "claude-3-5-sonnet-20241022"  # 최신 Sonnet 모델
        else:
            logger.warning("AI 요약이 비활성화되었습니다. CLAUDE_API_KEY를 설정하세요.")

    def summarize_news(self, news_list: List[News], country_name: str) -> Optional[str]:
        """
        뉴스 목록 요약
        """
        if not self.enabled:
            logger.debug("AI 요약이 비활성화되어 있습니다.")
            return None

        if not news_list:
            return "분석할 뉴스가 없습니다."

        try:
            # 뉴스 목록을 텍스트로 변환
            news_text = "\n\n".join([
                f"[{i+1}] {news.title}\n출처: {news.source}\n카테고리: {news.category or '기타'}\n{news.content or '(내용 없음)'}"
                for i, news in enumerate(news_list[:10])  # 최대 10개
            ])

            prompt = f"""당신은 금융 전문가입니다. {country_name}의 최근 뉴스를 분석하여 다음 형식으로 요약해주세요:

## 📰 뉴스 목록
{news_text}

## 요청사항
1. **주요 동향 요약** (3-5문장)
   - 전반적인 경제/금융 상황 개요
   - 주요 이슈 및 트렌드

2. **카테고리별 분석**
   - 금융규제: 주요 규제 변화 및 영향
   - 경제: 경제 지표 및 전망
   - 지정학적 리스크: 정치/안보 관련 이슈

3. **리스크 평가** (1-10점)
   - 금융 리스크: X/10
   - 정치 리스크: X/10
   - 운영 리스크: X/10
   - 각 리스크에 대한 간단한 설명 (1-2문장)

4. **권장 조치사항** (우선순위 순)
   - 즉시 조치 필요: ...
   - 모니터링 필요: ...
   - 참고사항: ...

간결하고 명확하게 작성해주세요. 한국어로 답변하세요."""

            # Claude API 호출
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.3,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            summary = message.content[0].text

            logger.info(f"✅ AI 요약 생성 완료: {country_name} ({len(news_list)}개 뉴스)")
            return summary

        except Exception as e:
            logger.error(f"❌ AI 요약 실패: {e}")
            return f"AI 요약 생성 중 오류가 발생했습니다: {str(e)}"

    def analyze_indicators(
        self,
        indicators: List[EconomicIndicator],
        country_name: str
    ) -> Optional[str]:
        """
        경제 지표 분석 및 해석
        """
        if not self.enabled:
            return None

        if not indicators:
            return "분석할 경제 지표가 없습니다."

        try:
            # 지표를 그룹화
            indicators_by_type = {}
            for ind in indicators:
                if ind.indicator_type not in indicators_by_type:
                    indicators_by_type[ind.indicator_type] = []
                indicators_by_type[ind.indicator_type].append(ind)

            # 최신 지표만 선택
            latest_indicators = []
            for indicator_type, inds in indicators_by_type.items():
                latest = sorted(inds, key=lambda x: x.recorded_at, reverse=True)[0]
                latest_indicators.append(latest)

            # 지표 텍스트 생성
            indicators_text = "\n".join([
                f"- {self._get_indicator_name(ind.indicator_type)}: {ind.value} {ind.unit or ''} ({ind.period})"
                for ind in latest_indicators
            ])

            prompt = f"""당신은 경제 분석 전문가입니다. {country_name}의 최신 경제 지표를 분석해주세요:

## 📊 경제 지표
{indicators_text}

## 요청사항
1. **전반적 경제 상황 평가** (3-4문장)
   - 현재 경제 상태 요약
   - 주요 강점과 약점

2. **지표별 해석**
   - 환율: 추세 및 영향
   - GDP 성장률: 성장 동력 분석
   - 인플레이션: 물가 안정성 평가
   - 무역수지: 대외 경제 건전성
   - (해당하는 지표에 대해서만)

3. **향후 전망** (1-3개월)
   - 긍정적 요인
   - 부정적 요인
   - 가능성 있는 시나리오

4. **투자/운영 시사점**
   - 금융기관 입장에서의 기회와 리스크
   - 권장 전략 (확장/보수적 접근/현상유지 등)

간결하고 명확하게 작성해주세요. 한국어로 답변하세요."""

            # Claude API 호출
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.3,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            analysis = message.content[0].text

            logger.info(f"✅ AI 지표 분석 완료: {country_name} ({len(latest_indicators)}개 지표)")
            return analysis

        except Exception as e:
            logger.error(f"❌ AI 지표 분석 실패: {e}")
            return f"AI 분석 생성 중 오류가 발생했습니다: {str(e)}"

    def generate_comparison_insight(
        self,
        myanmar_indicators: List[EconomicIndicator],
        indonesia_indicators: List[EconomicIndicator]
    ) -> Optional[str]:
        """
        미얀마 vs 인도네시아 비교 분석
        """
        if not self.enabled:
            return None

        try:
            # 양국 지표를 간단히 요약
            mm_summary = self._summarize_indicators(myanmar_indicators, "미얀마")
            id_summary = self._summarize_indicators(indonesia_indicators, "인도네시아")

            prompt = f"""당신은 국제 금융 전문가입니다. 미얀마와 인도네시아의 경제 지표를 비교 분석해주세요:

## 🇲🇲 미얀마
{mm_summary}

## 🇮🇩 인도네시아
{id_summary}

## 요청사항
1. **핵심 차이점** (3-4가지)
   - 경제 규모
   - 성장 속도
   - 리스크 프로필

2. **각국의 강점/약점**
   - 미얀마: 강점 2가지, 약점 2가지
   - 인도네시아: 강점 2가지, 약점 2가지

3. **금융기관 관점 비교**
   - 어느 국가가 더 안정적인가?
   - 어느 국가에서 성장 기회가 더 큰가?
   - 각국의 주요 리스크 요인

4. **전략적 권장사항**
   - 미얀마 사업부: ...
   - 인도네시아 사업부: ...
   - 전사적 리스크 관리: ...

간결하고 객관적으로 작성해주세요. 한국어로 답변하세요."""

            # Claude API 호출
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.3,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            insight = message.content[0].text

            logger.info("✅ AI 비교 분석 완료")
            return insight

        except Exception as e:
            logger.error(f"❌ AI 비교 분석 실패: {e}")
            return f"AI 분석 생성 중 오류가 발생했습니다: {str(e)}"

    def _summarize_indicators(self, indicators: List[EconomicIndicator], country: str) -> str:
        """지표 목록을 간단히 요약"""
        if not indicators:
            return f"{country}: 데이터 없음"

        # 지표 타입별 최신 값
        indicators_by_type = {}
        for ind in indicators:
            if ind.indicator_type not in indicators_by_type:
                indicators_by_type[ind.indicator_type] = []
            indicators_by_type[ind.indicator_type].append(ind)

        lines = []
        for indicator_type, inds in indicators_by_type.items():
            latest = sorted(inds, key=lambda x: x.recorded_at, reverse=True)[0]
            name = self._get_indicator_name(indicator_type)
            lines.append(f"- {name}: {latest.value} {latest.unit or ''}")

        return "\n".join(lines)

    def _get_indicator_name(self, indicator_type: str) -> str:
        """지표 타입을 한글 이름으로 변환"""
        names = {
            'exchange_rate': '환율',
            'gdp_growth': 'GDP 성장률',
            'inflation': '인플레이션',
            'interest_rate': '기준금리',
            'trade_balance': '무역수지',
            'unemployment_rate': '실업률',
            'exports': '수출',
            'imports': '수입',
            'forex_reserve': '외환보유액'
        }
        return names.get(indicator_type, indicator_type)


# 싱글톤 인스턴스
ai_summarizer = AISummarizer()
