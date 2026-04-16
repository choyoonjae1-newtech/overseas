import client from './client';
import { User } from '../types/user';

export const usersAPI = {
  getPendingUsers: async (): Promise<User[]> => {
    const response = await client.get<User[]>('/api/users/pending');
    return response.data;
  },

  approveUser: async (userId: number) => {
    const response = await client.put(`/api/users/${userId}/approve`);
    return response.data;
  },

  rejectUser: async (userId: number) => {
    const response = await client.put(`/api/users/${userId}/reject`);
    return response.data;
  },
};
