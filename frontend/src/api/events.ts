import client from './client';
import { Event, EventCreate } from '../types/event';

export const eventsAPI = {
  getByCountry: async (
    countryCode: string,
    params?: { start_date?: string; end_date?: string; event_type?: string }
  ): Promise<Event[]> => {
    const response = await client.get<Event[]>(`/api/countries/${countryCode}/events`, { params });
    return response.data;
  },

  create: async (data: EventCreate): Promise<Event> => {
    const response = await client.post<Event>('/api/events', data);
    return response.data;
  },

  update: async (eventId: number, data: Partial<EventCreate>): Promise<Event> => {
    const response = await client.put<Event>(`/api/events/${eventId}`, data);
    return response.data;
  },

  delete: async (eventId: number) => {
    const response = await client.delete(`/api/events/${eventId}`);
    return response.data;
  },
};
