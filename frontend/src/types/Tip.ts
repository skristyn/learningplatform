export interface Tip {
  user?: string;
  body: string;
  created_at?: string;
}

export interface TipResponse {
  meta: {
    total_count: number;
  };
  items: Tip[];
}
