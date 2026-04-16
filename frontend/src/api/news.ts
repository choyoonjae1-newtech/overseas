import client from './client';
import { News, NewsCreate } from '../types/news';

export const newsAPI = {
  getByCountry: async (
    countryCode: string,
    params?: { category?: string; limit?: number; offset?: number }
  ): Promise<News[]> => {
    const response = await client.get<News[]>(`/api/countries/${countryCode}/news`, { params });
    return response.data;
  },

  getDetail: async (newsId: number): Promise<News> => {
    const response = await client.get<News>(`/api/news/${newsId}`);
    return response.data;
  },

  create: async (data: NewsCreate): Promise<News> => {
    const response = await client.post<News>('/api/news', data);
    return response.data;
  },

  update: async (newsId: number, data: Partial<NewsCreate>): Promise<News> => {
    const response = await client.put<News>(`/api/news/${newsId}`, data);
    return response.data;
  },

  delete: async (newsId: number) => {
    const response = await client.delete(`/api/news/${newsId}`);
    return response.data;
  },
};
