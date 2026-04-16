import { useState, useEffect } from 'react';
import { indicatorsAPI } from '../api/indicators';
import { EconomicIndicator } from '../types/indicator';

interface IndicatorsViewProps {
  countryCode: string;
}

export default function IndicatorsView({ countryCode }: IndicatorsViewProps) {
  const [indicators, setIndicators] = useState<EconomicIndicator[]>([]);
  const [loading, setLoading] = useState(true);

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
      exchange_rate: '환율',
      gdp_growth: 'GDP 성장률',
      inflation: '인플레이션율',
      interest_rate: '기준금리',
      forex_reserve: '외환보유고',
    };
    return names[type] || type;
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

  if (loading) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">로딩 중...</p>
      </div>
    );
  }

  const groupedIndicators = groupByType(indicators);

  const getSourceUrl = (type: string, countryCode: string) => {
    const sources: Record<string, Record<string, string>> = {
      MM: {
        exchange_rate: 'https://www.cbm.gov.mm/content/exchange-rate',
        gdp_growth: 'https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG?locations=MM',
        inflation: 'https://www.csostat.gov.mm/',
        interest_rate: 'https://www.cbm.gov.mm/content/monetary-policy',
        forex_reserve: 'https://www.cbm.gov.mm/content/foreign-reserve',
      },
      ID: {
        exchange_rate: 'https://www.bi.go.id/en/statistik/informasi-kurs/transaksi-bi/default.aspx',
        gdp_growth: 'https://www.bps.go.id/en/statistics-table/2/MTk3IzI=/gross-domestic-product.html',
        inflation: 'https://www.bps.go.id/en/statistics-table/2/MTI3NiMy/inflation-rate.html',
        interest_rate: 'https://www.bi.go.id/en/fungsi-utama/moneter/bi-7day-rr/default.aspx',
        forex_reserve: 'https://www.bi.go.id/en/statistik/ekonomi-keuangan/sdsk/Default.aspx',
      },
    };
    return sources[countryCode]?.[type] || '#';
  };

  return (
    <div className="space-y-6">
      {Object.entries(groupedIndicators).map(([type, items]) => (
        <div key={type} className="bg-white border border-gray-200 overflow-hidden">
          <div className="bg-gray-50 px-6 py-3 border-b border-gray-200 flex justify-between items-center">
            <h3 className="text-base font-semibold text-gray-800">{getIndicatorName(type)}</h3>
            <a
              href={getSourceUrl(type, countryCode)}
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-blue-700 hover:text-blue-800 flex items-center gap-1"
            >
              데이터 출처 →
            </a>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-600 uppercase">기간</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-600 uppercase">수치</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-600 uppercase">단위</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-600 uppercase">출처</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-600 uppercase">비고</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {items.map((item) => (
                  <tr key={item.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{item.period}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {item.value.toLocaleString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{item.unit || '-'}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-blue-700">
                      {item.source || '-'}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600">{item.note || '-'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ))}

      {indicators.length === 0 && (
        <div className="text-center py-12 bg-white border border-gray-200">
          <p className="text-gray-500">등록된 경제 지표가 없습니다.</p>
        </div>
      )}
    </div>
  );
}
