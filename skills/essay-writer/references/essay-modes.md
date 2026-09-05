# Essay modes

Use this reference to select the smallest workflow that satisfies the request. A mode describes the job, not a rigid template.

## Mode selection

| User need | Primary mode | Useful combination |
|---|---|---|
| “Help me understand this assignment” | Plan | Plan → Review |
| “Give me a thesis and outline” | Plan | Plan → Research |
| “Write an essay about…” | Draft | Plan → Draft → Review |
| “Turn these notes or sources into an essay” | Draft | Draft → Review |
| “Improve, rewrite, or proofread this essay” | Edit | Edit → Review |
| “Grade this against the rubric” | Review | Review only |
| “Find evidence and competing views” | Research | Research → Plan → Draft |
| “Does this look AI-generated?” | Detect | Detect only |
| “Find or fix repetitive statistical or structural patterns” | Pattern | Pattern → Edit → Review |
| “Map claims to sources or audit citations” | Evidence | Evidence → Edit or Draft |
| “Write a personal statement” | Personal statement | Plan → Personal statement → Review |
| “Write a scholarship essay” | Scholarship essay | Plan → Scholarship essay → Review |
| “Write a lab report” | Lab report | Plan → Lab report → Review |
| “Synthesize research into a literature review” | Literature review | Research → Literature review → Review |

Do not silently switch Review or Detect into rewriting. If several modes are requested, complete them in the order that avoids wasted work.

## Plan

### Establish

- What question must the essay answer?
- Which instruction words control the task: analyse, compare, evaluate, argue, reflect, explain, or describe?
- What position can the available evidence support?
- What length, audience, level, and citation style apply?

### Build

1. Paraphrase the task without weakening it.
2. Propose a working thesis that is specific, arguable, and responsive.
3. Map the major claims, evidence, analysis, counterargument, and implications.
4. Order the sections by reasoning rather than symmetry.
5. List evidence that is supplied, evidence that needs verification, and decisions the writer must make.

### Return

Lead with the working thesis, then the argument map and outline. End with only the material evidence gaps or choices that remain.

## Draft

Draft may begin with a topic, assignment, brief, notes, rubric, sources, or any combination of them.

### When information is incomplete

- If a missing fact would change the argument, ask or mark the gap.
- If a minor convention is missing, infer a sensible default and state it briefly.
- If no length is supplied, write a focused medium-length draft appropriate to the task instead of stalling.
- If the user's position is unknown but the prompt permits several, choose a defensible working position and label it as an assumption.
- Never create a personal anecdote to make the essay feel authentic.

### Evidence boundaries

- Build only on facts supplied by the user or verified through available research.
- Distinguish a source's statement from the essay's inference.
- Do not create a bibliography entry from guessed author, date, title, publisher, DOI, or page details.
- If the user requests a citation style, format only metadata that can be verified.
- Place evidence next to the claim it supports and explain why it matters.
- Preserve meaningful uncertainty and disagreement.

### Return

Return the complete essay first. Add a short `Evidence or assumptions to check` note only when something material remains unresolved.

## Edit

Select a level from [voice-and-editing.md](voice-and-editing.md).

Before changing the draft, identify:

- thesis and main line of reasoning;
- paragraph functions;
- evidence, quotations, citations, and numbers;
- strongest voice markers;
- deliberate fragments, repetition, dialect, or ambiguity;
- assignment constraints.

Revise the weakest layer first. Sentence polish cannot repair a missing argument, and a structural rewrite is unnecessary when the draft needs only proofreading.

Return the revised essay first. Mention major interpretive changes, unresolved evidence, or citation concerns after it.

## Review

Review the essay without silently rewriting it.

### Report shape

1. **Overall reading:** one concise paragraph on what the essay currently achieves.
2. **Prompt and rubric fit:** requirements met, partly met, or missing.
3. **Argument:** thesis, reasoning, counterargument, and implications.
4. **Evidence:** quality, placement, attribution, uncertainty, and citation integrity.
5. **Structure:** paragraph purpose, order, transitions, opening, and ending.
6. **Voice and clarity:** strengths worth preserving and passages that obstruct the reader.
7. **Revision priorities:** the three to five changes with the largest likely benefit.

Quote or point to specific passages. Separate observation from preference. Do not assign a grade unless the user supplies a rubric or grading scale that makes the grade meaningful. When a rubric is supplied, use [rubric-review.md](rubric-review.md) and map each criterion to evidence, status, impact, and priority.

## Evidence

Use [evidence-and-citations.md](evidence-and-citations.md) to build a claim-source ledger or audit citations, quotations, numbers, and source metadata.

Return the ledger and citation findings without silently rewriting the essay. Distinguish supported, partially supported, unsupported, unverified, and not-applicable claims. Never fill missing bibliographic details from memory or pattern matching.

## Research

Use [research-lenses.md](research-lenses.md) when the essay needs external evidence, current information, or a deliberate challenge to consensus.

Return:

1. a scoped research question;
2. the strongest evidence found;
3. a contradiction map;
4. an evidence-weighted synthesis;
5. unresolved questions and source limitations;
6. an essay-ready argument map if requested.

Do not describe analytical lenses as real experts who were consulted.

## Detect

Use [ai-writing-signals.md](ai-writing-signals.md). Detection produces a calibrated report, not a rewrite, accusation, percentage, or model attribution.

If the user also wants an edit, finish and clearly separate the signal report before beginning the edit. Improve the writing for truth, argument, voice, and reader experience, never for detector evasion.

## Pattern

Use [pattern-audit.md](pattern-audit.md) when the user asks for statistical, structural, repetitive, or mechanically regular writing patterns to be identified or repaired.

Pattern mode may describe sentence-shape recurrence, rhythm, transition frequency, paragraph uniformity, rhetorical lists, abstraction, stance markers, vocabulary repetition, and repeated paragraph templates. It may use simple descriptive counts when they were actually measured, but it must not invent statistics or treat a pattern as authorship evidence.

If repair is requested, preserve the writer's meaning, evidence, quotations, citations, numbers, uncertainty, dialect, and purposeful repetition. Do not add mistakes or randomness, and do not promise a detector result.

## Personal statement, Scholarship essay, Lab report, and Literature review

Use [specialized-writing.md](specialized-writing.md). These modes keep the shared evidence and voice rules but use different structures and evidence boundaries. Do not turn a personal statement into a résumé, a scholarship essay into invented hardship, a lab report into a polished result unsupported by data, or a literature review into a list of abstracts.
