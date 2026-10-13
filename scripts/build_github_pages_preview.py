"""Build an isolated read-only GitHub Pages fallback under /Swag/.

No evaluation files, private data, backend or user state are copied.
"""
from __future__ import annotations
import json
import shutil
from pathlib import Path

root = Path(__file__).resolve().parents[1]
source = root / "web"
destination = root / "tmp-github-pages"
if destination.exists():
    shutil.rmtree(destination)
shutil.copytree(source, destination)
index = destination / "index.html"
index.write_text(index.read_text().replace('href="/styles.css"', 'href="/Swag/styles.css"')
                 .replace('src="/app.js"', 'src="/Swag/app.js"'))
app = destination / "app.js"
code = app.read_text()
# Preserve both the path strings and the regular-expression comparisons.
code = code.replace("/demo-data/", "/Swag/demo-data/")
code = code.replace("/api/", "/Swag/api/")
code = code.replace(r"\/api\/", r"\/Swag\/api\/")
app.write_text(code)
(destination / ".nojekyll").touch()
queue = json.loads((destination / "demo-data/queue.json").read_text())
research = json.loads((destination / "demo-data/research.json").read_text())
assert len(queue["items"]) == 6
assert len(research["references"]) == 8
assert len(research["routine_clients"]) == 20
assert len(research["challenge_cases"]) == 4
assert "/Swag/demo-data/queue.json" in code
assert "/Swag/api/queue" in code
assert "/Swag/styles.css" in index.read_text()
assert not any("ground_truth" in x.name for x in destination.rglob("*"))
print("Prepared six reviewed NDA cases and 32 unassessed research specimens for /Swag/")
