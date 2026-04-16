export interface SchedulerConfig {
  id: number;
  country_code: string;
  enabled: boolean;
  interval_hours: number;
  keywords: string[];
  last_run_at: string | null;
  next_run_at: string | null;
  status: 'idle' | 'running' | 'error';
  last_error: string | null;
}

export interface SchedulerConfigUpdate {
  enabled?: boolean;
  interval_hours?: number;
  keywords?: string[];
}

export interface TriggerResponse {
  success: boolean;
  message: string;
  collected_count?: number;
}
