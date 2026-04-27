import {
  FIT_LABEL,
  FIT_TONE,
  type CandidateReport,
} from '../types/candidate';
import { CompetencyCard } from './CompetencyCard';
import { ExportPanel } from './ExportPanel';
import { QuestionList } from './QuestionList';
import { ScoreMeter } from './ScoreMeter';

interface Props {
  report: CandidateReport;
  latencyMs: number | null;
}

export function ReportPanel({ report, latencyMs }: Props) {
  const tone = FIT_TONE[report.overall_fit];
  return (
    <div className="report">
      <header className="report-header">
        <span className="role">{report.role_applied || 'Role unspecified'}</span>
        <h2 className="name">{report.candidate_name || 'Candidate (name not stated)'}</h2>
        <div className="badges">
          <span className={`badge ${tone}`}>{FIT_LABEL[report.overall_fit]}</span>
          <span className="badge">{report.fit_score}/100</span>
          <span className="badge">
            {Math.round(report.confidence * 100)}% confidence
          </span>
        </div>
      </header>

      <div className="card">
        <h2>Executive summary</h2>
        <p className="summary-text">{report.summary}</p>
      </div>

      <ScoreMeter
        score={report.fit_score}
        fit={report.overall_fit}
        rationale={report.fit_rationale}
      />

      <div className="card">
        <h2>Strengths</h2>
        <ul className="bullet-list">
          {report.strengths.map((s, i) => (
            <li key={i}>{s}</li>
          ))}
        </ul>
      </div>

      <div className="card">
        <h2>Development areas</h2>
        <ul className="bullet-list">
          {report.development_areas.map((s, i) => (
            <li key={i}>{s}</li>
          ))}
        </ul>
      </div>

      {report.competencies.length > 0 && (
        <div className="card">
          <h2>Competency ratings</h2>
          <h3>Only competencies with evidence in the notes are rated</h3>
          <div className="competency-grid">
            {report.competencies.map((c) => (
              <CompetencyCard key={c.name} competency={c} />
            ))}
          </div>
        </div>
      )}

      <QuestionList questions={report.suggested_questions} />

      <div className="recommendation">
        {report.recommendation}
        {latencyMs !== null && (
          <div className="confidence">Generated in {latencyMs} ms</div>
        )}
      </div>

      <ExportPanel report={report} />
    </div>
  );
}
