export interface News {
  id: number;
  country_code: string;
  title: string;
  content: string | null;
  source: string | null;
  url: string | null;
  category: 'regulation' | 'geopolitical' | 'economic' | 'other' | null;
  published_at: string | null;
  created_at: string;
  source_type: 'api' | 'crawl' | 'manual';
}

export interface NewsCreate {
  country_code: string;
  title: string;
  content?: string;
  source?: string;
  url?: string;
  category?: string;
  published_at?: string;
}
