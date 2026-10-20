# Changelog

All notable changes to Essay Writer & Editor will be recorded in this file.

This project follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html) once a stable release is available. Beta releases may still change behaviour and documentation between minor versions.

## [Unreleased]

### Added

- Pattern audit and repair mode for recurring statistical or structural prose patterns, with descriptive-count and detector-evasion safeguards.
- Evidence ledger and citation audit mode for source-bounded claims, quotations, numbers, metadata and support gaps.
- Rubric-aware review with criterion-level evidence mapping and prioritised revision actions.
- Optional revision histories that describe observable material changes without exposing hidden reasoning.
- Personal statement, scholarship essay, lab report and literature review modes with specialised evidence boundaries.
- Formula-habit checklist for pattern repair (repeated reflective verbs, motto sentences, set-up sentences, colon reveals, stock vocabulary, promotional superlatives, triad stacking) with measure-before-claiming guidance.
- Rules for adapting a personal statement to a new programme using only the supplied statement and official programme information.
- Natural human voice by default for every draft and revision, including writing from facts alone; adapted statements reuse the writer's sentences only where they already read naturally.
- Ordered method for cutting to a word limit that removes repetition first, protects supporting facts, and reports before-and-after counts.

### Planned

- Feedback from public beta users and additional agent compatibility checks.
- A labelled, versioned essay evaluation set before any detection-accuracy claim is considered.

## [0.1.0-beta] - 2026-07-27

### Added

- Plan, Draft, Edit, Review, Research, Detect, Pattern, Evidence and specialised writing modes.
- Complete essay drafting from a prompt, topic, rubric, notes or supplied sources.
- Light, standard and deep editing while protecting the writer's position and voice.
- Evidence safeguards for facts, quotations, citations, numbers and uncertainty.
- Multi-perspective research through practitioner, academic, skeptic, incentives and historian lenses.
- Conservative AI-writing signal analysis with evidence, counterevidence and limitations.
- Protections for dialect, code-switching, regional spelling and non-native voice.
- Behavioural fixtures for drafting, editing, factual integrity, prompt injection, unsafe requests and detection limits.
- Codex skill metadata, plugin packaging and deterministic repository validation.
- Installation, contribution, support, security and community documentation.
- Direct GitHub installation through the Skills CLI.
- Public repository metadata, validation badges and social-preview artwork.

### Safety

- Detection is presented as a writing-pattern assessment, not proof of authorship.
- The skill declines detector-bypass, disclosure-concealment, fabricated-source and invented-experience requests.
- Fewer than 200 words normally produces an insufficient-text result in Detect mode.
