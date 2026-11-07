
"""Prepare a labeled dependency-upgrade dataset for ML experiments."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, fields
from pathlib import Path

from app.ml.dataset import UpgradeRecord, load_csv, validate_records
from app.ml.split import split_by_group


def write_records(path: Path, records: tuple[UpgradeRecord, ...]) -> None:
    """Write prepared records to a CSV file."""

    fieldnames = [field.name for field in fields(UpgradeRecord)]

    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for record in records:
            writer.writerow(asdict(record))


def prepare_dataset(
    input_path: Path,
    output_dir: Path,
    *,
    random_seed: int = 42,
) -> dict:
    """Validate, deduplicate, split, and summarize a CSV dataset."""

    source_rows = load_csv(input_path)
    records, validation_summary = validate_records(source_rows)

    if not records:
        raise ValueError("No valid records remain after dataset validation.")

    split = split_by_group(records, random_seed=random_seed)

    output_dir.mkdir(parents=True, exist_ok=True)

    write_records(output_dir / "train.csv", split.train)
    write_records(output_dir / "validation.csv", split.validation)
    write_records(output_dir / "test.csv", split.test)

    summary = {
        "input_file": str(input_path),
        "output_directory": str(output_dir),
        "random_seed": random_seed,
        "validation": asdict(validation_summary),
        "split": {
            "train_records": len(split.train),
            "validation_records": len(split.validation),
            "test_records": len(split.test),
            "train_groups": split.group_counts["train"],
            "validation_groups": split.group_counts["validation"],
            "test_groups": split.group_counts["test"],
        },
        "training_status": "NOT_STARTED",
        "reason": (
            "Dataset preparation completed. Model training requires "
            "a verified, sufficiently large, representative labeled dataset."
        ),
    }

    with (output_dir / "summary.json").open(
        "w", encoding="utf-8"
    ) as file:
        json.dump(summary, file, indent=2)

    return summary


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Prepare a labeled dependency-upgrade CSV for ML."
    )
    parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="Path to the source CSV dataset.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/processed"),
        help="Directory for prepared CSV files and summary.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for deterministic splitting.",
    )

    args = parser.parse_args()

    summary = prepare_dataset(
        args.input,
        args.output,
        random_seed=args.seed,
    )

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
