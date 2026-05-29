#!/usr/bin/env python3
"""Audit OpenAPI descriptions for terminology and consistency issues.

This script is read-only with respect to the OpenAPI spec. It writes Markdown and
JSON reports so findings can be reviewed before any description edits are made.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import yaml


DEFAULT_SPEC_PATH = Path("openapi.yaml")
DEFAULT_REPORT_PATH = Path("description_coherence_report.md")
DEFAULT_JSON_PATH = Path("description_coherence_report.json")
SHORT_DESCRIPTION_WORD_LIMIT = 3


@dataclass(frozen=True)
class Finding:
    path: str
    message: str
    description: str | None = None
    schema: str | None = None
    property_name: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "message": self.message,
            "description": self.description,
            "schema": self.schema,
            "property": self.property_name,
        }


TERMINOLOGY_RULES: dict[str, list[tuple[str, str]]] = {
    "MAC address": [
        ("MAC Address", r"\bMAC Address\b"),
        ("Mac address", r"\bMac address\b"),
        ("mac address", r"\bmac address\b"),
        ("Hardware address", r"\bhardware address\b"),
    ],
    "IP address": [
        ("IP Address", r"\bIP Address\b"),
        ("Ip address", r"\bIp address\b"),
        ("ip address", r"\bip address\b"),
    ],
    "VLAN ID": [
        ("VLAN Id", r"\bVLAN Id\b"),
        ("VLAN id", r"\bVLAN id\b"),
        ("Vlan ID", r"\bVlan ID\b"),
        ("vlan id", r"\bvlan id\b"),
    ],
    "RADIUS": [
        ("Radius", r"\bRadius\b"),
        ("radius server", r"\bradius server\b"),
        ("radius auth", r"\bradius auth\b"),
    ],
    "IPsec": [
        ("IPSec", r"\bIPSec\b"),
        ("ipsec", r"\bipsec\b"),
    ],
    "Mist Edge": [
        ("MxEdge", r"\bMxEdge\b"),
        ("mxedge", r"\bmxedge\b"),
        ("MX Edge", r"\bMX Edge\b"),
    ],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit description coherence in an OpenAPI document."
    )
    parser.add_argument("--spec", type=Path, default=DEFAULT_SPEC_PATH)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT_PATH)
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON_PATH)
    parser.add_argument(
        "--max-examples",
        type=int,
        default=25,
        help="Maximum findings to show per report section.",
    )
    return parser.parse_args()


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9_`=/.-]+", text)


def path_to_str(parts: Iterable[str]) -> str:
    text = ".".join(parts)
    return text.replace(".properties.", ".")


def normalized_description(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def excerpt(text: str, max_chars: int = 500) -> str:
    text = re.sub(r"\s+", " ", text.strip())
    if len(text) <= max_chars:
        return text
    return f"{text[: max_chars - 3]}..."


def starts_with_property_name(prop_name: str, description: str) -> bool:
    prop = prop_name.lower()
    desc = description.strip().lower()
    return bool(prop and desc and desc.startswith(prop))


def iter_descriptions(value: Any, parts: tuple[str, ...] = ()) -> Iterable[tuple[str, str, dict[str, Any]]]:
    if isinstance(value, dict):
        description = value.get("description")
        if isinstance(description, str):
            yield path_to_str(parts), description, value
        for key, child in value.items():
            yield from iter_descriptions(child, (*parts, str(key)))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from iter_descriptions(child, (*parts, str(index)))


def schema_type(schema: dict[str, Any]) -> str:
    if "$ref" in schema:
        return "ref"
    for key in ("oneOf", "anyOf", "allOf"):
        if key in schema:
            return key
    value = schema.get("type")
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "|".join(str(item) for item in value)
    return "unknown"


def analyze_schema_descriptions(schemas: dict[str, Any]) -> dict[str, list[Finding]]:
    findings: dict[str, list[Finding]] = defaultdict(list)

    for schema_name, schema in schemas.items():
        if not isinstance(schema, dict):
            continue

        schema_description = schema.get("description")
        if not isinstance(schema_description, str) or not schema_description.strip():
            findings["missing_schema_description"].append(
                Finding(
                    path=f"components.schemas.{schema_name}",
                    schema=schema_name,
                    message="Top-level schema has no description.",
                )
            )
        elif len(words(schema_description)) <= SHORT_DESCRIPTION_WORD_LIMIT:
            findings["very_short_description"].append(
                Finding(
                    path=f"components.schemas.{schema_name}",
                    schema=schema_name,
                    message=f"Description has {SHORT_DESCRIPTION_WORD_LIMIT} or fewer words.",
                    description=schema_description,
                )
            )

        properties = schema.get("properties")
        if not isinstance(properties, dict):
            continue

        required = set(schema.get("required") or [])
        for prop_name, prop_schema in properties.items():
            if not isinstance(prop_schema, dict):
                continue

            path = f"components.schemas.{schema_name}.{prop_name}"
            description = prop_schema.get("description")
            if not isinstance(description, str) or not description.strip():
                findings["missing_property_description"].append(
                    Finding(
                        path=path,
                        schema=schema_name,
                        property_name=prop_name,
                        message="Property has no description.",
                    )
                )
                continue

            description = description.strip()
            if len(words(description)) <= SHORT_DESCRIPTION_WORD_LIMIT:
                findings["very_short_description"].append(
                    Finding(
                        path=path,
                        schema=schema_name,
                        property_name=prop_name,
                        message=f"Description has {SHORT_DESCRIPTION_WORD_LIMIT} or fewer words.",
                        description=description,
                    )
                )

            if starts_with_property_name(prop_name, description):
                findings["description_starts_with_property"].append(
                    Finding(
                        path=path,
                        schema=schema_name,
                        property_name=prop_name,
                        message="Description starts with the property name.",
                        description=description,
                    )
                )

            if prop_schema.get("default") is not None and re.search(r"\brequired\b", description, re.I):
                findings["defaulted_field_mentions_required"].append(
                    Finding(
                        path=path,
                        schema=schema_name,
                        property_name=prop_name,
                        message="Defaulted field description mentions required; review for semantic accuracy.",
                        description=description,
                    )
                )

            if prop_name in required and re.search(r"\boptional\b", description, re.I):
                findings["required_field_mentions_optional"].append(
                    Finding(
                        path=path,
                        schema=schema_name,
                        property_name=prop_name,
                        message="Schema-required property description mentions optional.",
                        description=description,
                    )
                )

            if schema_type(prop_schema) == "object" and re.search(r"\b(list|array)\b", description, re.I):
                findings["shape_wording_review"].append(
                    Finding(
                        path=path,
                        schema=schema_name,
                        property_name=prop_name,
                        message="Object-shaped property description uses list/array wording.",
                        description=description,
                    )
                )

            if schema_type(prop_schema) == "array" and re.search(r"\bobject\b", description, re.I):
                findings["shape_wording_review"].append(
                    Finding(
                        path=path,
                        schema=schema_name,
                        property_name=prop_name,
                        message="Array-shaped property description uses object wording.",
                        description=description,
                    )
                )

    return findings


def analyze_terminology(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    descriptions = list(iter_descriptions(data))
    report: dict[str, dict[str, Any]] = {}

    for canonical, variants in TERMINOLOGY_RULES.items():
        variant_counts: Counter[str] = Counter()
        examples: dict[str, list[dict[str, str]]] = defaultdict(list)

        canonical_count = 0
        canonical_pattern = re.compile(re.escape(canonical))
        for path, description, _owner in descriptions:
            canonical_count += len(canonical_pattern.findall(description))
            for label, pattern in variants:
                matches = re.findall(pattern, description, flags=re.I if label == "Hardware address" else 0)
                if not matches:
                    continue
                variant_counts[label] += len(matches)
                if len(examples[label]) < 10:
                    examples[label].append({"path": path, "description": description})

        report[canonical] = {
            "canonical_count": canonical_count,
            "variant_counts": dict(variant_counts),
            "examples": examples,
        }

    return report


def analyze_duplicate_descriptions(data: dict[str, Any]) -> list[dict[str, Any]]:
    groups: dict[str, list[str]] = defaultdict(list)
    original_text: dict[str, str] = {}

    for path, description, _owner in iter_descriptions(data):
        normalized = normalized_description(description)
        if len(words(normalized)) <= SHORT_DESCRIPTION_WORD_LIMIT:
            continue
        groups[normalized].append(path)
        original_text.setdefault(normalized, description.strip())

    duplicates = []
    for normalized, paths in groups.items():
        if len(paths) < 4:
            continue
        duplicates.append(
            {
                "description": original_text[normalized],
                "count": len(paths),
                "paths": paths,
            }
        )

    return sorted(duplicates, key=lambda item: (-item["count"], item["description"]))


def render_findings(title: str, findings: list[Finding], max_examples: int) -> list[str]:
    lines = [f"## {title}", "", f"Count: {len(findings)}", ""]
    for finding in findings[:max_examples]:
        lines.append(f"- `{finding.path}`: {finding.message}")
        if finding.description:
            lines.append(f"  - Description: {json.dumps(excerpt(finding.description))}")
    if len(findings) > max_examples:
        lines.append(f"- ... {len(findings) - max_examples} more")
    lines.append("")
    return lines


def render_report(
    spec_path: Path,
    findings: dict[str, list[Finding]],
    terminology: dict[str, dict[str, Any]],
    duplicate_descriptions: list[dict[str, Any]],
    max_examples: int,
) -> str:
    issue_order = [
        ("Missing Schema Descriptions", "missing_schema_description"),
        ("Missing Property Descriptions", "missing_property_description"),
        ("Very Short Descriptions", "very_short_description"),
        ("Descriptions Starting With Property Name", "description_starts_with_property"),
        ("Defaulted Fields Mentioning Required", "defaulted_field_mentions_required"),
        ("Required Fields Mentioning Optional", "required_field_mentions_optional"),
        ("Shape Wording Review", "shape_wording_review"),
    ]
    total = sum(len(findings.get(key, [])) for _title, key in issue_order)

    lines = [
        "# OpenAPI Description Coherence Report",
        "",
        f"Spec: `{spec_path}`",
        "",
        "This report is heuristic. Review findings before changing the spec, especially conditional wording such as `Required if ...`.",
        "",
        "## Summary",
        "",
        f"- Total heuristic findings: {total}",
    ]
    for title, key in issue_order:
        lines.append(f"- {title}: {len(findings.get(key, []))}")
    lines.append(f"- Repeated description groups: {len(duplicate_descriptions)}")
    lines.append("")

    lines.extend(["## Terminology Variants", ""])
    for canonical, info in terminology.items():
        variant_counts = info["variant_counts"]
        variant_total = sum(variant_counts.values())
        lines.append(f"### Preferred: `{canonical}`")
        lines.append("")
        lines.append(f"- Preferred occurrences: {info['canonical_count']}")
        lines.append(f"- Variant occurrences: {variant_total}")
        for variant, count in sorted(variant_counts.items()):
            lines.append(f"- `{variant}`: {count}")
            for example in info["examples"].get(variant, [])[:3]:
                lines.append(f"  - `{example['path']}`: {json.dumps(excerpt(example['description']))}")
        lines.append("")

    for title, key in issue_order:
        lines.extend(render_findings(title, findings.get(key, []), max_examples))

    lines.extend(["## Repeated Descriptions", ""])
    lines.append("Identical descriptions are not automatically bad, but large groups often expose generic wording or reusable concepts.")
    lines.append("")
    for group in duplicate_descriptions[:max_examples]:
        lines.append(f"- {group['count']} uses: {json.dumps(excerpt(group['description']))}")
        for path in group["paths"][:8]:
            lines.append(f"  - `{path}`")
        if len(group["paths"]) > 8:
            lines.append(f"  - ... {len(group['paths']) - 8} more")
    if len(duplicate_descriptions) > max_examples:
        lines.append(f"- ... {len(duplicate_descriptions) - max_examples} more groups")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    data = yaml.safe_load(args.spec.read_text())
    schemas = data.get("components", {}).get("schemas", {})
    if not isinstance(schemas, dict):
        raise SystemExit("No components.schemas object found")

    findings = analyze_schema_descriptions(schemas)
    terminology = analyze_terminology(data)
    duplicate_descriptions = analyze_duplicate_descriptions(data)

    json_data = {
        "summary": {
            "spec": str(args.spec),
            "finding_counts": {key: len(value) for key, value in findings.items()},
            "repeated_description_groups": len(duplicate_descriptions),
        },
        "findings": {key: [item.to_dict() for item in value] for key, value in findings.items()},
        "terminology": terminology,
        "repeated_descriptions": duplicate_descriptions,
    }
    report = render_report(args.spec, findings, terminology, duplicate_descriptions, args.max_examples)

    args.json.write_text(json.dumps(json_data, indent=2) + "\n")
    args.report.write_text(report + "\n")
    print(report)
    print(f"Markdown report written to: {args.report.resolve()}")
    print(f"JSON report written to: {args.json.resolve()}")


if __name__ == "__main__":
    main()
