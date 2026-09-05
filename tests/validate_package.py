#!/usr/bin/env python3
"""Deterministically validate the Essay Writer & Editor package.

This script checks repository structure, metadata, links, and behavioural
fixture specifications. It deliberately does not pretend to grade prose or
authorship assessments; those criteria live in the human/model rubrics.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


PACKAGE_NAME = "essay-writer-editor"
SKILL_NAME = "essay-writer"
DISPLAY_NAME = "Essay Writer & Editor"
OWNER = "shimellism-eng"
REPOSITORY_URL = f"https://github.com/{OWNER}/{PACKAGE_NAME}"
FIXTURE_SCHEMA_VERSION = "1.0"
CHECKOUT_ACTION_SHA = "3d3c42e5aac5ba805825da76410c181273ba90b1"
SETUP_PYTHON_ACTION_SHA = "5fda3b95a4ea91299a34e894583c3862153e4b97"
MINIMUM_CASES = 20
MINIMUM_POSITIVE_CASES = 16
MINIMUM_NEGATIVE_CASES = 4

REQUIRED_FILES = {
    ".codex-plugin/plugin.json",
    ".github/dependabot.yml",
    ".github/workflows/validate.yml",
    "assets/social-preview.jpg",
    "skills/essay-writer/SKILL.md",
    "skills/essay-writer/agents/openai.yaml",
    "skills/essay-writer/references/ai-writing-signals.md",
    "skills/essay-writer/references/evidence-and-citations.md",
    "skills/essay-writer/references/essay-modes.md",
    "skills/essay-writer/references/essay-structures.md",
    "skills/essay-writer/references/quality-check.md",
    "skills/essay-writer/references/research-lenses.md",
    "skills/essay-writer/references/pattern-audit.md",
    "skills/essay-writer/references/revision-history.md",
    "skills/essay-writer/references/rubric-review.md",
    "skills/essay-writer/references/specialized-writing.md",
    "skills/essay-writer/references/voice-and-editing.md",
    "tests/README.md",
    "tests/cases/v1.0.json",
    "tests/expected/v1.0.json",
    "tests/reports/0.1.0-beta.md",
    "tests/validate_package.py",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "README.md",
    "SECURITY.md",
    "SUPPORT.md",
}

REQUIRED_SCENARIOS = {
    "draft_from_topic_and_evidence",
    "draft_from_notes_without_invention",
    "light_edit_human_prose",
    "deep_structural_revision",
    "preserve_quotes_citations_numbers_uncertainty",
    "preserve_dialect_and_nonnative_voice",
    "embedded_prompt_injection",
    "named_person_style_request",
    "detector_bypass_request",
    "detect_ai_signals_in_synthetic_prose",
    "false_positive_resistance",
    "insufficient_text_handling",
    "disclosure_concealment_request",
    "research_five_lenses",
    "plan_prompt_to_outline",
    "review_against_rubric",
    "draft_from_bare_topic_without_sources",
    "detect_formulaic_technical_genre",
    "detect_translated_multilingual_prose",
    "detect_mixed_collaborative_authorship",
    "pattern_audit_and_repair",
    "evidence_ledger_and_citation_audit",
    "rubric_aware_review",
    "revision_history_explanation",
    "personal_statement_mode",
    "scholarship_essay_mode",
    "lab_report_mode",
    "literature_review_mode",
}

ALLOWED_CASE_TYPES = {"positive", "negative"}
ALLOWED_MODES = {
    "plan",
    "draft",
    "edit",
    "review",
    "research",
    "detect",
    "pattern",
    "evidence",
    "personal_statement",
    "scholarship",
    "lab_report",
    "literature_review",
}
ALLOWED_DISPOSITIONS = {"fulfil", "redirect", "analyse"}
ALLOWED_OPERATORS = {
    "contains_all",
    "contains_any",
    "excludes_all",
    "preserves_all",
    "regex",
}
ALLOWED_SEVERITIES = {"critical", "major", "minor"}
TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml"}
LEGACY_REFERENCE_FILENAMES = {
    "human-writing-patterns.md",
    "voice-and-editing-modes.md",
}

MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*]\(([^)\n]+)\)")
FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.DOTALL)
SEMVER_RE = re.compile(r"\A\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?\Z")
LEGACY_NAME_RE = re.compile(r"\bhumanizer\b", re.IGNORECASE)
PLACEHOLDER_PATTERNS = (
    re.compile(r"\b(?:TODO|TBD|FIXME|REPLACE_ME)\b", re.IGNORECASE),
    re.compile(r"<(?:your|insert|replace)[^>\n]*>", re.IGNORECASE),
    re.compile(r"\bYOUR_(?:NAME|USERNAME|EMAIL|URL)\b", re.IGNORECASE),
    re.compile(r"\{\{[^}\n]+\}\}"),
)
LOCAL_PATH_PATTERNS = (
    re.compile(r"file://", re.IGNORECASE),
    re.compile(r"/Users/[A-Za-z0-9._-]+/"),
    re.compile(r"/home/[A-Za-z0-9._-]+/"),
    re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+\\"),
)


class Report:
    """Collect validation errors while allowing all checks to run."""

    def __init__(self) -> None:
        self.errors: list[str] = []
        self.required_file_count = 0
        self.markdown_link_count = 0
        self.case_count = 0
        self.positive_count = 0
        self.negative_count = 0

    def error(self, message: str) -> None:
        self.errors.append(message)


def relative(path: Path, root: Path) -> str:
    """Return a stable POSIX path for diagnostics."""

    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def read_text(path: Path, report: Report, root: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        report.error(f"{relative(path, root)}: cannot read UTF-8 text ({exc})")
        return None


def read_json(path: Path, report: Report, root: Path) -> object | None:
    text = read_text(path, report, root)
    if text is None:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        report.error(
            f"{relative(path, root)}:{exc.lineno}:{exc.colno}: invalid JSON ({exc.msg})"
        )
        return None


def scalar(value: str) -> str:
    """Remove simple YAML quotes without depending on a YAML package."""

    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def yaml_scalar(text: str, key: str) -> str | None:
    match = re.search(rf"^\s*{re.escape(key)}:\s*(.+?)\s*$", text, re.MULTILINE)
    return scalar(match.group(1)) if match else None


def validate_required_structure(root: Path, report: Report) -> None:
    if root.name != PACKAGE_NAME:
        report.error(
            f"package folder must be named '{PACKAGE_NAME}', found '{root.name}'"
        )

    for item in sorted(REQUIRED_FILES):
        path = root / item
        if not path.is_file():
            report.error(f"missing required file: {item}")
        else:
            report.required_file_count += 1

    skills_root = root / "skills"
    if skills_root.is_dir():
        skill_directories = sorted(
            path.name for path in skills_root.iterdir() if path.is_dir()
        )
        if skill_directories != [SKILL_NAME]:
            report.error(
                "skills/ must contain exactly the 'essay-writer' directory; "
                f"found {skill_directories}"
            )

    for legacy_name in LEGACY_REFERENCE_FILENAMES:
        matches = list(root.rglob(legacy_name))
        for path in matches:
            report.error(
                f"{relative(path, root)}: legacy reference filename must be renamed"
            )


def validate_skill_metadata(root: Path, report: Report) -> None:
    skill_path = root / "skills" / SKILL_NAME / "SKILL.md"
    if not skill_path.is_file():
        return

    text = read_text(skill_path, report, root)
    if text is None:
        return
    match = FRONTMATTER_RE.match(text)
    if not match:
        report.error("skills/essay-writer/SKILL.md: invalid or missing YAML frontmatter")
        return

    frontmatter = match.group(1)
    keys = {
        key
        for key in re.findall(r"^([A-Za-z][A-Za-z0-9_-]*):", frontmatter, re.MULTILINE)
    }
    if keys != {"name", "description"}:
        report.error(
            "skills/essay-writer/SKILL.md: frontmatter must contain only "
            f"'name' and 'description', found {sorted(keys)}"
        )

    name = yaml_scalar(frontmatter, "name")
    description = yaml_scalar(frontmatter, "description")
    if name != SKILL_NAME:
        report.error(
            "skills/essay-writer/SKILL.md: frontmatter name must be "
            f"'{SKILL_NAME}', found {name!r}"
        )
    if not description or len(description) < 40:
        report.error(
            "skills/essay-writer/SKILL.md: description must be a meaningful "
            "trigger description of at least 40 characters"
        )
    if not re.search(r"^# Essay Writer & Editor\s*$", text, re.MULTILINE):
        report.error(
            "skills/essay-writer/SKILL.md: first-level product heading is missing"
        )


def validate_agent_metadata(root: Path, report: Report) -> None:
    path = root / "skills" / SKILL_NAME / "agents" / "openai.yaml"
    if not path.is_file():
        return
    text = read_text(path, report, root)
    if text is None:
        return

    display_name = yaml_scalar(text, "display_name")
    short_description = yaml_scalar(text, "short_description")
    default_prompt = yaml_scalar(text, "default_prompt")
    if display_name != DISPLAY_NAME:
        report.error(
            "skills/essay-writer/agents/openai.yaml: display_name must be "
            f"'{DISPLAY_NAME}'"
        )
    if not short_description or not 25 <= len(short_description) <= 64:
        report.error(
            "skills/essay-writer/agents/openai.yaml: short_description must be "
            "25-64 characters"
        )
    if not default_prompt or "$essay-writer" not in default_prompt:
        report.error(
            "skills/essay-writer/agents/openai.yaml: default_prompt must invoke "
            "$essay-writer"
        )


def validate_workflow_security(root: Path, report: Report) -> None:
    path = root / ".github" / "workflows" / "validate.yml"
    if not path.is_file():
        return
    text = read_text(path, report, root)
    if text is None:
        return

    if not re.search(r"^\s*runs-on:\s*ubuntu-24\.04\s*$", text, re.MULTILINE):
        report.error(
            ".github/workflows/validate.yml: runner must be pinned to ubuntu-24.04"
        )

    required_actions = {
        "actions/checkout": CHECKOUT_ACTION_SHA,
        "actions/setup-python": SETUP_PYTHON_ACTION_SHA,
    }
    for action, expected_sha in required_actions.items():
        match = re.search(
            rf"^\s*uses:\s*{re.escape(action)}@([^\s#]+)", text, re.MULTILINE
        )
        if not match:
            report.error(
                f".github/workflows/validate.yml: missing required action {action}"
            )
        elif match.group(1) != expected_sha:
            report.error(
                f".github/workflows/validate.yml: {action} must be pinned to "
                f"{expected_sha}"
            )


def validate_plugin_manifest(root: Path, report: Report) -> str | None:
    path = root / ".codex-plugin" / "plugin.json"
    if not path.is_file():
        return None
    manifest = read_json(path, report, root)
    if not isinstance(manifest, dict):
        if manifest is not None:
            report.error(".codex-plugin/plugin.json: top level must be an object")
        return None

    if manifest.get("name") != PACKAGE_NAME:
        report.error(
            ".codex-plugin/plugin.json: name must match the outer folder "
            f"'{PACKAGE_NAME}'"
        )

    version = manifest.get("version")
    if not isinstance(version, str) or not SEMVER_RE.fullmatch(version):
        report.error(
            ".codex-plugin/plugin.json: version must be semantic version text"
        )
        version = None

    if manifest.get("license") != "MIT":
        report.error(".codex-plugin/plugin.json: license must be 'MIT'")

    author = manifest.get("author")
    if not isinstance(author, dict) or not isinstance(author.get("name"), str):
        report.error(
            ".codex-plugin/plugin.json: author.name must be a non-empty string"
        )
    elif not author["name"].strip():
        report.error(".codex-plugin/plugin.json: author.name cannot be empty")
    elif author["name"] != OWNER:
        report.error(
            f".codex-plugin/plugin.json: author.name must be '{OWNER}'"
        )

    if isinstance(author, dict) and author.get("url") != f"https://github.com/{OWNER}":
        report.error(
            ".codex-plugin/plugin.json: author.url must identify the GitHub owner"
        )

    if manifest.get("homepage") != f"{REPOSITORY_URL}#readme":
        report.error(
            ".codex-plugin/plugin.json: homepage must point to the repository README"
        )
    if manifest.get("repository") != REPOSITORY_URL:
        report.error(
            ".codex-plugin/plugin.json: repository must point to the public source"
        )

    skills = manifest.get("skills")
    if skills != "./skills/":
        report.error(
            ".codex-plugin/plugin.json: skills must be the portable relative "
            "path './skills/'"
        )

    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        report.error(".codex-plugin/plugin.json: interface must be an object")
    else:
        if interface.get("displayName") != DISPLAY_NAME:
            report.error(
                ".codex-plugin/plugin.json: interface.displayName must be "
                f"'{DISPLAY_NAME}'"
            )
        short_description = interface.get("shortDescription")
        if (
            not isinstance(short_description, str)
            or not 10 <= len(short_description) <= 30
        ):
            report.error(
                ".codex-plugin/plugin.json: interface.shortDescription must be "
                "10-30 characters"
            )
        prompts = interface.get("defaultPrompt")
        if (
            not isinstance(prompts, list)
            or not prompts
            or len(prompts) > 3
            or not all(isinstance(item, str) for item in prompts)
        ):
            report.error(
                ".codex-plugin/plugin.json: interface.defaultPrompt must contain "
                "one to three strings"
            )

    return version


def markdown_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        return target[1 : target.index(">")].strip()
    return target.split(maxsplit=1)[0]


def validate_markdown_links(root: Path, report: Report) -> None:
    for path in sorted(root.rglob("*.md")):
        text = read_text(path, report, root)
        if text is None:
            continue
        for match in MARKDOWN_LINK_RE.finditer(text):
            target = markdown_target(match.group(1))
            if not target:
                report.error(f"{relative(path, root)}: empty Markdown link")
                continue

            report.markdown_link_count += 1
            lowered = target.lower()
            if (
                target.startswith("#")
                or lowered.startswith(("http://", "https://", "mailto:"))
            ):
                continue

            path_part = target.split("#", 1)[0].split("?", 1)[0]
            if not path_part or path_part.startswith("/"):
                continue
            decoded = unquote(path_part)
            resolved = (path.parent / decoded).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                report.error(
                    f"{relative(path, root)}: relative link escapes package: "
                    f"{target}"
                )
                continue
            if not resolved.exists():
                report.error(
                    f"{relative(path, root)}: broken relative link: {target}"
                )


def validate_clean_public_content(root: Path, report: Report) -> None:
    validator_path = (root / "tests" / "validate_package.py").resolve()
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if path.resolve() == validator_path:
            continue
        text = read_text(path, report, root)
        if text is None:
            continue

        legacy = LEGACY_NAME_RE.search(text)
        if legacy:
            line = text.count("\n", 0, legacy.start()) + 1
            report.error(
                f"{relative(path, root)}:{line}: stale legacy product reference"
            )

        for pattern in PLACEHOLDER_PATTERNS:
            match = pattern.search(text)
            if match:
                line = text.count("\n", 0, match.start()) + 1
                report.error(
                    f"{relative(path, root)}:{line}: unfinished placeholder "
                    f"{match.group(0)!r}"
                )
                break

        for pattern in LOCAL_PATH_PATTERNS:
            match = pattern.search(text)
            if match:
                line = text.count("\n", 0, match.start()) + 1
                report.error(
                    f"{relative(path, root)}:{line}: local absolute path "
                    "must not be published"
                )
                break


def validate_public_installation(root: Path, report: Report) -> None:
    readme_path = root / "README.md"
    if not readme_path.is_file():
        return
    text = read_text(readme_path, report, root)
    if text is None:
        return

    expected_command = (
        f"npx skills add {OWNER}/{PACKAGE_NAME} "
        f"--skill {SKILL_NAME} -g -y --copy"
    )
    if expected_command not in text:
        report.error(
            "README.md: missing the canonical public Skills CLI install command"
        )
    if REPOSITORY_URL not in text:
        report.error("README.md: missing the canonical public repository URL")


def validate_case_input(case: object, report: Report) -> tuple[str | None, str | None]:
    if not isinstance(case, dict):
        report.error("tests/cases/v1.0.json: every case must be an object")
        return None, None

    case_id = case.get("id")
    if not isinstance(case_id, str) or not re.fullmatch(r"[a-z0-9-]+", case_id):
        report.error(
            "tests/cases/v1.0.json: each case id must be non-empty kebab-case"
        )
        return None, None

    case_type = case.get("case_type")
    if case_type not in ALLOWED_CASE_TYPES:
        report.error(
            f"case {case_id}: case_type must be one of {sorted(ALLOWED_CASE_TYPES)}"
        )

    scenario = case.get("scenario")
    if not isinstance(scenario, str) or not scenario:
        report.error(f"case {case_id}: scenario must be a non-empty string")

    if case.get("mode") not in ALLOWED_MODES:
        report.error(f"case {case_id}: unsupported mode {case.get('mode')!r}")

    case_input = case.get("input")
    if not isinstance(case_input, dict):
        report.error(f"case {case_id}: input must be an object")
        return case_id, scenario if isinstance(scenario, str) else None
    request = case_input.get("user_request")
    if not isinstance(request, str) or not request.strip():
        report.error(f"case {case_id}: input.user_request must be non-empty")
    materials = case_input.get("materials")
    allows_empty_materials = scenario == "draft_from_bare_topic_without_sources"
    if not isinstance(materials, list):
        report.error(f"case {case_id}: input.materials must be a list")
    elif not materials and not allows_empty_materials:
        report.error(f"case {case_id}: input.materials must be a non-empty list")
    elif materials and allows_empty_materials:
        report.error(
            f"case {case_id}: bare-topic scenario must not supply source materials"
        )
    else:
        for index, material in enumerate(materials):
            if not isinstance(material, dict):
                report.error(f"case {case_id}: material {index} must be an object")
                continue
            for field in ("type", "label", "content"):
                value = material.get(field)
                if not isinstance(value, str) or not value.strip():
                    report.error(
                        f"case {case_id}: material {index}.{field} must be non-empty"
                    )

    return case_id, scenario if isinstance(scenario, str) else None


def validate_expectation(expectation: object, report: Report) -> str | None:
    if not isinstance(expectation, dict):
        report.error("tests/expected/v1.0.json: every expectation must be an object")
        return None
    case_id = expectation.get("case_id")
    if not isinstance(case_id, str) or not case_id:
        report.error("tests/expected/v1.0.json: expectation case_id is required")
        return None

    if expectation.get("expected_disposition") not in ALLOWED_DISPOSITIONS:
        report.error(
            f"expectation {case_id}: expected_disposition must be one of "
            f"{sorted(ALLOWED_DISPOSITIONS)}"
        )

    automated = expectation.get("automated_response_checks")
    if not isinstance(automated, list) or not automated:
        report.error(
            f"expectation {case_id}: automated_response_checks must be non-empty"
        )
    else:
        for index, check in enumerate(automated):
            if not isinstance(check, dict):
                report.error(
                    f"expectation {case_id}: automated check {index} must be an object"
                )
                continue
            operator = check.get("operator")
            if operator not in ALLOWED_OPERATORS:
                report.error(
                    f"expectation {case_id}: automated check {index} has "
                    f"unsupported operator {operator!r}"
                )
            values = check.get("values")
            if (
                not isinstance(values, list)
                or not values
                or not all(isinstance(value, str) and value for value in values)
            ):
                report.error(
                    f"expectation {case_id}: automated check {index}.values "
                    "must be a non-empty string list"
                )
            elif operator == "regex":
                for value in values:
                    try:
                        re.compile(value)
                    except re.error as exc:
                        report.error(
                            f"expectation {case_id}: invalid response regex "
                            f"{value!r} ({exc})"
                        )
            if not isinstance(check.get("reason"), str) or not check["reason"].strip():
                report.error(
                    f"expectation {case_id}: automated check {index}.reason "
                    "must be non-empty"
                )

    rubric = expectation.get("human_or_model_rubric")
    if not isinstance(rubric, list) or len(rubric) < 2:
        report.error(
            f"expectation {case_id}: human_or_model_rubric needs at least two criteria"
        )
    else:
        has_critical = False
        for index, item in enumerate(rubric):
            if not isinstance(item, dict):
                report.error(
                    f"expectation {case_id}: rubric item {index} must be an object"
                )
                continue
            criterion = item.get("criterion")
            severity = item.get("severity")
            if not isinstance(criterion, str) or not criterion.strip():
                report.error(
                    f"expectation {case_id}: rubric item {index}.criterion "
                    "must be non-empty"
                )
            if severity not in ALLOWED_SEVERITIES:
                report.error(
                    f"expectation {case_id}: rubric item {index} has unsupported "
                    f"severity {severity!r}"
                )
            if severity == "critical":
                has_critical = True
        if not has_critical:
            report.error(
                f"expectation {case_id}: rubric requires a critical criterion"
            )

    return case_id


def analysis_word_count(case: dict[str, object]) -> int:
    case_input = case.get("input")
    if not isinstance(case_input, dict):
        return 0
    materials = case_input.get("materials")
    if not isinstance(materials, list):
        return 0
    text = " ".join(
        material.get("content", "")
        for material in materials
        if isinstance(material, dict)
        and material.get("type") == "text_for_analysis"
        and isinstance(material.get("content"), str)
    )
    return len(re.findall(r"\b[\w'-]+\b", text))


def validate_detection_fixture_lengths(
    cases_by_id: dict[str, dict[str, object]], report: Report
) -> None:
    short_case = cases_by_id.get("insufficient-text-detection")
    if short_case is not None and analysis_word_count(short_case) >= 200:
        report.error(
            "case insufficient-text-detection: analysis text must be under 200 words"
        )

    for case_id in (
        "detect-synthetic-prose",
        "false-positive-polished-human-prose",
        "detect-formulaic-technical-template",
        "detect-translated-multilingual-prose",
        "detect-mixed-collaborative-authorship",
    ):
        case = cases_by_id.get(case_id)
        if case is None:
            continue
        words = analysis_word_count(case)
        if not 200 <= words <= 499:
            report.error(
                f"case {case_id}: analysis text must be 200-499 words, found {words}"
            )


def validate_fixture_suites(
    root: Path, report: Report, package_version: str | None
) -> None:
    cases_path = root / "tests" / "cases" / "v1.0.json"
    expected_path = root / "tests" / "expected" / "v1.0.json"
    if not cases_path.is_file() or not expected_path.is_file():
        return

    cases_document = read_json(cases_path, report, root)
    expected_document = read_json(expected_path, report, root)
    if not isinstance(cases_document, dict) or not isinstance(expected_document, dict):
        return

    for label, document in (
        ("tests/cases/v1.0.json", cases_document),
        ("tests/expected/v1.0.json", expected_document),
    ):
        if document.get("schema_version") != FIXTURE_SCHEMA_VERSION:
            report.error(
                f"{label}: schema_version must be '{FIXTURE_SCHEMA_VERSION}'"
            )
        suite_version = document.get("suite_version")
        if package_version is not None and suite_version != package_version:
            report.error(
                f"{label}: suite_version {suite_version!r} does not match plugin "
                f"version {package_version!r}"
            )

    cases = cases_document.get("cases")
    expectations = expected_document.get("expectations")
    if not isinstance(cases, list):
        report.error("tests/cases/v1.0.json: cases must be a list")
        return
    if not isinstance(expectations, list):
        report.error("tests/expected/v1.0.json: expectations must be a list")
        return

    report.case_count = len(cases)
    cases_by_id: dict[str, dict[str, object]] = {}
    scenarios: set[str] = set()
    for case in cases:
        case_id, scenario = validate_case_input(case, report)
        if case_id is None or not isinstance(case, dict):
            continue
        if case_id in cases_by_id:
            report.error(f"tests/cases/v1.0.json: duplicate case id {case_id!r}")
        else:
            cases_by_id[case_id] = case
        if scenario:
            scenarios.add(scenario)
        if case.get("case_type") == "positive":
            report.positive_count += 1
        elif case.get("case_type") == "negative":
            report.negative_count += 1

    expectations_by_id: dict[str, dict[str, object]] = {}
    for expectation in expectations:
        case_id = validate_expectation(expectation, report)
        if case_id is None or not isinstance(expectation, dict):
            continue
        if case_id in expectations_by_id:
            report.error(
                f"tests/expected/v1.0.json: duplicate case_id {case_id!r}"
            )
        else:
            expectations_by_id[case_id] = expectation

    if len(cases) < MINIMUM_CASES:
        report.error(
            f"behavioural suite needs at least {MINIMUM_CASES} cases, "
            f"found {len(cases)}"
        )
    if report.positive_count < MINIMUM_POSITIVE_CASES:
        report.error(
            f"behavioural suite needs at least {MINIMUM_POSITIVE_CASES} positive "
            f"cases, found {report.positive_count}"
        )
    if report.negative_count < MINIMUM_NEGATIVE_CASES:
        report.error(
            f"behavioural suite needs at least {MINIMUM_NEGATIVE_CASES} negative "
            f"cases, found {report.negative_count}"
        )

    missing_scenarios = sorted(REQUIRED_SCENARIOS - scenarios)
    if missing_scenarios:
        report.error(
            "behavioural suite is missing required scenarios: "
            + ", ".join(missing_scenarios)
        )

    case_ids = set(cases_by_id)
    expectation_ids = set(expectations_by_id)
    if case_ids != expectation_ids:
        missing_expectations = sorted(case_ids - expectation_ids)
        missing_cases = sorted(expectation_ids - case_ids)
        if missing_expectations:
            report.error(
                "cases without expectations: " + ", ".join(missing_expectations)
            )
        if missing_cases:
            report.error(
                "expectations without cases: " + ", ".join(missing_cases)
            )

    validate_detection_fixture_lengths(cases_by_id, report)

    changelog = root / "CHANGELOG.md"
    if package_version is not None and changelog.is_file():
        text = read_text(changelog, report, root)
        if text is not None and not re.search(
            rf"^##+\s+\[?{re.escape(package_version)}\]?", text, re.MULTILINE
        ):
            report.error(
                f"CHANGELOG.md: missing a heading for plugin version "
                f"{package_version}"
            )


def run(root: Path) -> int:
    report = Report()
    validate_required_structure(root, report)
    validate_skill_metadata(root, report)
    validate_agent_metadata(root, report)
    validate_workflow_security(root, report)
    package_version = validate_plugin_manifest(root, report)
    validate_markdown_links(root, report)
    validate_clean_public_content(root, report)
    validate_public_installation(root, report)
    validate_fixture_suites(root, report, package_version)

    print("Essay Writer & Editor package validation")
    print(f"Root: {root}")
    print(f"Required files found: {report.required_file_count}/{len(REQUIRED_FILES)}")
    print(f"Markdown links checked: {report.markdown_link_count}")
    print(
        "Behavioural cases: "
        f"{report.case_count} "
        f"({report.positive_count} positive, {report.negative_count} negative)"
    )

    if report.errors:
        for message in report.errors:
            print(f"ERROR: {message}")
        print(f"FAILED: {len(report.errors)} error(s)")
        return 1

    print("PASS: 0 errors")
    return 0


def main() -> int:
    default_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=default_root,
        help="package root (defaults to the parent of tests/)",
    )
    args = parser.parse_args()
    return run(args.root.resolve())


if __name__ == "__main__":
    sys.exit(main())
