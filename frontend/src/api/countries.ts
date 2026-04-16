import client from './client';
import { Country } from '../types/country';

export const countriesAPI = {
  getAll: async (): Promise<Country[]> => {
    const response = await client.get<Country[]>('/api/countries');
    return response.data;
  },
};
