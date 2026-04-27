import type { CompetencyRating } from '../types/candidate';

interface Props {
  competency: CompetencyRating;
}

function Star({ filled }: { filled: boolean }) {
  return (
    <svg
      className={filled ? 'star filled' : 'star'}
      viewBox="0 0 20 20"
      aria-hidden
    >
      <path d="M10 1.5l2.6 5.27 5.82.85-4.21 4.1.99 5.78L10 14.77l-5.2 2.73.99-5.78L1.58 7.62l5.82-.85L10 1.5z" />
    </svg>
  );
}

export function CompetencyCard({ competency }: Props) {
  const rating = Math.max(1, Math.min(5, Math.round(competency.rating)));
  return (
    <div
      className={
        competency.development_area
          ? 'competency-card development'
          : 'competency-card'
      }
    >
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: 8,
        }}
      >
        <span className="competency-name">{competency.name}</span>
        <span
          className="stars"
          aria-label={`Rated ${rating} out of 5`}
          title={`${rating} / 5`}
        >
          {[1, 2, 3, 4, 5].map((i) => (
            <Star key={i} filled={i <= rating} />
          ))}
        </span>
      </div>
      <div className="evidence">"{competency.evidence}"</div>
      {competency.development_area && (
        <div className="dev-tag">Development area</div>
      )}
    </div>
  );
}
