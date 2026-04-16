import client from './client';
import { LoginRequest, RegisterRequest, LoginResponse, User } from '../types/user';

export const authAPI = {
  register: async (data: RegisterRequest) => {
    const response = await client.post('/api/auth/register', data);
    return response.data;
  },

  login: async (data: LoginRequest): Promise<LoginResponse> => {
    const response = await client.post<LoginResponse>('/api/auth/login', data);
    return response.data;
  },

  getMe: async (): Promise<User> => {
    const response = await client.get<User>('/api/auth/me');
    return response.data;
  },
};
