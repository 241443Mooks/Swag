"""Conservative DOCX extraction with stable, inspectable source anchors."""
from __future__ import annotations

import hashlib
import io
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
REQUIRED_PART = "word/document.xml"
UNSUPPORTED = {"drawing", "pict", "object", "altChunk", "sdt", "fldChar", "instrText", "del", "ins", "txbxContent", "footnoteReference", "endnoteReference", "commentReference"}
UNSUPPORTED_PARTS = ("word/footnotes", "word/endnotes", "word/comments", "word/embeddings/", "word/media/", "word/charts/", "word/diagrams/")
METADATA_PARTS = {"word/styles.xml", "word/stylesWithEffects.xml", "word/settings.xml", "word/webSettings.xml", "word/fontTable.xml", "word/numbering.xml"}


def _tag(element):
    return element.tag.rsplit("}", 1)[-1]


def _text(element):
    parts = []
    for node in element.iter():
        kind = _tag(node)
        if kind == "t":
            parts.append(node.text or "")
        elif kind == "tab":
            parts.append("\t")
        elif kind in ("br", "cr"):
            parts.append("\n")
    return "".join(parts).strip()


def extract(data: bytes, filename: str) -> dict:
    result = {"filename": Path(filename).name, "sha256": hashlib.sha256(data).hexdigest(), "units": [], "coverage": {"status": "complete", "issues": [], "parts": []}, "size": len(data)}
    issues = result["coverage"]["issues"]
    if len(data) > 2_000_000:
        issues.append("File exceeds the 2 MB local demonstration limit")
        result["coverage"]["status"] = "blocked"
        return result
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            names = archive.namelist()
            if REQUIRED_PART not in names or any(name.startswith("/") or ".." in Path(name).parts for name in names):
                raise ValueError("Invalid DOCX package structure")
            if sum(info.file_size for info in archive.infolist()) > 10_000_000:
                raise ValueError("Expanded DOCX exceeds safety limit")
            for name in names:
                if name.startswith(UNSUPPORTED_PARTS):
                    issues.append("Unsupported content part: " + name)
                elif name.startswith("word/") and name.endswith(".xml") and name not in METADATA_PARTS and name != REQUIRED_PART and not re.fullmatch(r"word/(?:header|footer)\d+\.xml", name) and not name.startswith("word/theme/"):
                    issues.append("Unaccounted Word part: " + name)
                elif name.startswith("customXml/") and name.endswith(".xml") and not "itemProps" in name:
                    custom = ET.fromstring(archive.read(name))
                    if any((element.text or "").strip() for element in custom.iter()):
                        issues.append("Custom XML contains text requiring manual review: " + name)
            parts = [REQUIRED_PART] + sorted(name for name in names if re.fullmatch(r"word/(?:header|footer)\d+\.xml", name))
            for part in parts:
                result["coverage"]["parts"].append(part)
                root = ET.fromstring(archive.read(part))
                container = root.find(W + "body") if part == REQUIRED_PART else root
                if container is None:
                    issues.append("Missing document body")
                    continue
                _walk(container, part, result["units"], issues)
    except (zipfile.BadZipFile, ET.ParseError, KeyError, ValueError, OSError) as exc:
        issues.append("Unreadable DOCX: " + str(exc))
    if issues or not result["units"]:
        result["coverage"]["status"] = "blocked"
        if not result["units"] and not issues:
            issues.append("No extractable text")
    return result


def _walk(container, part, units, issues):
    paragraph_index = 0
    table_index = 0
    for child in container:
        kind = _tag(child)
        if kind == "p":
            paragraph_index += 1
            _paragraph(child, f"{part}:p{paragraph_index}", part, units, issues)
        elif kind == "tbl":
            table_index += 1
            for element in child:
                if _tag(element) not in ("tblPr", "tblGrid", "tr"):
                    issues.append("Unsupported table element " + _tag(element) + " in " + part)
            for row_index, row in enumerate(child.findall(W + "tr"), 1):
                for element in row:
                    if _tag(element) not in ("trPr", "tc"):
                        issues.append("Unsupported table-row element " + _tag(element) + " in " + part)
                for cell_index, cell in enumerate(row.findall(W + "tc"), 1):
                    cell_p_index = 0
                    for element in cell:
                        cell_kind = _tag(element)
                        if cell_kind == "p":
                            cell_p_index += 1
                            _paragraph(element, f"{part}:t{table_index}:r{row_index}:c{cell_index}:p{cell_p_index}", part, units, issues)
                        elif cell_kind == "tbl":
                            issues.append("Nested table requires manual review at " + part)
                        elif cell_kind != "tcPr":
                            issues.append("Unsupported table-cell element " + cell_kind + " in " + part)
        elif kind not in ("sectPr",):
            issues.append("Unsupported document element " + kind + " in " + part)


def _paragraph(paragraph, anchor, part, units, issues):
    for node in paragraph.iter():
        if _tag(node) in UNSUPPORTED:
            issues.append("Unsupported " + _tag(node) + " at " + anchor)
    value = _text(paragraph)
    if value:
        units.append({"anchor": anchor, "part": part, "kind": "paragraph" if ":t" not in anchor else "table", "text": value})


def extract_file(path: Path) -> dict:
    return extract(path.read_bytes(), path.name)
