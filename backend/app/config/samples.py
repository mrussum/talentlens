"""Pre-loaded sample interview-note scenarios used by both the frontend
quick-start buttons and the backend dry-run prompt verification."""

from typing import Dict, List, TypedDict


class Sample(TypedDict):
    key: str
    label: str
    role: str
    notes: str


SENIOR_PM_NOTES = """\
Candidate: Priya Ramanathan. Role: Senior Product Manager (B2B SaaS payments).
Interviewer: J. Hollis. Format: 60-min structured interview + portfolio walkthrough.

Background: 9 years total PM experience, last 4 at a mid-market fintech leading a
cross-functional team of 12 across engineering, design, and ops. Previously product
lead at a logistics scale-up.

Stakeholder management — strong signal. Walked us through a 14-month enterprise
contract renewal where she personally re-built the relationship with the client's
CFO after a botched migration. Quote: "I ran a weekly steering with their finance
team for nine months — no slides, just a shared doc and honest trade-offs." She
named six internal stakeholders by role and described how she sequenced
conversations to land a controversial roadmap cut. Clearly comfortable in the
room with senior people.

Delivery — strong. Gave concrete numbers on three shipped initiatives: a billing
revamp (cut churn 11%), a partner API (4 design partners live in 5 months), and
an internal tooling rebuild. Talked confidently about scope cuts she made and why.
"I'd rather ship 60% of the spec on time than 100% three months late, and I'll
fight my designer for that trade." Owned a delivery miss honestly — a search
feature that slipped two quarters because she underestimated the data pipeline
work.

Data & analytics — mixed-to-weak. When asked how she sized the billing opportunity
she described "directional analysis" but couldn't articulate the funnel maths.
Pushed on cohort retention and she conflated it with monthly active users twice.
Said "I lean on our analyst for the deep cuts" — fair, but she didn't seem to
sense-check the numbers herself. Would not be comfortable owning the metrics
review for a data-heavy product area.

Leadership — mixed signals. Strong on 1:1s and individual coaching — three
references unprompted talked about her as a manager who "made them better."
Less convincing on shaping a team direction: when asked how she'd set strategy
for an underperforming team of 8 she defaulted to "I'd run a workshop" twice
without going deeper. One concerning anecdote about avoiding a difficult
conversation with an underperforming engineer for two quarters.

Communication — strong. Articulate, structured answers, comfortable with
silence, asked sharp clarifying questions back. Wrote a clear follow-up email
within two hours of the interview.
"""

GRADUATE_ANALYST_NOTES = """\
Candidate: Tom Beasley. Role: Graduate Strategy Analyst.
Interviewer: K. Okafor. Format: case interview + competency questions, 75 min.

Background: First-class Economics degree from Warwick (2025), one summer
internship at a small economic consultancy, plus two years as a part-time
debating coach during university. No full-time commercial experience.

Communication — excellent. Genuinely the strongest grad communicator I've
seen this cycle. Structured every answer with a clear top-line, then
supporting points. Used "let me think for a moment" and actually thought.
On the case (a hypothetical pricing problem for a regional bus operator)
he laid out his framework on the whiteboard before diving in. Quote:
"I want to make sure we're solving the right problem before I start
calculating things." When I pushed back hard on one of his assumptions
he updated his thinking visibly rather than getting defensive.

Problem solving — strong potential, raw. The case answer was structurally
sound but he missed two obvious revenue levers (concession pricing,
off-peak demand) that any practitioner would have hit. When prompted he
got there quickly. He's clearly bright and the framework is good — he
just hasn't seen many real commercial problems yet.

Drive & motivation — strong. Specific reason for applying: read our
published research on transport policy and named two reports by author.
Already done a structured 30-page write-up of his consultancy summer
project — sent it unprompted as part of his application. Two referees
both used the phrase "first one in, last one out."

Commercial awareness — weak, as expected for a grad. Couldn't name our
top three competitors. Confused gross and net revenue at one point in the
case. Vague on what "consulting margin" actually means. Not a red flag for
the level — but he'll need real coaching here in his first six months.

Collaboration — limited evidence. Talked enthusiastically about debate
society but most examples were about him personally winning rather than
the team. Said "I'm probably better one-on-one than in a big group" —
self-aware, at least. No real workplace collaboration stories to draw on.

Adaptability — moderate signal. Handled a curveball question about a
gap in his CV (a deferred year) calmly and honestly. Updated his case
answer twice when given new information without losing the thread.
"""

SALES_DIRECTOR_NOTES = """\
Candidate: Marcus Vance. Role: Sales Director (Enterprise, EMEA).
Interviewer: D. Pereira + R. Singh (panel). Format: 90 min, panel.

Background: 14 years enterprise sales, last role VP Sales at a series-C
cybersecurity vendor where he scaled EMEA revenue from £4m to £22m ARR
over three years. Two prior IC quota-carrying roles, both President's
Club. Strong personal network in financial services and telco.

Drive — extremely strong. Probably the most evident drive I've seen on
this loop. Came in with a 12-month plan already drafted, named six
specific accounts he believed he could open in his first quarter, two
of which he claimed warm intros to. Quote: "I don't really do quiet
quarters — I'd rather miss a number trying than coast and hit it." Two
of his references independently described him as "relentless."

Commercial track record — strong. Concrete numbers throughout: deal
sizes, sales cycles, win rates, net retention. Talked through a £3.4m
deal he closed last year in granular detail — multi-threaded across
seven stakeholders, 11-month cycle, displaced an incumbent. Clearly
knows the mechanics of complex enterprise selling.

Decision making — strong. Walked us through a call he made to fire
two underperforming AEs in his first 90 days at his current role, with
data and a clear rationale. Comfortable making unpopular calls quickly.

Collaboration — concerning. Three separate moments. (1) When asked how
he worked with marketing he said "I tell them what I need and they
deliver it — that's the deal." Tone was dismissive, not playful. (2)
Described product team as "always in the way" of customer commitments.
(3) A back-channel reference (former peer, not on his list) used the
phrase "great closer, terrible teammate" and gave a specific example of
him going around a colleague to win an internal political fight.

Listening — concerning. Interrupted Rohit twice in the panel, including
once mid-question. When I asked an open question about a deal he lost,
he gave a 6-minute monologue that mostly blamed procurement. Did not
ask what we were looking for in this role until the final 5 minutes.

Empowering individuals — mixed. Talks about "building my bench" and
named two people he's promoted. But also told a story about overriding
an AE's discount decision in front of the customer "to show them how
it's done" — framed as mentoring, read as undermining.

Articulating information — strong. Crisp, confident, structured. Maybe
too polished in places — felt like a couple of answers were rehearsed
verbatim from previous interviews.
"""


SAMPLES: List[Sample] = [
    {
        "key": "senior_pm",
        "label": "Senior Product Manager",
        "role": "Senior Product Manager (B2B SaaS payments)",
        "notes": SENIOR_PM_NOTES,
    },
    {
        "key": "graduate_analyst",
        "label": "Graduate Analyst",
        "role": "Graduate Strategy Analyst",
        "notes": GRADUATE_ANALYST_NOTES,
    },
    {
        "key": "sales_director",
        "label": "Sales Director",
        "role": "Sales Director (Enterprise, EMEA)",
        "notes": SALES_DIRECTOR_NOTES,
    },
]


def samples_by_key() -> Dict[str, Sample]:
    return {s["key"]: s for s in SAMPLES}
