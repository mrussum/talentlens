import { useMemo } from 'react';
import type { FrameworkSummary, SampleScenario } from '../types/candidate';

interface Props {
  notes: string;
  onNotesChange: (value: string) => void;
  role: string;
  onRoleChange: (value: string) => void;
  framework: string;
  onFrameworkChange: (value: string) => void;
  frameworks: FrameworkSummary[];
  samples: SampleScenario[];
  onLoadSample: (sample: SampleScenario) => void;
  onSubmit: () => void;
  loading: boolean;
}

const MIN_CHARS = 50;
const MAX_CHARS = 15000;

export function InputPanel({
  notes,
  onNotesChange,
  role,
  onRoleChange,
  framework,
  onFrameworkChange,
  frameworks,
  samples,
  onLoadSample,
  onSubmit,
  loading,
}: Props) {
  const charCount = notes.length;
  const tooShort = charCount > 0 && charCount < MIN_CHARS;
  const tooLong = charCount > MAX_CHARS;
  const submitDisabled =
    loading || charCount < MIN_CHARS || tooLong;

  const frameworkOptions = useMemo(
    () =>
      frameworks.length
        ? frameworks
        : [{ key: 'saville_wave', label: 'Saville Wave Professional', competencies: [] }],
    [frameworks]
  );

  return (
    <div className="input-panel">
      <div className="card">
        <h2>Assessment Input</h2>

        <div className="field-row" style={{ marginBottom: 14 }}>
          <label htmlFor="role">Role applied for (optional)</label>
          <input
            id="role"
            type="text"
            value={role}
            onChange={(e) => onRoleChange(e.target.value)}
            placeholder="e.g. Senior Product Manager"
            maxLength={200}
            disabled={loading}
          />
        </div>

        <div className="field-row" style={{ marginBottom: 14 }}>
          <label htmlFor="framework">Competency framework</label>
          <select
            id="framework"
            value={framework}
            onChange={(e) => onFrameworkChange(e.target.value)}
            disabled={loading}
          >
            {frameworkOptions.map((fw) => (
              <option key={fw.key} value={fw.key}>
                {fw.label}
              </option>
            ))}
          </select>
        </div>

        <div className="field-row">
          <label htmlFor="notes">Interview notes / assessment data</label>
          <textarea
            id="notes"
            value={notes}
            onChange={(e) => onNotesChange(e.target.value)}
            placeholder="Paste your raw interview notes, evidence, observations, ratings, quotes from the candidate, references — the more concrete signal, the better the report."
            disabled={loading}
            spellCheck
          />
          <div className="field-hint">
            <span>
              {charCount.toLocaleString()} / {MAX_CHARS.toLocaleString()} chars
              {tooShort && ' — minimum 50'}
            </span>
            {(tooShort || tooLong) && (
              <span className="err">
                {tooShort ? 'Too short to generate' : 'Notes exceed maximum length'}
              </span>
            )}
          </div>
        </div>

        <div className="button-row" style={{ marginTop: 16 }}>
          <button
            type="button"
            className="btn-primary"
            onClick={onSubmit}
            disabled={submitDisabled}
          >
            {loading ? 'Generating…' : 'Generate Report'}
          </button>
        </div>
      </div>

      <div className="card">
        <h2>Quick-start scenarios</h2>
        <div className="sample-buttons">
          {samples.map((s) => (
            <button
              key={s.key}
              type="button"
              className="btn-ghost"
              onClick={() => onLoadSample(s)}
              disabled={loading}
            >
              {s.label}
            </button>
          ))}
        </div>
      </div>

      <div className="card">
        <h2>How to use</h2>
        <div className="instructions">
          <ol>
            <li>Paste raw interview notes, references, or assessment-centre data into the notes field.</li>
            <li>Optionally specify the role being assessed and pick a competency framework.</li>
            <li>
              Click <strong>Generate Report</strong>. Claude will rate only competencies for which there
              is concrete evidence in the notes — never fabricated.
            </li>
            <li>Review the report on the right. Export as JSON or Markdown when you're done.</li>
          </ol>
        </div>
      </div>
    </div>
  );
}
