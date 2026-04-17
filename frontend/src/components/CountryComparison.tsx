import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { indicatorsAPI } from '../api/indicators';
import { newsAPI } from '../api/news';
import { EconomicIndicator } from '../types/indicator';
import { News } from '../types/news';

export default function CountryComparison() {
  const navigate = useNavigate();
  const [myanmarIndicators, setMyanmarIndicators] = useState<EconomicIndicator[]>([]);
  const [indonesiaIndicators, setIndonesiaIndicators] = useState<EconomicIndicator[]>([]);
  const [myanmarNews, setMyanmarNews] = useState<News[]>([]);
  const [indonesiaNews, setIndonesiaNews] = useState<News[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [mmIndicators, idIndicators, mmNews, idNews] = await Promise.all([
        indicatorsAPI.getByCountry('MM'),
        indicatorsAPI.getByCountry('ID'),
        newsAPI.getByCountry('MM', {}),
        newsAPI.getByCountry('ID', {}),
      ]);

      setMyanmarIndicators(mmIndicators);
      setIndonesiaIndicators(idIndicators);
      setMyanmarNews(mmNews.slice(0, 5)); // 최근 5개
      setIndonesiaNews(idNews.slice(0, 5));
    } catch (error) {
      console.error('데이터 로딩 실패:', error);
    } finally {
      setLoading(false);
    }
  };

  const getLatestIndicator = (indicators: EconomicIndicator[], type: string) => {
    const filtered = indicators.filter(ind => ind.indicator_type === type);
    if (filtered.length === 0) return null;
    return filtered.sort((a, b) =>
      new Date(b.recorded_at).getTime() - new Date(a.recorded_at).getTime()
    )[0];
  };

  const ComparisonCard = ({ title, mmValue, idValue, unit, mmSource, idSource }: {
    title: string;
    mmValue: number | null;
    idValue: number | null;
    unit: string;
    mmSource?: string;
    idSource?: string;
  }) => (
    <div className="bg-white border border-gray-200 rounded-lg p-4">
      <h3 className="text-sm font-semibold text-gray-800 mb-3">{title}</h3>
      <div className="grid grid-cols-2 gap-3">
        {/* Myanmar */}
        <div className="text-center p-3 bg-blue-50 rounded">
          <p className="text-xs text-gray-600 mb-1">🇲🇲 미얀마</p>
          <p className="text-lg font-bold text-blue-700">
            {mmValue !== null ? `${mmValue.toLocaleString()} ${unit}` : 'N/A'}
          </p>
          {mmSource && <p className="text-xs text-gray-500 mt-1">{mmSource}</p>}
        </div>

        {/* Indonesia */}
        <div className="text-center p-3 bg-green-50 rounded">
          <p className="text-xs text-gray-600 mb-1">🇮🇩 인도네시아</p>
          <p className="text-lg font-bold text-green-700">
            {idValue !== null ? `${idValue.toLocaleString()} ${unit}` : 'N/A'}
          </p>
          {idSource && <p className="text-xs text-gray-500 mt-1">{idSource}</p>}
        </div>
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <p className="text-gray-500">로딩 중...</p>
      </div>
    );
  }

  const mmExchangeRate = getLatestIndicator(myanmarIndicators, 'exchange_rate');
  const idExchangeRate = getLatestIndicator(indonesiaIndicators, 'exchange_rate');
  const mmGDP = getLatestIndicator(myanmarIndicators, 'gdp_growth');
  const idGDP = getLatestIndicator(indonesiaIndicators, 'gdp_growth');
  const mmInflation = getLatestIndicator(myanmarIndicators, 'inflation');
  const idInflation = getLatestIndicator(indonesiaIndicators, 'inflation');
  const mmInterestRate = getLatestIndicator(myanmarIndicators, 'interest_rate');
  const idInterestRate = getLatestIndicator(indonesiaIndicators, 'interest_rate');
  const mmTradeBalance = getLatestIndicator(myanmarIndicators, 'trade_balance');
  const idTradeBalance = getLatestIndicator(indonesiaIndicators, 'trade_balance');
  const mmUnemployment = getLatestIndicator(myanmarIndicators, 'unemployment_rate');
  const idUnemployment = getLatestIndicator(indonesiaIndicators, 'unemployment_rate');

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-4 flex justify-between items-center">
          <button
            onClick={() => navigate('/')}
            className="text-blue-700 hover:text-blue-800 text-sm"
          >
            ← 홈으로
          </button>
          <h1 className="text-xl font-semibold text-gray-800">국가 비교 분석</h1>
          <div className="w-20"></div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-6 space-y-6">
        {/* 개요 */}
        <div className="bg-gradient-to-r from-blue-50 to-green-50 p-6 rounded-lg border border-blue-200">
          <h2 className="text-lg font-semibold text-gray-800 mb-2">미얀마 vs 인도네시아</h2>
          <p className="text-sm text-gray-600">
            두 국가의 주요 경제 지표, 뉴스, 정책 동향을 비교하여 전략적 의사결정을 지원합니다.
          </p>
        </div>

        {/* 주요 경제 지표 비교 */}
        <div>
          <h2 className="text-lg font-semibold text-gray-800 mb-4">📊 주요 경제 지표 비교</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <ComparisonCard
              title="환율 (USD 기준)"
              mmValue={mmExchangeRate?.value || null}
              idValue={idExchangeRate?.value || null}
              unit={mmExchangeRate?.unit || idExchangeRate?.unit || ''}
              mmSource={mmExchangeRate?.period}
              idSource={idExchangeRate?.period}
            />

            <ComparisonCard
              title="GDP 성장률"
              mmValue={mmGDP?.value || null}
              idValue={idGDP?.value || null}
              unit="%"
              mmSource={mmGDP?.period}
              idSource={idGDP?.period}
            />

            <ComparisonCard
              title="인플레이션"
              mmValue={mmInflation?.value || null}
              idValue={idInflation?.value || null}
              unit="%"
              mmSource={mmInflation?.period}
              idSource={idInflation?.period}
            />

            <ComparisonCard
              title="기준금리"
              mmValue={mmInterestRate?.value || null}
              idValue={idInterestRate?.value || null}
              unit="%"
              mmSource={mmInterestRate?.period}
              idSource={idInterestRate?.period}
            />

            <ComparisonCard
              title="실업률"
              mmValue={mmUnemployment?.value || null}
              idValue={idUnemployment?.value || null}
              unit="%"
              mmSource={mmUnemployment?.period}
              idSource={idUnemployment?.period}
            />

            <ComparisonCard
              title="무역수지"
              mmValue={mmTradeBalance?.value || null}
              idValue={idTradeBalance?.value || null}
              unit={mmTradeBalance?.unit || idTradeBalance?.unit || 'USD'}
              mmSource={mmTradeBalance?.period}
              idSource={idTradeBalance?.period}
            />
          </div>
        </div>

        {/* 최근 뉴스 비교 */}
        <div>
          <h2 className="text-lg font-semibold text-gray-800 mb-4">📰 최근 주요 소식</h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Myanmar News */}
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <h3 className="text-base font-semibold text-blue-700 mb-3 flex items-center gap-2">
                <span>🇲🇲</span>
                <span>미얀마</span>
              </h3>
              <div className="space-y-3">
                {myanmarNews.length > 0 ? (
                  myanmarNews.map((news) => (
                    <div key={news.id} className="border-b border-gray-200 pb-3 last:border-0">
                      <h4 className="text-sm font-medium text-gray-900 mb-1">{news.title}</h4>
                      <p className="text-xs text-gray-500">
                        {news.source} • {news.published_at ? new Date(news.published_at).toLocaleDateString('ko-KR') : '날짜 미상'}
                      </p>
                    </div>
                  ))
                ) : (
                  <p className="text-sm text-gray-500">뉴스가 없습니다.</p>
                )}
              </div>
              <button
                onClick={() => navigate('/countries/MM')}
                className="mt-4 text-sm text-blue-700 hover:text-blue-800"
              >
                더보기 →
              </button>
            </div>

            {/* Indonesia News */}
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <h3 className="text-base font-semibold text-green-700 mb-3 flex items-center gap-2">
                <span>🇮🇩</span>
                <span>인도네시아</span>
              </h3>
              <div className="space-y-3">
                {indonesiaNews.length > 0 ? (
                  indonesiaNews.map((news) => (
                    <div key={news.id} className="border-b border-gray-200 pb-3 last:border-0">
                      <h4 className="text-sm font-medium text-gray-900 mb-1">{news.title}</h4>
                      <p className="text-xs text-gray-500">
                        {news.source} • {news.published_at ? new Date(news.published_at).toLocaleDateString('ko-KR') : '날짜 미상'}
                      </p>
                    </div>
                  ))
                ) : (
                  <p className="text-sm text-gray-500">뉴스가 없습니다.</p>
                )}
              </div>
              <button
                onClick={() => navigate('/countries/ID')}
                className="mt-4 text-sm text-green-700 hover:text-green-800"
              >
                더보기 →
              </button>
            </div>
          </div>
        </div>

        {/* 종합 분석 */}
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-3">💡 종합 분석</h2>
          <div className="space-y-2 text-sm text-gray-700">
            <p>
              • <strong>경제 규모:</strong> 인도네시아가 미얀마보다 현저히 큰 경제 규모를 가지고 있습니다.
            </p>
            <p>
              • <strong>성장률:</strong> {mmGDP && idGDP && (
                mmGDP.value > idGDP.value
                  ? '미얀마의 GDP 성장률이 인도네시아보다 높습니다.'
                  : '인도네시아의 GDP 성장률이 미얀마보다 높습니다.'
              )}
            </p>
            <p>
              • <strong>인플레이션:</strong> {mmInflation && idInflation && (
                mmInflation.value > idInflation.value
                  ? '미얀마의 인플레이션이 인도네시아보다 높아 물가 안정성이 낮습니다.'
                  : '인도네시아의 인플레이션이 미얀마보다 높아 물가 압력이 존재합니다.'
              )}
            </p>
            <p className="text-xs text-gray-500 mt-3">
              ⚠️ 이 분석은 최신 데이터를 기반으로 한 개괄적인 비교이며, 상세한 의사결정을 위해서는 전문가의 추가 분석이 필요합니다.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
