# Dataset and extraction audit — 11 October 2026

The 12 source DOCX files were opened as ZIP/WordprocessingML packages before implementation: one reference, five historical, six incoming. All have one body part, one header and one footer. The body uses ordered paragraphs; no source file currently contains tables, drawings, text boxes, footnotes, endnotes or embedded objects. The header states the material is fictional; the footer repeats the synthetic-use limitation. All five historical IDs match exactly five decision-register rows.

The paragraph order matters: the T03 rights expansion is a second paragraph under clause 11 while clause 9 retains no-licence wording; T04 omits the clause 9 heading and text; T05 adds Schedule 1 after clause 14 and says it prevails over the main agreement. T06 changes clause 3 without changing its heading. T02 changes clause 10. T01 changes parties only. This audit describes source structure, not a runtime answer key.

Stable anchors use part and paragraph position, e.g. `word/document.xml:p25`; table anchors use table/row/cell/paragraph positions. Original bytes are served unchanged and identified by SHA-256. Extraction reads all body paragraphs, table cell paragraphs and discovered header/footer parts, then marks unsupported elements or content parts as blocked. The current source set is fully extractable. The parser is deliberately conservative for unfamiliar Word features; it is not a general-purpose DOCX or legal-document parser.

The held-out CSV was opened only by the isolated evaluator after independent analysis. Runtime code never imports or traverses its directory.
