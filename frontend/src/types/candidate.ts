export type FitLevel =
  | 'strong_fit'
  | 'good_fit'
  | 'possible_fit'
  | 'not_recommended';

export interface CompetencyRating {
  name: string;
  rating: number;
  evidence: string;
  development_area: boolean;
}

export interface CandidateReport {
  candidate_name: string | null;
  role_applied: string | null;
  summary: string;
  overall_fit: FitLevel;
  fit_score: number;
  fit_rationale: string;
  strengths: string[];
  development_areas: string[];
  competencies: CompetencyRating[];
  suggested_questions: string[];
  recommendation: string;
  confidence: number;
}

export interface GenerateRequest {
  notes: string;
  role?: string;
  competency_framework?: string;
}

export interface GenerateResponse {
  success: boolean;
  data?: CandidateReport;
  error?: string;
  latency_ms: number;
}

export interface FrameworkSummary {
  key: string;
  label: string;
  competencies: string[];
}

export interface FrameworksResponse {
  frameworks: FrameworkSummary[];
}

export interface SampleScenario {
  key: string;
  label: string;
  role: string;
  notes: string;
}

export const FIT_LABEL: Record<FitLevel, string> = {
  strong_fit: 'Strong fit',
  good_fit: 'Good fit',
  possible_fit: 'Possible fit',
  not_recommended: 'Not recommended',
};

export const FIT_TONE: Record<FitLevel, 'positive' | 'good' | 'caution' | 'negative'> = {
  strong_fit: 'positive',
  good_fit: 'good',
  possible_fit: 'caution',
  not_recommended: 'negative',
};
