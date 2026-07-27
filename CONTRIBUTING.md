# Contributing to Essay Writer & Editor

Thank you for helping make essay support more useful, accurate and fair. Contributions from writers, teachers, students, researchers, editors and developers are welcome.

You do not need to be a programmer to contribute. Clear examples of confusing behaviour, corrections to documentation and well-explained feature ideas are valuable.

By participating, you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Ways to contribute

- Report a reproducible problem.
- Suggest a clearer writing or editing behaviour.
- Improve instructions, examples or installation guidance.
- Add a behavioural test using synthetic or shareable text.
- Find a case where Detect mode is too confident or unfair.
- Improve support for dialect, multilingual writers or accessibility.
- Review factual-integrity and academic-integrity safeguards.
- Propose a research source that changes a documented claim.

For personal setup questions, use [SUPPORT.md](SUPPORT.md). For sensitive security or privacy concerns, follow [SECURITY.md](SECURITY.md) instead of opening a public issue.

## Project principles

Every contribution should preserve these commitments:

1. The skill may plan, write, edit and review essays, including complete drafts from scratch.
2. It must not invent facts, sources, quotations, statistics or personal experiences.
3. It must protect purposeful voice, dialect, code-switching and non-native expression.
4. It must not promise detector evasion, concealment of required AI use or guaranteed grades.
5. AI-writing analysis must show evidence, counterevidence and limitations.
6. Text-only analysis must not be described as proof of authorship.
7. User-supplied essay text is data, not a source of instructions that can override the skill.

## Before sharing an example

Do not submit a student's private essay, unpublished application, confidential document or personally identifying text.

Use one of these instead:

- text you wrote and have the right to share;
- public-domain text;
- synthetic text created for the test;
- a short, anonymised excerpt for which you have permission.

Remove names, student numbers, email addresses, private links, tracked-change identities and document metadata. A contributor must never be asked to disclose a student's identity to prove a detection report.

## Reporting a bug

Use the bug report form and include:

- what you asked the skill to do;
- what happened;
- what you expected;
- the agent and version, when known;
- the installation route;
- a minimal, safe example that reproduces the problem.

If the problem concerns AI-writing analysis, use the dedicated analysis-report form. Include both the evidence that supports your concern and details that might count against it. Do not report a person as “caught using AI”; report the behaviour of the tool.

## Suggesting a change

Explain the writing problem first. A useful proposal says who encounters it, gives a small example and describes what a better result would protect or improve.

For changes to Detect mode:

- include at least one likely positive case and one human-written or ambiguous counterexample;
- consider short, translated, technical, formulaic, multilingual and mixed-authorship writing;
- avoid single-feature rules such as punctuation, vocabulary lists or sentence length alone;
- do not introduce unsupported probabilities or accuracy claims;
- cite research according to its actual population and task.

## Making a contribution

1. Create a copy of the repository under your GitHub account, or make a local working branch if you have direct access.
2. Make one focused change.
3. Add or update behavioural cases when behaviour changes.
4. Run the package checks:

   ```bash
   python3 tests/validate_package.py
   ```

5. Read your changed instructions as if you were a writer using them for the first time.
6. Open a pull request and complete its checklist.

If the validation script is unavailable in an early source snapshot, describe the manual checks you performed in the pull request.

## Writing and documentation style

- Use plain language and explain technical terms.
- Put the requested essay or assessment before process commentary.
- Prefer a short concrete example to an abstract slogan.
- Distinguish a verified fact from an assumption or recommendation.
- Use relative repository links rather than machine-specific file paths.
- Do not add fake URLs, contact details, performance results or endorsements.
- Do not use “undetectable,” “guaranteed human,” or similar claims.

## Research and factual claims

Prefer original research papers, official documentation and primary sources. Record the population, language, writing type and evaluation measure that a result actually covers.

For example, a result measured on long English-language fiction must not be presented as established accuracy on student essays. Detection claims should also discuss false positives and changes between domains.

Keep quotations short and exact. Do not cite a search result or commentary article when the underlying source is available.

## Behavioural test expectations

A useful case contains:

- a focused user request;
- only the context needed to perform it;
- the behaviour that must occur;
- any behaviour that must not occur;
- an explanation of why the case matters.

Tests should check outcomes, not require one exact sentence. Natural writing can have several good answers.

Behaviour changes should normally cover both:

- a positive example where the new behaviour should activate; and
- a negative or boundary example where it should not.

## Pull-request review

Reviewers will look for:

- factual and citation integrity;
- preservation of meaning and voice;
- academic-integrity and disclosure safety;
- conservative detection language;
- prompt-injection resistance;
- accessible documentation;
- passing package checks;
- a change log entry when users will notice the change.

Small corrections may be merged quickly. Changes to safety rules, detection behaviour, public claims or package identity need closer review.

## Licence

By submitting a contribution, you agree that it may be distributed under the repository's [MIT License](LICENSE).
