import { useState } from 'react';
import { InputPanel } from './components/InputPanel';
import { ReportPanel } from './components/ReportPanel';
import { useGenerate } from './hooks/useGenerate';
import { SAMPLE_SCENARIOS } from './types/samples';
import type { SampleScenario } from './types/candidate';

export default function App() {
  const [notes, setNotes] = useState('');
  const [role, setRole] = useState('');
  const [framework, setFramework] = useState('saville_wave');
  const { loading, report, error, latencyMs, frameworks, generate } = useGenerate();

  const handleSubmit = () => {
    void generate({
      notes,
      role: role.trim() || undefined,
      competency_framework: framework,
    });
  };

  const handleLoadSample = (sample: SampleScenario) => {
    setNotes(sample.notes);
    setRole(sample.role);
  };

  return (
    <div className="app">
      <div className="topbar">
        <h1>
          Talent<span className="accent">Lens</span> — Candidate Assessment Reports
        </h1>
        <span className="meta">v1.0.0 · powered by Claude</span>
      </div>
      <div className="layout">
        <InputPanel
          notes={notes}
          onNotesChange={setNotes}
          role={role}
          onRoleChange={setRole}
          framework={framework}
          onFrameworkChange={setFramework}
          frameworks={frameworks}
          samples={SAMPLE_SCENARIOS}
          onLoadSample={handleLoadSample}
          onSubmit={handleSubmit}
          loading={loading}
        />
        <div>
          {loading ? (
            <div className="placeholder">
              <div className="spinner" />
              <h2>Generating report…</h2>
              <p>
                Claude is reviewing the notes, mapping evidence to competencies, and
                drafting follow-up questions. Typically 3–5 seconds.
              </p>
            </div>
          ) : error ? (
            <div className="placeholder error">
              <h2>Could not generate report</h2>
              <p>{error}</p>
              {latencyMs !== null && (
                <span className="latency">failed after {latencyMs} ms</span>
              )}
            </div>
          ) : report ? (
            <ReportPanel report={report} latencyMs={latencyMs} />
          ) : (
            <div className="placeholder">
              <h2>No report yet</h2>
              <p>
                Paste interview notes on the left or load one of the quick-start scenarios,
                then click <strong>Generate Report</strong>.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
