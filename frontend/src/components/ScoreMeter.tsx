import { FIT_LABEL, FIT_TONE, type FitLevel } from '../types/candidate';

interface Props {
  score: number;
  fit: FitLevel;
  rationale: string;
}

export function ScoreMeter({ score, fit, rationale }: Props) {
  const clamped = Math.max(0, Math.min(100, Math.round(score)));
  const tone = FIT_TONE[fit];
  const fillClass =
    tone === 'caution'
      ? 'score-fill caution'
      : tone === 'negative'
        ? 'score-fill negative'
        : 'score-fill';

  return (
    <div className="card">
      <h2>Fit Score</h2>
      <div className="score-meter">
        <div className="score-meter-row">
          <span className="score-value">{clamped}</span>
          <span className="score-of">/ 100</span>
          <span className={`badge ${tone}`} style={{ marginLeft: 'auto' }}>
            {FIT_LABEL[fit]}
          </span>
        </div>
        <div
          className="score-track"
          role="progressbar"
          aria-valuenow={clamped}
          aria-valuemin={0}
          aria-valuemax={100}
          aria-label="Candidate fit score"
        >
          <div className={fillClass} style={{ width: `${clamped}%` }} />
        </div>
        <p className="score-rationale">{rationale}</p>
      </div>
    </div>
  );
}
