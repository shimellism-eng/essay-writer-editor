#!/usr/bin/env python3
"""Check a statement or essay draft for formula habits, rhythm, repetition,
length and untraced facts.

Usage:
    python3 check_statement.py DRAFT.txt [--limit 800-900] [--source FILE ...]

DRAFT.txt is plain text with paragraphs separated by blank lines.
--limit gives a target word range (or a single maximum).
--source names the files every fact must trace to: the writer's original
statement or CV, and the notes taken from official programme pages.

The counts are descriptive. They show where to look; they do not measure
authorship and cannot predict any detector's result.
Exit status is 1 when any check fails, otherwise 0.
"""

from __future__ import annotations

import argparse
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

STOCK_WORDS = [
    "passion", "passionate", "delve", "pivotal", "invaluable", "perfectly",
    "moreover", "furthermore", "additionally", "tapestry", "testament",
    "seamless", "seamlessly", "leverage", "leveraging", "foster", "fostering",
    "realm", "landscape", "journey", "robust", "crucial", "vital",
    "unwavering", "meticulous", "embark", "navigate the", "ever-evolving",
    "in today's", "rapidly changing", "it is important to note",
    "plays a crucial role", "perfectly aligns", "aligns perfectly",
    "dream", "ignited", "sparked my interest", "deeply resonated",
]
SUPERLATIVES = [
    r"no\.\s?1\b", r"number one", r"globally leading", r"world-leading",
    r"world-class", r"leading (?:firm|company|group|institution) in",
    r"top \d+ (?:firm|network|company)", r"prestigious", r"renowned",
]
COLON_REVEAL = re.compile(
    r"\b(?:one|a single|the same|a simple|the key|a clear)\s+"
    r"(?:principle|lesson|thing|truth|idea|question|goal|conclusion|insight)\s*:",
    re.IGNORECASE,
)
MOTTO = re.compile(
    r"only as \w+ as|is not just .{1,60}[;,] (?:it|they) (?:is|are)|"
    r"\bat its core\b|\bthe key to\b|\bmore than just\b",
    re.IGNORECASE,
)
REFLECTIVE = re.compile(
    r"\b(?:showed|shown|taught|made) me\b|\bmade me reali[sz]e\b|"
    r"\bhelped me (?:understand|realise|realize)\b",
    re.IGNORECASE,
)
INSIGHT = re.compile(
    r"\bI (?:came to see|now see|realized|realised|believe|expect|"
    r"understood|learned|learnt)\b",
    re.IGNORECASE,
)
SENTENCE_SPLIT = re.compile(r"(?<=[.?!])[\"”']?\s+(?=[A-Z\"“(])")
NAME_RUN = re.compile(
    r"\b(?:[A-Z][\w&().'-]*|of|and|the|for|de)"
    r"(?:\s+(?:[A-Z][\w&().'-]*|of|and|the|for|de))+"
)
NUMBER = re.compile(r"\d[\d,]*(?:\.\d+)?(?:/\d+)?%?")
QUOTED = re.compile(r"[\"“]([^\"”]{6,})[\"”]")
SENTENCE_STARTERS = {
    "I", "The", "A", "An", "In", "At", "My", "When", "This", "That", "These",
    "Those", "It", "Among", "After", "Before", "During", "Through", "With",
    "As", "Most", "Another", "Over", "Outside", "Apart", "Still", "From",
    "Comparing", "Serving", "Roles", "Our", "We", "Its", "Their", "Since",
}
LINK_WORDS = {"of", "and", "the", "for", "de"}


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9'’-]+", text)


def norm(text: str) -> str:
    text = text.replace("’", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", text).lower()


def sentences(paragraph: str) -> list[str]:
    return [s.strip() for s in SENTENCE_SPLIT.split(paragraph) if s.strip()]


def parse_limit(value: str | None) -> tuple[int, int] | None:
    if not value:
        return None
    if "-" in value:
        low, high = value.split("-", 1)
        return int(low), int(high)
    return 0, int(value)


class Report:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, str]] = []

    def add(self, status: str, name: str, detail: str) -> None:
        self.rows.append((status, name, detail))

    @property
    def failed(self) -> bool:
        return any(status == "FAIL" for status, _, _ in self.rows)

    def print(self) -> None:
        width = max(len(name) for _, name, _ in self.rows)
        for status, name, detail in self.rows:
            print(f"{status:<4}  {name:<{width}}  {detail}")
        counts = Counter(status for status, _, _ in self.rows)
        print(
            f"\n{counts['PASS']} pass, {counts['WARN']} to review, "
            f"{counts['FAIL']} fail"
        )


def found(pattern_list: list[str], text: str) -> list[str]:
    hits = []
    for item in pattern_list:
        pattern = item if any(c in item for c in "\\[(") else r"\b" + re.escape(item) + r"\b"
        hits += [m.group(0) for m in re.finditer(pattern, text, re.IGNORECASE)]
    return hits


def short_list(items: list[str], limit: int = 4) -> str:
    shown = "; ".join(f'"{i}"' for i in items[:limit])
    return shown + (f" (+{len(items) - limit} more)" if len(items) > limit else "")


def check(draft: str, limit: tuple[int, int] | None, sources: list[str]) -> Report:
    report = Report()
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", draft) if p.strip()]
    all_sentences = [s for p in paragraphs for s in sentences(p)]
    total = len(words(draft))

    # Length
    if limit:
        low, high = limit
        ok = low <= total <= high
        report.add("PASS" if ok else "FAIL", "Word count", f"{total} (target {low}-{high})")
    else:
        report.add("PASS", "Word count", f"{total} (no target given)")

    # Punctuation and vocabulary
    dashes = draft.count("—")
    report.add("FAIL" if dashes else "PASS", "Em dashes", str(dashes))
    stock = found(STOCK_WORDS, draft)
    report.add("FAIL" if stock else "PASS", "Stock vocabulary", short_list(stock) if stock else "none")
    sup = found(SUPERLATIVES, draft)
    report.add("FAIL" if sup else "PASS", "Promotional superlatives", short_list(sup) if sup else "none")

    # Formula habits
    reveals = [m.group(0) for m in COLON_REVEAL.finditer(draft)]
    report.add("FAIL" if reveals else "PASS", "Colon reveals", short_list(reveals) if reveals else "none")
    mottos = [s for s in all_sentences if MOTTO.search(s)]
    report.add("WARN" if mottos else "PASS", "Motto sentences", short_list(mottos, 2) if mottos else "none")
    reflective = [m.group(0) for m in REFLECTIVE.finditer(draft)]
    report.add("WARN" if len(reflective) > 3 else "PASS", "Reflective verbs", f"{len(reflective)} (review above 3)")
    insight = [m.group(0) for m in INSIGHT.finditer(draft)]
    report.add("WARN" if len(insight) > 3 else "PASS", "Insight openers", f"{len(insight)} (review above 3)")
    setups = [
        s for s in all_sentences
        if len(words(s)) <= 9 and not NUMBER.search(s)
        and not re.search(r"\b[A-Z]{2,}|\b[A-Z][a-z]+\s+[A-Z]", s[1:])
    ]
    report.add("WARN" if setups else "PASS", "Short set-up sentences", short_list(setups, 3) if setups else "none")

    # Rhythm and openings
    lengths = [len(words(s)) for s in all_sentences]
    if len(lengths) >= 5:
        spread = statistics.pstdev(lengths)
        report.add(
            "WARN" if spread < 5 else "PASS",
            "Sentence rhythm",
            f"{len(lengths)} sentences, {min(lengths)}-{max(lengths)} words, "
            f"mean {statistics.mean(lengths):.1f}, spread {spread:.1f} (review below 5)",
        )
    openers = Counter(" ".join(words(s)[:2]).lower() for s in all_sentences)
    common, count = openers.most_common(1)[0] if openers else ("", 0)
    share = count / max(len(all_sentences), 1)
    report.add(
        "WARN" if share > 0.2 and count > 3 else "PASS",
        "Repeated openings",
        f'most common "{common}" x{count}',
    )
    triad = re.compile(r"\b[\w-]+(?: [\w-]+){0,3}, [\w-]+(?: [\w-]+){0,3},? and [\w-]+")
    heavy = [i + 1 for i, p in enumerate(paragraphs) if len(triad.findall(p)) > 2]
    report.add(
        "WARN" if heavy else "PASS",
        "Lists of three",
        f"paragraphs {heavy} have more than two" if heavy else "no paragraph has more than two",
    )

    # Repetition across paragraphs
    where: dict[tuple[str, ...], set[int]] = defaultdict(set)
    for i, p in enumerate(paragraphs):
        tokens = [w.lower() for w in words(p)]
        for j in range(len(tokens) - 4):
            gram = tuple(tokens[j:j + 5])
            if sum(len(t) > 3 for t in gram) >= 3:
                where[gram].add(i)
    repeats = sorted({" ".join(g) for g, ps in where.items() if len(ps) > 1})
    report.add(
        "WARN" if repeats else "PASS",
        "Repeated phrases",
        short_list(repeats, 3) if repeats else "no 5-word phrase repeats across paragraphs",
    )

    # Fact lock
    if sources:
        pool = norm(" ".join(sources))
        pool_digits = re.sub(r"[,\s]", "", pool)
        missing_numbers = sorted({
            n for n in NUMBER.findall(draft)
            if re.sub(r"[,\s]", "", n.lower()) not in pool_digits
        })
        report.add(
            "FAIL" if missing_numbers else "PASS",
            "Fact lock: numbers",
            "untraced: " + ", ".join(missing_numbers) if missing_numbers else "all traced to sources",
        )
        names = set()
        for m in (m for s in all_sentences for m in NAME_RUN.finditer(s)):
            parts = m.group(0).rstrip(".,;:").split()
            while parts and (parts[0] in SENTENCE_STARTERS or parts[0] in LINK_WORDS):
                parts = parts[1:]
            while parts and parts[-1] in LINK_WORDS:
                parts = parts[:-1]
            if len(parts) >= 2:
                names.add(" ".join(parts))
        for sentence in all_sentences:
            for token in re.findall(r"[A-Za-z][\w&()'-]*", sentence)[1:]:
                token = re.sub(r"['’]s$", "", token)
                if token.count("(") != token.count(")"):
                    token = token.strip("()")
                if token[:1].isupper() and token != "I" and len(token) > 1:
                    names.add(token)
        names |= set(QUOTED.findall(draft))
        missing_names = sorted(
            n for n in names
            if not re.search(r"(?<![a-z0-9])" + re.escape(norm(n).strip(" ,.")) + r"(?![a-z0-9])", pool)
        )
        report.add(
            "WARN" if missing_names else "PASS",
            "Fact lock: names and titles",
            "check: " + short_list(missing_names, 6) if missing_names else "all traced to sources",
        )
    else:
        report.add("WARN", "Fact lock", "no --source given; facts not checked")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("draft", type=Path)
    parser.add_argument("--limit", help="word range such as 800-900, or a maximum such as 1000")
    parser.add_argument("--source", type=Path, nargs="*", default=[])
    args = parser.parse_args()
    draft = args.draft.read_text(encoding="utf-8")
    sources = [p.read_text(encoding="utf-8", errors="replace") for p in args.source]
    report = check(draft, parse_limit(args.limit), sources)
    report.print()
    return 1 if report.failed else 0


if __name__ == "__main__":
    sys.exit(main())
