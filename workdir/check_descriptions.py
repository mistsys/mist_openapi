#!/usr/bin/env python3
"""Report schema properties whose OpenAPI descriptions need cleanup."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


SPEC_PATH = Path("openapi.yaml")
JSON_PATH = Path("description_issues.json")
REPORT_PATH = Path("description_issues_report.txt")
SHORT_DESCRIPTION_WORD_LIMIT = 3


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9_`=/.-]+", text)


def property_type(schema: dict[str, Any]) -> str:
    value = schema.get("type")
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "|".join(str(item) for item in value)
    return "unknown"


def normalized_start(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def starts_with_property_name(prop_name: str, description: str) -> bool:
    prop = prop_name.lower()
    desc = description.strip().lower()
    if not prop or not desc:
        return False

    return desc.startswith(prop)


def analyze(data: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    issues: dict[str, list[dict[str, Any]]] = {
        "missing_description": [],
        "very_short_description": [],
        "description_starts_with_property": [],
    }

    schemas = data.get("components", {}).get("schemas", {})
    for schema_name, schema in schemas.items():
        if not isinstance(schema, dict):
            continue

        properties = schema.get("properties")
        if not isinstance(properties, dict):
            continue

        for prop_name, prop_schema in properties.items():
            if not isinstance(prop_schema, dict):
                continue

            item = {
                "path": f"{schema_name}.{prop_name}",
                "schema": schema_name,
                "type": property_type(prop_schema),
            }
            description = prop_schema.get("description")
            if not description:
                issues["missing_description"].append(item)
                continue

            description = str(description).strip()
            described_item = {**item, "description": description}

            if len(words(description)) <= SHORT_DESCRIPTION_WORD_LIMIT:
                issues["very_short_description"].append(described_item)

            if starts_with_property_name(prop_name, description):
                issues["description_starts_with_property"].append(described_item)

    return issues


def render_report(issues: dict[str, list[dict[str, Any]]]) -> str:
    total = sum(len(values) for values in issues.values())
    lines = [
        "Loading OpenAPI specification...",
        "Analyzing descriptions...",
        "=" * 80,
        "OpenAPI ATTRIBUTE DESCRIPTION ANALYSIS REPORT",
        "=" * 80,
        "",
        f"TOTAL ISSUES FOUND: {total}",
        "",
    ]

    sections = [
        ("MISSING DESCRIPTIONS", "missing_description"),
        ("VERY SHORT DESCRIPTIONS", "very_short_description"),
        ("DESCRIPTION STARTS WITH PROPERTY NAME", "description_starts_with_property"),
    ]

    for title, key in sections:
        values = issues[key]
        lines.extend(
            [
                "-" * 80,
                f"{title} ({len(values)} found)",
                "-" * 80,
            ]
        )

        for item in values[:50]:
            if key == "missing_description":
                lines.append(f"  \u2022 {item['path']} (type: {item['type']})")
            else:
                lines.append(f"  \u2022 {item['path']}")
                lines.append(f"    Description: {json.dumps(item['description'])}")

        if len(values) > 50:
            lines.append(f"  ... and {len(values) - 50} more")

        lines.append("")

    lines.append(f"Report saved to: {REPORT_PATH.resolve()}")
    lines.append(f"Issues exported to: {JSON_PATH.resolve()}")
    return "\n".join(lines)


def main() -> None:
    data = yaml.safe_load(SPEC_PATH.read_text())
    issues = analyze(data)
    report = render_report(issues)

    JSON_PATH.write_text(json.dumps(issues, indent=2) + "\n")
    REPORT_PATH.write_text(report + "\n")
    print(report)


if __name__ == "__main__":
    main()
