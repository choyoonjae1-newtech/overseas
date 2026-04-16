import client from './client';
import { EconomicIndicator, IndicatorCreate } from '../types/indicator';

export const indicatorsAPI = {
  // 국가별 경제 지표 조회
  getByCountry: async (countryCode: string, indicatorType?: string): Promise<EconomicIndicator[]> => {
    const params = indicatorType ? { indicator_type: indicatorType } : {};
    const response = await client.get(`/api/indicators/countries/${countryCode}`, { params });
    return response.data;
  },

  // 경제 지표 추가
  create: async (data: IndicatorCreate): Promise<EconomicIndicator> => {
    const response = await client.post('/api/indicators', data);
    return response.data;
  },

  // 경제 지표 삭제
  delete: async (id: number): Promise<void> => {
    await client.delete(`/api/indicators/${id}`);
  },
};
