export interface Event {
  id: number;
  country_code: string;
  title: string;
  description: string | null;
  event_date: string;
  event_type: 'holiday' | 'regulation' | 'deadline' | 'other' | null;
  source: string | null;
  url: string | null;
}

export interface EventCreate {
  country_code: string;
  title: string;
  description?: string;
  event_date: string;
  event_type?: string;
  source?: string;
  url?: string;
}
