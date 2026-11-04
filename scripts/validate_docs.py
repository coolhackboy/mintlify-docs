"""Offline checks for the Vidgo Mintlify docs. Run from the repo root: python scripts/validate_docs.py

Checks:
1. docs.json is valid JSON.
2. Every navigation page exists as .mdx and appears only once per language.
3. Every api.openapi file exists and is valid JSON.
4. Every frontmatter `openapi` reference resolves to a registered spec, path and method.
5. Every internal link (/...) in .mdx files points to an existing page or a redirect source.
6. zh navigation only lists zh/ pages; en navigation never lists zh/ pages.
`mint broken-links` reports false positives on Windows, so use this script there; `mint validate` still works.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
errors = []

docs = json.load(open("docs.json", encoding="utf-8"))


def pages(node):
    if isinstance(node, str):
        yield node
        return
    if isinstance(node, list):
        for c in node:
            yield from pages(c)
        return
    for k in ("languages", "tabs", "groups", "pages", "anchors", "dropdowns"):
        for c in node.get(k, []):
            yield from pages(c)


for lang in docs["navigation"]["languages"]:
    ps = list(pages(lang))
    code = lang["language"]
    for p in ps:
        if not os.path.exists(p + ".mdx"):
            errors.append(f"[nav:{code}] missing page {p}")
        if code == "zh" and not p.startswith("zh/"):
            errors.append(f"[nav:zh] non-zh page {p}")
        if code != "zh" and p.startswith("zh/"):
            errors.append(f"[nav:{code}] zh page {p}")
    dup = {p for p in ps if ps.count(p) > 1}
    for p in sorted(dup):
        errors.append(f"[nav:{code}] duplicate page {p}")

specs = {}
for path in docs["api"]["openapi"]:
    f = path.lstrip("/")
    if not os.path.exists(f):
        errors.append(f"[openapi] missing {path}")
        continue
    try:
        specs[path] = json.load(open(f, encoding="utf-8-sig"))
    except Exception as e:  # noqa: BLE001
        errors.append(f"[openapi] invalid JSON {path}: {e}")

redirects = {r["source"] for r in docs.get("redirects", [])}
all_pages = {os.path.relpath(f, ROOT).replace("\\", "/")[:-4] for f in glob.glob("**/*.mdx", recursive=True)}
LINK = re.compile(r"\]\((/[^)\s#]*)(#[^)\s]*)?\)|href=\"(/[^\"#]*)(#[^\"]*)?\"")
for f in sorted(glob.glob("**/*.mdx", recursive=True)):
    rel = f.replace("\\", "/")
    text = open(f, encoding="utf-8-sig").read()
    m = re.match(r"---\n(.*?)\n---", text.replace("\r\n", "\n"), re.S)
    fm = m.group(1) if m else ""
    om = re.search(r'^openapi:\s*"([^"]+)"', fm, re.M)
    if om:
        parts = om.group(1).split()
        if len(parts) == 3:
            spec, method, path = parts
            cands = [specs.get(spec)] if spec in specs else []
            if spec not in specs:
                errors.append(f"[frontmatter] {rel}: spec not registered {spec}")
        else:
            method, path = parts
            cands = list(specs.values())
        if cands and not any(method.lower() in (s.get("paths", {}).get(path) or {}) for s in cands if s):
            errors.append(f"[frontmatter] {rel}: {method} {path} not found")
    body = re.sub(r"```.*?```", "", text, flags=re.S)
    for lm in LINK.finditer(body):
        target = (lm.group(1) or lm.group(3)).rstrip("/")
        if not target or target.startswith("//"):
            continue
        t = target.lstrip("/") or "index"
        if os.path.splitext(t)[1] in (".json", ".png", ".svg", ".jpg", ".ico"):
            continue
        if t in all_pages or t + "/index" in all_pages or target in redirects:
            continue
        errors.append(f"[link] {rel}: {target}")

for e in errors:
    print(e)
print(f"{len(errors)} problem(s)")
sys.exit(1 if errors else 0)
