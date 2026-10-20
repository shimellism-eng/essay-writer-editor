#!/usr/bin/env python3
"""Turn a plain-text statement into a clean Word (.docx) file.

Usage:
    python3 make_docx.py STATEMENT.txt OUTPUT.docx [--title TEXT] [--subtitle TEXT]

Paragraphs in STATEMENT.txt are separated by blank lines. The file uses
Times New Roman 12 pt, justified paragraphs and an optional centred title.
It is built from scratch with the standard library, so it carries no author,
company, software or editing-history metadata.
"""

from __future__ import annotations

import argparse
import re
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""

ROOT_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

DOC_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults>
<w:rPrDefault><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="Times New Roman" w:cs="Times New Roman"/><w:sz w:val="24"/><w:szCs w:val="24"/><w:lang w:val="en-US"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:after="200" w:line="336" w:lineRule="auto"/></w:pPr></w:pPrDefault>
</w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>
</w:styles>"""

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def paragraph(text: str, align: str = "both", bold: bool = False, size: int | None = None,
              after: int | None = None) -> str:
    run_props = ""
    if bold or size:
        run_props = "<w:rPr>" + ("<w:b/>" if bold else "") + (
            f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>' if size else "") + "</w:rPr>"
    spacing = f'<w:spacing w:after="{after}"/>' if after is not None else ""
    return (
        f'<w:p><w:pPr><w:jc w:val="{align}"/>{spacing}</w:pPr>'
        f'<w:r>{run_props}<w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>'
    )


def build(paragraphs: list[str], title: str | None, subtitle: str | None) -> str:
    body = []
    if title:
        body.append(paragraph(title, "center", bold=True, size=28, after=60))
    if subtitle:
        body.append(paragraph(subtitle, "center", after=280))
    body += [paragraph(p) for p in paragraphs]
    section = ('<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
               '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
               'w:header="708" w:footer="708" w:gutter="0"/></w:sectPr>')
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<w:document xmlns:w="{W_NS}"><w:body>{"".join(body)}{section}</w:body></w:document>')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--title")
    parser.add_argument("--subtitle")
    args = parser.parse_args()
    text = args.source.read_text(encoding="utf-8")
    paragraphs = [re.sub(r"\s*\n\s*", " ", p).strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    fixed_time = (2000, 1, 1, 0, 0, 0)
    with zipfile.ZipFile(args.output, "w", zipfile.ZIP_DEFLATED) as docx:
        for name, data in [
            ("[Content_Types].xml", CONTENT_TYPES),
            ("_rels/.rels", ROOT_RELS),
            ("word/_rels/document.xml.rels", DOC_RELS),
            ("word/styles.xml", STYLES),
            ("word/document.xml", build(paragraphs, args.title, args.subtitle)),
        ]:
            info = zipfile.ZipInfo(name, date_time=fixed_time)
            info.compress_type = zipfile.ZIP_DEFLATED
            docx.writestr(info, data)
    words = len(re.findall(r"[A-Za-z0-9'’-]+", " ".join(paragraphs)))
    print(f"Wrote {args.output} ({len(paragraphs)} paragraphs, {words} words, no metadata)")


if __name__ == "__main__":
    main()
