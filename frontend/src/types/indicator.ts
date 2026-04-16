export interface EconomicIndicator {
  id: number;
  country_id: number;
  indicator_type: string;
  value: number;
  unit: string | null;
  period: string;
  recorded_at: string;
  source: string | null;
  note: string | null;
}

export interface IndicatorCreate {
  country_code: string;
  indicator_type: string;
  value: number;
  unit?: string;
  period: string;
  recorded_at: string;
  source?: string;
  note?: string;
}
