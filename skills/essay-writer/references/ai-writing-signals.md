# AI-writing signal analysis

Use this reference only when the user explicitly asks whether a passage shows signs associated with AI-generated writing.

## Scope

Text-only analysis cannot verify authorship. A human can write highly regular prose, an AI can produce irregular prose, and editing can mix both. This mode identifies patterns worth examining and explains uncertainty.

Do not:

- claim that an assessment proves who or what wrote the text;
- return an “AI percentage” or probability;
- infer a particular model from stylistic stereotypes;
- decide from one word, phrase, punctuation mark, transition, or grammatical error;
- treat non-native English, dialect, formal register, or clean grammar as evidence of AI use;
- recommend disciplinary, admissions, employment, publication, or legal action from the report alone;
- rewrite toward a detector score.

## Evidence hierarchy

Keep three kinds of evidence separate:

1. **Direct provenance:** supplied edit history, generation logs, metadata, or an explicit chatbot artefact.
2. **Source relationship:** whether the text accurately and specifically engages its prompt, sources, quotations, and evidence.
3. **Writing patterns:** recurring structural, rhetorical, and linguistic features within the passage.

Direct provenance can support a stronger conclusion about process. Writing patterns alone cannot.

## Minimum text and confidence

- Fewer than 200 words normally yields `insufficient text`. Report an obvious artefact if present, but do not convert it into an authorship verdict.
- From 200 to 499 words, writing patterns alone cannot exceed `low` confidence.
- At 500 words or more, use `moderate` confidence only when several independent signals recur across the piece and counterevidence is limited.
- Reserve `high` confidence for direct provenance evidence. Style alone never qualifies.
- Reduce confidence for translated, collaboratively written, heavily edited, formulaic, highly technical, multilingual, or mixed-authorship text.

Word count is an evidence threshold, not a promise that longer text is reliably detectable.

## Analyse clusters, not quirks

### Structure and paragraph function

Look for repeated paragraph templates, mechanically balanced sections, identical topic-sentence patterns, serial mini-conclusions, or an introduction and conclusion that restate one another with little development.

Counterevidence may include purposeful changes of pace, paragraph functions shaped by the argument, or irregularity that clearly serves meaning. Randomness by itself is not human evidence.

### Explanation and reader trust

Look for a point being stated, paraphrased, moralised, and summarised after it is already clear. Notice conclusions that explain the lesson rather than earning it.

Counterevidence may include necessary repetition in teaching, accessibility, legal, technical, or high-stakes writing.

### Specificity and source use

Look for vague authorities, unnamed studies, generic examples, unsupported precision, or citations that do not support the nearby claim. Check whether the essay meaningfully responds to supplied sources rather than merely mentioning them.

Counterevidence may include accurate names, bounded examples, source-specific reasoning, and honest limits. Specificity is useful only when it is supported.

### Rhythm and rhetorical recurrence

Look for persistent uniformity in sentence length, clause shape, transition language, triads, headings, and closing sentences. Note generic enthusiasm, emotional labels without observed detail, and repeated contrast formulas.

Counterevidence may include a consistent genre requirement or a writer's demonstrated personal habit. Never use an em dash, semicolon, contraction, fragment, or preferred word as a verdict.

### Voice and decisions

Look for a speaker who never makes a bounded judgement, reveals a priority, takes an intellectual risk, or chooses among competing interpretations. Notice essays that remain polished but noncommittal.

Counterevidence may include a stable vocabulary, distinctive but relevant compression, defensible preferences, and choices connected to the writer's evidence. Do not confuse identity markers or errors with authenticity.

### Interface artefacts

Report leaked phrases such as an unedited assistant preamble, refusal, instruction echo, citation token, placeholder, or formatting residue. Quote the exact artefact.

An artefact may show that an AI tool touched the document. It does not establish how much of the essay was generated or whether the use was permitted.

## Decide the assessment

Use one label:

- **`insufficient text`:** too little or unsuitable material for a meaningful pattern assessment.
- **`human-leaning`:** individual, source-connected decisions outweigh the observed AI-associated patterns.
- **`mixed or uncertain`:** signals conflict, are weak, or fit ordinary genre and editing conventions.
- **`AI-leaning`:** multiple independent signals recur across the text and plausible genre explanations do not account for them.

`Human-leaning` does not certify human authorship. `AI-leaning` does not prove AI authorship.

## Report format

### Assessment

State the label and permitted confidence level in one sentence.

### Evidence

Give two to five strongest observations. Quote short passages and explain the pattern. Prefer evidence from different categories.

### Counterevidence

Give the strongest features that weigh against the assessment or offer an ordinary alternative explanation.

### Limitations

State the text length and relevant conditions such as translation, technical genre, collaboration, editing, or missing provenance.

### Suggested next step

Recommend a proportionate check: compare the essay with notes and sources, inspect version history, ask the writer to explain key decisions, or discuss permitted AI use. If the user owns the essay, offer an ordinary evidence, argument, and voice edit without promising detector outcomes.

## Method boundary

Research on long-form narrative structure suggests that model outputs can exhibit recurring structural patterns. That result does not establish reliable detection for essays, new models, edited work, or individual high-stakes decisions. Keep the method scoped to transparent heuristic review until a labelled, versioned, essay-specific benchmark supports stronger claims.

## Research notes

- [StoryScope: Investigating idiosyncrasies in AI fiction](https://arxiv.org/abs/2604.03136) reports strong classification from discourse-level features in a controlled corpus of roughly 5,000-word fictional stories. Its 93.2% macro-F1 result is specific to that dataset and does not validate this skill on essays.
- [A Large Scale Social Web Audit of AI Generated Text Detection Systems](https://doi.org/10.1609/icwsm.v20i1.42660) reports considerable false positives and unequal flagging patterns in an in-the-wild audit, reinforcing the need for counterevidence and non-punitive use.
- [Findings of the Counter Turing Test: AI-Generated Text Detection](https://arxiv.org/abs/2605.20761) shows that controlled shared-task performance can be high while cross-domain generalisation, adversarial robustness, and model attribution remain separate challenges.

These sources motivate the feature categories and cautions. They are not an accuracy evaluation of Essay Writer & Editor.
