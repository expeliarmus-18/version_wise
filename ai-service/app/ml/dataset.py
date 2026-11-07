
"""Validation and normalization for historical upgrade observations."""

from __future__ import annotations

import csv
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


SUPPORTED_LABELS = frozenset(
    {
        "COMPILATION_FAILURE",
        "TEST_FAILURE",
        "DEPENDENCY_RESOLUTION_FAILURE",
        "OTHER_BUILD_FAILURE",
        "SUCCESSFUL_BUILD",
        "UNKNOWN",
    }
)


@dataclass(frozen=True, slots=True)
class UpgradeRecord:
    """Canonical representation of one observed dependency upgrade."""

    record_id: str
    ecosystem: str
    group_id: str
    artifact_id: str
    current_version: str
    target_version: str
    upgrade_type: str
    project_id: str
    observation_timestamp: str
    label: str
    source_label: str
    label_evidence: str
    label_confidence: float | None
    data_source: str
    source_license: str
    split_group: str


@dataclass(frozen=True, slots=True)
class DatasetSummary:
    """Counts produced during dataset validation."""

    input_records: int
    valid_records: int
    invalid_records: int
    duplicate_records: int
    label_counts: dict[str, int]


class DatasetValidationError(ValueError):
    """Raised when a source record cannot be normalized."""


def normalize_label(source_label: str) -> str:
    """Normalize known labels without guessing unknown categories."""

    normalized = source_label.strip().upper()

    if normalized not in SUPPORTED_LABELS:
        raise DatasetValidationError(
            f"Unsupported label: {source_label!r}"
        )

    return normalized


def parse_confidence(value: str) -> float | None:
    """Parse optional label confidence in the inclusive range [0, 1]."""

    if not value.strip():
        return None

    try:
        confidence = float(value)
    except ValueError as exc:
        raise DatasetValidationError(
            "label_confidence must be numeric"
        ) from exc

    if not 0.0 <= confidence <= 1.0:
        raise DatasetValidationError(
            "label_confidence must be between 0 and 1"
        )

    return confidence


def normalize_record(
    source: dict[str, str],
) -> UpgradeRecord:
    """Validate and normalize one source record."""

    required_fields = (
        "record_id",
        "ecosystem",
        "group_id",
        "artifact_id",
        "current_version",
        "target_version",
        "upgrade_type",
        "project_id",
        "observation_timestamp",
        "label",
        "label_evidence",
        "data_source",
        "source_license",
        "split_group",
    )

    missing = [
        field
        for field in required_fields
        if not source.get(field, "").strip()
    ]

    if missing:
        raise DatasetValidationError(
            f"Missing required fields: {', '.join(missing)}"
        )

    source_label = source["label"].strip()

    return UpgradeRecord(
        record_id=source["record_id"].strip(),
        ecosystem=source["ecosystem"].strip().lower(),
        group_id=source["group_id"].strip(),
        artifact_id=source["artifact_id"].strip(),
        current_version=source["current_version"].strip(),
        target_version=source["target_version"].strip(),
        upgrade_type=source["upgrade_type"].strip().upper(),
        project_id=source["project_id"].strip(),
        observation_timestamp=source[
            "observation_timestamp"
        ].strip(),
        label=normalize_label(source_label),
        source_label=source_label,
        label_evidence=source["label_evidence"].strip(),
        label_confidence=parse_confidence(
            source.get("label_confidence", "")
        ),
        data_source=source["data_source"].strip(),
        source_license=source["source_license"].strip(),
        split_group=source["split_group"].strip(),
    )


def duplicate_key(record: UpgradeRecord) -> tuple[str, ...]:
    """Identify repeated observations of the same project upgrade."""

    return (
        record.ecosystem,
        record.group_id,
        record.artifact_id,
        record.current_version,
        record.target_version,
        record.project_id,
    )


def validate_records(
    source_records: Iterable[dict[str, str]],
) -> tuple[list[UpgradeRecord], DatasetSummary]:
    """Normalize records and remove repeated upgrade observations."""

    valid_records: list[UpgradeRecord] = []
    seen_keys: set[tuple[str, ...]] = set()

    input_count = 0
    invalid_count = 0
    duplicate_count = 0

    for source in source_records:
        input_count += 1

        try:
            record = normalize_record(source)
        except DatasetValidationError:
            invalid_count += 1
            continue

        key = duplicate_key(record)

        if key in seen_keys:
            duplicate_count += 1
            continue

        seen_keys.add(key)
        valid_records.append(record)

    label_counts = Counter(
        record.label for record in valid_records
    )

    summary = DatasetSummary(
        input_records=input_count,
        valid_records=len(valid_records),
        invalid_records=invalid_count,
        duplicate_records=duplicate_count,
        label_counts=dict(sorted(label_counts.items())),
    )

    return valid_records, summary


def load_csv(path: Path) -> list[dict[str, str]]:
    """Load source observations from a UTF-8 CSV file."""

    with path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        return list(csv.DictReader(file))
