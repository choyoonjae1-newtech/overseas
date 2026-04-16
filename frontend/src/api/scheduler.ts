import client from './client';
import { SchedulerConfig, SchedulerConfigUpdate, TriggerResponse } from '../types/scheduler';

export const schedulerAPI = {
  // 스케줄러 설정 목록 조회
  getConfigs: async (): Promise<SchedulerConfig[]> => {
    const response = await client.get('/api/scheduler/configs');
    return response.data;
  },

  // 스케줄러 설정 수정
  updateConfig: async (id: number, data: SchedulerConfigUpdate): Promise<SchedulerConfig> => {
    const response = await client.put(`/api/scheduler/configs/${id}`, data);
    return response.data;
  },

  // 수동 뉴스 수집 트리거
  triggerCollection: async (countryCode: string): Promise<TriggerResponse> => {
    const response = await client.post(`/api/scheduler/trigger/${countryCode}`);
    return response.data;
  },

  // 수동 경제 지표 수집 트리거
  triggerIndicatorsCollection: async (): Promise<TriggerResponse> => {
    const response = await client.post('/api/scheduler/trigger-indicators');
    return response.data;
  },
};
