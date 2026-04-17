import { useState, useEffect } from 'react';
import { indicatorsAPI } from '../api/indicators';
import { EconomicIndicator } from '../types/indicator';
import IndicatorChart from './IndicatorChart';

interface IndicatorsViewProps {
  countryCode: string;
}

export default function IndicatorsView({ countryCode }: IndicatorsViewProps) {
  const [indicators, setIndicators] = useState<EconomicIndicator[]>([]);
  const [loading, setLoading] = useState(true);
  const [expandedSections, setExpandedSections] = useState<Record<string, boolean>>({});

  useEffect(() => {
    loadIndicators();
  }, [countryCode]);

  const loadIndicators = async () => {
    setLoading(true);
    try {
      const data = await indicatorsAPI.getByCountry(countryCode);
      setIndicators(data);
    } catch (error) {
      console.error('지표 로딩 실패:', error);
    } finally {
      setLoading(false);
    }
  };

  const getIndicatorName = (type: string) => {
    const names: Record<string, string> = {
      exchange_rate: '환율 (USD 기준)',
      black_market_rate: '암시장 환율',
      gdp_growth: 'GDP 성장률',
      gdp_growth_forecast: 'GDP 성장률 전망',
      inflation: '소비자물가 상승률 (CPI)',
      interest_rate: '기준금리',
      forex_reserve: '외환보유액',
      trade_balance: '무역수지',
      exports: '수출',
      imports: '수입',
      unemployment_rate: '실업률',
      industrial_production: '산업생산지수',
      manufacturing_pmi: '제조업 PMI',
      consumer_confidence: '소비자신뢰지수',
      government_debt: '정부부채',
      fdi: '외국인직접투자',
      retail_sales: '소매판매',
      auto_sales: '자동차판매',
      tourist_arrivals: '외국인관광객',
    };
    return names[type] || type;
  };

  // 핵심 지표 vs 상세 지표 구분
  const coreIndicators = ['exchange_rate', 'gdp_growth', 'inflation', 'interest_rate', 'trade_balance'];

  const isCoreIndicator = (type: string) => coreIndicators.includes(type);

  const toggleSection = (type: string) => {
    setExpandedSections(prev => ({
      ...prev,
      [type]: !prev[type]
    }));
  };

  const groupByType = (indicators: EconomicIndicator[]) => {
    const grouped: Record<string, EconomicIndicator[]> = {};
    indicators.forEach((ind) => {
      if (!grouped[ind.indicator_type]) {
        grouped[ind.indicator_type] = [];
      }
      grouped[ind.indicator_type].push(ind);
    });
    return grouped;
  };

  const getLatestIndicator = (type: string) => {
    const typeIndicators = indicators.filter(ind => ind.indicator_type === type);
    if (typeIndicators.length === 0) return null;
    return typeIndicators.sort((a, b) =>
      new Date(b.recorded_at).getTime() - new Date(a.recorded_at).getTime()
    )[0];
  };

  const calculateKRWExchangeRate = () => {
    const USD_TO_KRW = 1350; // 2026년 4월 기준 환율 (근사치)
    const latestExchangeRate = getLatestIndicator('exchange_rate');

    if (!latestExchangeRate) return null;

    if (countryCode === 'MM') {
      // MMK/USD -> KRW/MMK = KRW/USD / MMK/USD
      const krwPerMMK = USD_TO_KRW / latestExchangeRate.value;
      return {
        value: krwPerMMK,
        unit: 'KRW/MMK',
        localCurrency: 'MMK',
        usdRate: latestExchangeRate.value,
      };
    } else if (countryCode === 'ID') {
      // IDR/USD -> KRW/IDR = KRW/USD / IDR/USD
      const krwPerIDR = USD_TO_KRW / latestExchangeRate.value;
      return {
        value: krwPerIDR,
        unit: 'KRW/IDR',
        localCurrency: 'IDR',
        usdRate: latestExchangeRate.value,
      };
    }
    return null;
  };

  if (loading) {
    return (
      <div className="text-center py-8 sm:py-12">
        <p className="text-gray-500 text-sm">로딩 중...</p>
      </div>
    );
  }

  const groupedIndicators = groupByType(indicators);
  const krwExchange = calculateKRWExchangeRate();
  const latestGDP = getLatestIndicator('gdp_growth');
  const latestInflation = getLatestIndicator('inflation');
  const latestInterestRate = getLatestIndicator('interest_rate');
  const latestTradeBalance = getLatestIndicator('trade_balance');

  // 최종 업데이트 시점 계산
  const getLastUpdateTime = () => {
    if (indicators.length === 0) return null;
    const latestDate = indicators.reduce((latest, ind) => {
      const currentDate = new Date(ind.recorded_at);
      return currentDate > latest ? currentDate : latest;
    }, new Date(0));
    return latestDate;
  };

  const lastUpdate = getLastUpdateTime();

  return (
    <div className="space-y-4 sm:space-y-6">
      {/* 최종 업데이트 시점 */}
      {lastUpdate && (
        <div className="bg-yellow-50 border border-yellow-200 px-3 sm:px-4 py-2 sm:py-3 flex items-center gap-2">
          <svg className="w-4 h-4 text-yellow-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p className="text-xs sm:text-sm text-yellow-800">
            <span className="font-medium">최종 업데이트:</span> {lastUpdate.toLocaleString('ko-KR', {
              year: 'numeric',
              month: 'long',
              day: 'numeric',
              hour: '2-digit',
              minute: '2-digit'
            })} <span className="text-yellow-600">(실시간 연동 아님)</span>
          </p>
        </div>
      )}

      {/* 주요 지표 요약 */}
      <div className="bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-200 p-4 sm:p-6">
        <h2 className="text-base sm:text-lg font-semibold text-gray-800 mb-4">주요 경제 지표 현황</h2>

        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
          {/* 원화 환율 */}
          {krwExchange && (
            <div className="bg-white p-3 sm:p-4 rounded border border-blue-200">
              <p className="text-xs text-gray-600 mb-1">원화 환율</p>
              <p className="text-lg sm:text-xl font-bold text-blue-700">
                {krwExchange.value.toFixed(2)}
              </p>
              <p className="text-xs text-gray-500 mt-1">{krwExchange.unit}</p>
              <p className="text-xs text-gray-400 mt-1">
                (1 USD = {krwExchange.usdRate.toLocaleString()} {krwExchange.localCurrency})
              </p>
            </div>
          )}

          {/* GDP 성장률 */}
          {latestGDP && (
            <div className="bg-white p-3 sm:p-4 rounded border border-blue-200">
              <p className="text-xs text-gray-600 mb-1">GDP 성장률</p>
              <p className="text-lg sm:text-xl font-bold text-green-700">
                {latestGDP.value}%
              </p>
              <p className="text-xs text-gray-500 mt-1">{latestGDP.period}</p>
              <p className="text-xs text-gray-400 mt-1">{latestGDP.source}</p>
            </div>
          )}

          {/* 인플레이션 */}
          {latestInflation && (
            <div className="bg-white p-3 sm:p-4 rounded border border-blue-200">
              <p className="text-xs text-gray-600 mb-1">인플레이션</p>
              <p className="text-lg sm:text-xl font-bold text-orange-700">
                {latestInflation.value}%
              </p>
              <p className="text-xs text-gray-500 mt-1">{latestInflation.period}</p>
              <p className="text-xs text-gray-400 mt-1">{latestInflation.source}</p>
            </div>
          )}

          {/* 기준금리 */}
          {latestInterestRate && (
            <div className="bg-white p-3 sm:p-4 rounded border border-blue-200">
              <p className="text-xs text-gray-600 mb-1">기준금리</p>
              <p className="text-lg sm:text-xl font-bold text-purple-700">
                {latestInterestRate.value}%
              </p>
              <p className="text-xs text-gray-500 mt-1">{latestInterestRate.period}</p>
              <p className="text-xs text-gray-400 mt-1">{latestInterestRate.source}</p>
            </div>
          )}
        </div>

        {/* 무역수지 */}
        {latestTradeBalance && (
          <div className="mt-3 sm:mt-4 bg-white p-3 sm:p-4 rounded border border-blue-200">
            <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-2">
              <div>
                <p className="text-xs text-gray-600 mb-1">무역수지 ({latestTradeBalance.period})</p>
                <p className={`text-lg sm:text-xl font-bold ${latestTradeBalance.value >= 0 ? 'text-blue-700' : 'text-red-700'}`}>
                  {latestTradeBalance.value >= 0 ? '+' : ''}{latestTradeBalance.value.toLocaleString()} {latestTradeBalance.unit}
                </p>
              </div>
              <p className="text-xs text-gray-500">{latestTradeBalance.note}</p>
            </div>
          </div>
        )}
      </div>

      {/* 차트 시각화 */}
      {indicators.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <h2 className="text-base sm:text-lg font-semibold text-gray-800">📊 지표 추이 차트</h2>
            <span className="text-xs text-gray-500">(시계열 데이터)</span>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {/* 환율 차트 */}
            {indicators.some(ind => ind.indicator_type === 'exchange_rate') && (
              <IndicatorChart
                indicators={indicators}
                indicatorType="exchange_rate"
                indicatorName="환율 (USD 기준)"
                chartType="line"
              />
            )}

            {/* GDP 성장률 차트 */}
            {indicators.some(ind => ind.indicator_type === 'gdp_growth') && (
              <IndicatorChart
                indicators={indicators}
                indicatorType="gdp_growth"
                indicatorName="GDP 성장률"
                chartType="bar"
              />
            )}

            {/* 인플레이션 차트 */}
            {indicators.some(ind => ind.indicator_type === 'inflation') && (
              <IndicatorChart
                indicators={indicators}
                indicatorType="inflation"
                indicatorName="소비자물가 상승률 (CPI)"
                chartType="line"
              />
            )}

            {/* 무역수지 차트 */}
            {indicators.some(ind => ind.indicator_type === 'trade_balance') && (
              <IndicatorChart
                indicators={indicators}
                indicatorType="trade_balance"
                indicatorName="무역수지"
                chartType="bar"
              />
            )}

            {/* 실업률 차트 */}
            {indicators.some(ind => ind.indicator_type === 'unemployment_rate') && (
              <IndicatorChart
                indicators={indicators}
                indicatorType="unemployment_rate"
                indicatorName="실업률"
                chartType="line"
              />
            )}

            {/* 기준금리 차트 */}
            {indicators.some(ind => ind.indicator_type === 'interest_rate') && (
              <IndicatorChart
                indicators={indicators}
                indicatorType="interest_rate"
                indicatorName="기준금리"
                chartType="line"
              />
            )}
          </div>
        </div>
      )}

      {/* 핵심 지표 */}
      {Object.entries(groupedIndicators)
        .filter(([type]) => isCoreIndicator(type))
        .length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <h2 className="text-base sm:text-lg font-semibold text-gray-800">📊 핵심 경제 지표</h2>
            <span className="text-xs text-gray-500">(항상 표시)</span>
          </div>

          {Object.entries(groupedIndicators)
            .filter(([type]) => isCoreIndicator(type))
            .map(([type, items]) => (
              <div key={type} className="bg-white border border-blue-200 overflow-hidden shadow-sm">
                <div className="bg-gradient-to-r from-blue-50 to-indigo-50 px-3 sm:px-6 py-3 border-b border-blue-200">
                  <h3 className="text-sm sm:text-base font-semibold text-gray-800">{getIndicatorName(type)}</h3>
                  {items[0]?.source && (
                    <p className="text-xs text-gray-500 mt-1">출처: {items[0].source}</p>
                  )}
                </div>
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-3 sm:px-6 py-2 sm:py-3 text-left text-xs font-medium text-gray-600 uppercase">기간</th>
                        <th className="px-3 sm:px-6 py-2 sm:py-3 text-left text-xs font-medium text-gray-600 uppercase">수치</th>
                        <th className="px-3 sm:px-6 py-2 sm:py-3 text-left text-xs font-medium text-gray-600 uppercase">단위</th>
                        <th className="px-3 sm:px-6 py-2 sm:py-3 text-left text-xs font-medium text-gray-600 uppercase hidden sm:table-cell">비고</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {items
                        .sort((a, b) => new Date(b.recorded_at).getTime() - new Date(a.recorded_at).getTime())
                        .map((item) => (
                          <tr key={item.id} className="hover:bg-gray-50">
                            <td className="px-3 sm:px-6 py-3 sm:py-4 whitespace-nowrap text-xs sm:text-sm text-gray-900 font-medium">{item.period}</td>
                            <td className="px-3 sm:px-6 py-3 sm:py-4 whitespace-nowrap text-xs sm:text-sm font-semibold text-gray-900">
                              {item.value.toLocaleString()}
                            </td>
                            <td className="px-3 sm:px-6 py-3 sm:py-4 whitespace-nowrap text-xs sm:text-sm text-gray-600">{item.unit || '-'}</td>
                            <td className="px-3 sm:px-6 py-3 sm:py-4 text-xs sm:text-sm text-gray-600 hidden sm:table-cell">
                              {item.note || '-'}
                            </td>
                          </tr>
                        ))}
                    </tbody>
                  </table>
                </div>
              </div>
            ))}
        </div>
      )}

      {/* 상세 지표 (접을 수 있음) */}
      {Object.entries(groupedIndicators)
        .filter(([type]) => !isCoreIndicator(type))
        .length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <h2 className="text-base sm:text-lg font-semibold text-gray-800">📈 상세 경제 지표</h2>
            <span className="text-xs text-gray-500">(클릭하여 펼치기/접기)</span>
          </div>

          {Object.entries(groupedIndicators)
            .filter(([type]) => !isCoreIndicator(type))
            .map(([type, items]) => {
              const isExpanded = expandedSections[type] || false;

              return (
                <div key={type} className="bg-white border border-gray-200 overflow-hidden">
                  <button
                    onClick={() => toggleSection(type)}
                    className="w-full bg-gray-50 px-3 sm:px-6 py-3 border-b border-gray-200 hover:bg-gray-100 transition flex justify-between items-center"
                  >
                    <div className="text-left">
                      <h3 className="text-sm sm:text-base font-semibold text-gray-800">{getIndicatorName(type)}</h3>
                      {items[0]?.source && (
                        <p className="text-xs text-gray-500 mt-1">출처: {items[0].source}</p>
                      )}
                    </div>
                    <svg
                      className={`w-5 h-5 text-gray-600 transition-transform ${isExpanded ? 'rotate-180' : ''}`}
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  </button>

                  {isExpanded && (
                    <div className="overflow-x-auto">
                      <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                          <tr>
                            <th className="px-3 sm:px-6 py-2 sm:py-3 text-left text-xs font-medium text-gray-600 uppercase">기간</th>
                            <th className="px-3 sm:px-6 py-2 sm:py-3 text-left text-xs font-medium text-gray-600 uppercase">수치</th>
                            <th className="px-3 sm:px-6 py-2 sm:py-3 text-left text-xs font-medium text-gray-600 uppercase">단위</th>
                            <th className="px-3 sm:px-6 py-2 sm:py-3 text-left text-xs font-medium text-gray-600 uppercase hidden sm:table-cell">비고</th>
                          </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                          {items
                            .sort((a, b) => new Date(b.recorded_at).getTime() - new Date(a.recorded_at).getTime())
                            .map((item) => (
                              <tr key={item.id} className="hover:bg-gray-50">
                                <td className="px-3 sm:px-6 py-3 sm:py-4 whitespace-nowrap text-xs sm:text-sm text-gray-900 font-medium">{item.period}</td>
                                <td className="px-3 sm:px-6 py-3 sm:py-4 whitespace-nowrap text-xs sm:text-sm font-semibold text-gray-900">
                                  {item.value.toLocaleString()}
                                </td>
                                <td className="px-3 sm:px-6 py-3 sm:py-4 whitespace-nowrap text-xs sm:text-sm text-gray-600">{item.unit || '-'}</td>
                                <td className="px-3 sm:px-6 py-3 sm:py-4 text-xs sm:text-sm text-gray-600 hidden sm:table-cell">
                                  {item.note || '-'}
                                </td>
                              </tr>
                            ))}
                        </tbody>
                      </table>
                    </div>
                  )}
                </div>
              );
            })}
        </div>
      )}

      {indicators.length === 0 && (
        <div className="text-center py-8 sm:py-12 bg-white border border-gray-200">
          <p className="text-gray-500 text-sm">등록된 경제 지표가 없습니다.</p>
        </div>
      )}
    </div>
  );
}
