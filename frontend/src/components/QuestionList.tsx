interface Props {
  questions: string[];
}

export function QuestionList({ questions }: Props) {
  return (
    <div className="card">
      <h2>Suggested follow-up questions</h2>
      <h3>STAR-format probes for the next interview</h3>
      <ol className="question-list">
        {questions.map((q, idx) => (
          <li key={idx}>{q}</li>
        ))}
      </ol>
    </div>
  );
}
