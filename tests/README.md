# Behavioural evaluation

This directory separates two different kinds of evidence:

1. `validate_package.py` performs deterministic checks on the repository and
   test specifications. These checks run in continuous integration.
2. The behavioural fixtures describe responses that a human or capable model
   must grade. Static validation cannot prove that an essay is natural, that an
   edit preserves voice, or that an AI-writing assessment is fair.

Passing CI means that the package is internally consistent. It does not mean
that every supported model will produce the same response or that authorship
can be determined from prose.

## Fixture format

`cases/v1.0.json` contains versioned prompts and source material.
`expected/v1.0.json` contains the matching expectations.
The [0.1.0-beta live evaluation report](reports/0.1.0-beta.md) records
manually reviewed runs separately from the static fixture definitions.

Each expectation has two deliberately separate sections:

- `automated_response_checks` records exact strings or patterns that a future
  response runner can check without interpretation.
- `human_or_model_rubric` records semantic criteria that require judgment.

The package validator verifies the fixture schema and the one-to-one mapping
between inputs and expectations. It does not invent a model response or mark a
semantic criterion as passed.

## Run deterministic validation

From the repository root:

```bash
python3 tests/validate_package.py
```

The script uses only the Python standard library.

## Run the official skill check

The GitHub Actions workflow also downloads OpenAI's public
`quick_validate.py` at a pinned commit, verifies its checksum, installs its
PyYAML dependency, and validates `skills/essay-writer`.

## Grade a behavioural case

1. Give the selected case's `input` object to the skill.
2. Save the response outside this repository or in an ignored working folder.
3. Apply every `automated_response_checks` entry literally.
4. Grade every `human_or_model_rubric` entry and record evidence for the score.
5. Treat any failed `critical` criterion as a failed case.

Do not report an aggregate detection-accuracy claim from these fixtures. They
are regression scenarios, not a labelled, representative essay benchmark.
