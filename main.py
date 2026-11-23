#!/usr/bin/env python3
"""Read-only validator for local XML sitemap and sitemap-index files."""
from __future__ import annotations
import argparse
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

LIMIT = 50_000

def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()

def valid_http_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)

def valid_lastmod(value: str) -> bool:
    from datetime import date, datetime
    try:
        if "T" in value:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
        else:
            date.fromisoformat(value)
        return True
    except ValueError:
        return False

def audit_tree(root: ET.Element) -> dict:
    kind = local_name(root.tag)
    findings: list[dict] = []
    if kind not in {"urlset", "sitemapindex"}:
        findings.append({"level": "error", "message": f"Expected urlset or sitemapindex root, found '{kind}'."})
        return {"kind": kind, "entries": 0, "findings": findings}
    entry_name = "url" if kind == "urlset" else "sitemap"
    entries = [child for child in root if local_name(child.tag) == entry_name]
    seen: set[str] = set()
    for index, entry in enumerate(entries, 1):
        values = {local_name(child.tag): (child.text or "").strip() for child in entry}
        loc = values.get("loc", "")
        if not loc:
            findings.append({"level": "error", "entry": index, "message": "Missing loc element."})
        elif not valid_http_url(loc):
            findings.append({"level": "error", "entry": index, "message": f"loc must be an absolute HTTP(S) URL: {loc}"})
        elif loc in seen:
            findings.append({"level": "warning", "entry": index, "message": f"Duplicate loc: {loc}"})
        seen.add(loc)
        lastmod = values.get("lastmod")
        if lastmod and not valid_lastmod(lastmod):
            findings.append({"level": "warning", "entry": index, "message": f"Invalid lastmod value: {lastmod}"})
    if len(entries) > LIMIT:
        findings.append({"level": "error", "message": f"{len(entries)} entries exceeds the {LIMIT:,}-entry sitemap limit."})
    return {"kind": kind, "entries": len(entries), "findings": findings}

def audit_file(path: Path) -> dict:
    try:
        root = ET.parse(path).getroot()
    except (OSError, ET.ParseError) as exc:
        return {"file": str(path), "kind": None, "entries": 0,
                "findings": [{"level": "error", "message": f"Cannot parse XML: {exc}"}]}
    report = audit_tree(root)
    report["file"] = str(path)
    report["errors"] = sum(x["level"] == "error" for x in report["findings"])
    report["warnings"] = sum(x["level"] == "warning" for x in report["findings"])
    return report

def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a local sitemap.xml without fetching URLs.")
    parser.add_argument("path", nargs="?", default="sample-sitemap.xml")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = audit_file(Path(args.path))
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Sitemap audit: {report['file']}")
        print(f"Type: {report['kind'] or 'invalid'} | entries: {report['entries']} | errors: {report.get('errors', 0)} | warnings: {report.get('warnings', 0)}")
        for item in report["findings"]:
            where = f"entry {item['entry']}: " if "entry" in item else ""
            print(f"[{item['level'].upper()}] {where}{item['message']}")
        if not report["findings"]:
            print("No issues found.")
    return 1 if report.get("errors", 0) else 0

if __name__ == "__main__":
    raise SystemExit(main())
