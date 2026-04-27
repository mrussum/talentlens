import { useState } from 'react';
import { FIT_LABEL, type CandidateReport } from '../types/candidate';

interface Props {
  report: CandidateReport;
}

function reportToMarkdown(r: CandidateReport): string {
  const lines: string[] = [];
  const name = r.candidate_name?.trim() || 'Candidate';
  const role = r.role_applied?.trim() || 'Role unspecified';
  lines.push(`# Candidate Assessment Report — ${name}`);
  lines.push('');
  lines.push(`**Role:** ${role}`);
  lines.push(`**Overall fit:** ${FIT_LABEL[r.overall_fit]} (${r.fit_score}/100)`);
  lines.push(`**Confidence:** ${(r.confidence * 100).toFixed(0)}%`);
  lines.push('');
  lines.push('## Executive summary');
  lines.push(r.summary);
  lines.push('');
  lines.push('## Fit rationale');
  lines.push(r.fit_rationale);
  lines.push('');
  lines.push('## Strengths');
  r.strengths.forEach((s) => lines.push(`- ${s}`));
  lines.push('');
  lines.push('## Development areas');
  r.development_areas.forEach((s) => lines.push(`- ${s}`));
  lines.push('');
  lines.push('## Competency ratings');
  r.competencies.forEach((c) => {
    const stars = '★'.repeat(c.rating) + '☆'.repeat(5 - c.rating);
    lines.push(`### ${c.name} — ${stars} (${c.rating}/5)${c.development_area ? '  _[development area]_' : ''}`);
    lines.push(`> ${c.evidence}`);
    lines.push('');
  });
  lines.push('## Suggested follow-up questions');
  r.suggested_questions.forEach((q, idx) => lines.push(`${idx + 1}. ${q}`));
  lines.push('');
  lines.push('## Recommendation');
  lines.push(`> ${r.recommendation}`);
  lines.push('');
  return lines.join('\n');
}

function safeFilename(name: string | null | undefined, ext: string): string {
  const base = (name || 'candidate-report').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  return `${base || 'candidate-report'}.${ext}`;
}

export function ExportPanel({ report }: Props) {
  const [status, setStatus] = useState<string>('');

  const copyJson = async () => {
    try {
      await navigator.clipboard.writeText(JSON.stringify(report, null, 2));
      setStatus('Report JSON copied to clipboard.');
    } catch {
      setStatus('Could not access clipboard. Try the download instead.');
    }
    window.setTimeout(() => setStatus(''), 3000);
  };

  const downloadMarkdown = () => {
    const md = reportToMarkdown(report);
    const blob = new Blob([md], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = safeFilename(report.candidate_name, 'md');
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    setStatus('Markdown downloaded.');
    window.setTimeout(() => setStatus(''), 3000);
  };

  return (
    <div className="card">
      <h2>Export</h2>
      <div className="export-panel">
        <button type="button" className="btn-secondary" onClick={copyJson}>
          Copy report JSON
        </button>
        <button type="button" className="btn-secondary" onClick={downloadMarkdown}>
          Download as Markdown
        </button>
        {status && <span className="export-status">{status}</span>}
      </div>
    </div>
  );
}
