import { useCallback, useEffect, useRef, useState } from 'react';
import type {
  CandidateReport,
  FrameworkSummary,
  GenerateRequest,
  GenerateResponse,
  FrameworksResponse,
} from '../types/candidate';

interface UseGenerateState {
  loading: boolean;
  report: CandidateReport | null;
  error: string | null;
  latencyMs: number | null;
  frameworks: FrameworkSummary[];
}

interface UseGenerate extends UseGenerateState {
  generate: (req: GenerateRequest) => Promise<void>;
  reset: () => void;
}

const API_BASE = (import.meta.env.VITE_API_BASE as string | undefined) ?? '/api';

export function useGenerate(): UseGenerate {
  const [state, setState] = useState<UseGenerateState>({
    loading: false,
    report: null,
    error: null,
    latencyMs: null,
    frameworks: [],
  });
  const inflight = useRef<AbortController | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const res = await fetch(`${API_BASE}/frameworks`);
        if (!res.ok) return;
        const body = (await res.json()) as FrameworksResponse;
        if (!cancelled) {
          setState((s) => ({ ...s, frameworks: body.frameworks ?? [] }));
        }
      } catch {
        // best-effort — UI defaults to saville_wave
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const generate = useCallback(async (req: GenerateRequest) => {
    inflight.current?.abort();
    const ctrl = new AbortController();
    inflight.current = ctrl;
    setState((s) => ({ ...s, loading: true, error: null }));
    try {
      const res = await fetch(`${API_BASE}/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(req),
        signal: ctrl.signal,
      });
      if (!res.ok) {
        const text = await res.text().catch(() => '');
        let detail = `request failed with status ${res.status}`;
        try {
          const parsed = JSON.parse(text);
          if (typeof parsed?.detail === 'string') detail = parsed.detail;
        } catch {
          if (text) detail = text;
        }
        setState((s) => ({
          ...s,
          loading: false,
          report: null,
          error: detail,
          latencyMs: null,
        }));
        return;
      }
      const body = (await res.json()) as GenerateResponse;
      if (body.success && body.data) {
        setState((s) => ({
          ...s,
          loading: false,
          report: body.data ?? null,
          error: null,
          latencyMs: body.latency_ms,
        }));
      } else {
        setState((s) => ({
          ...s,
          loading: false,
          report: null,
          error: body.error ?? 'Unknown error generating report',
          latencyMs: body.latency_ms,
        }));
      }
    } catch (err) {
      if ((err as Error).name === 'AbortError') return;
      setState((s) => ({
        ...s,
        loading: false,
        report: null,
        error: (err as Error).message,
        latencyMs: null,
      }));
    } finally {
      if (inflight.current === ctrl) inflight.current = null;
    }
  }, []);

  const reset = useCallback(() => {
    inflight.current?.abort();
    setState((s) => ({ ...s, loading: false, report: null, error: null, latencyMs: null }));
  }, []);

  return { ...state, generate, reset };
}
