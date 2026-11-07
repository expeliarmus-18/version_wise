
"""Deterministic group-aware dataset splitting."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Sequence

from app.ml.dataset import UpgradeRecord


@dataclass(frozen=True, slots=True)
class DatasetSplit:
    train: tuple[UpgradeRecord, ...]
    validation: tuple[UpgradeRecord, ...]
    test: tuple[UpgradeRecord, ...]

    @property
    def group_counts(self) -> dict[str, int]:
        return {
            "train": len({record.split_group for record in self.train}),
            "validation": len({record.split_group for record in self.validation}),
            "test": len({record.split_group for record in self.test}),
        }


def split_by_group(
    records: Sequence[UpgradeRecord],
    *,
    train_ratio: float = 0.8,
    validation_ratio: float = 0.1,
    test_ratio: float = 0.1,
    random_seed: int = 42,
) -> DatasetSplit:
    """Split records while keeping each split_group in exactly one partition."""

    ratios = (train_ratio, validation_ratio, test_ratio)

    if any(ratio <= 0 for ratio in ratios):
        raise ValueError("All split ratios must be greater than zero.")

    if not abs(sum(ratios) - 1.0) < 1e-9:
        raise ValueError("Split ratios must sum to 1.0.")

    if not records:
        raise ValueError("Cannot split an empty dataset.")

    grouped: dict[str, list[UpgradeRecord]] = {}

    for record in records:
        group = record.split_group.strip()
        if not group:
            raise ValueError("Every record must have a non-empty split_group.")
        grouped.setdefault(group, []).append(record)

    if len(grouped) < 3:
        raise ValueError(
            "At least 3 distinct split groups are required "
            "to create train, validation, and test partitions."
        )

    rng = random.Random(random_seed)

    # Shuffle first so equal-sized groups have seeded tie-breaking.
    groups = list(grouped.items())
    rng.shuffle(groups)
    groups.sort(key=lambda item: len(item[1]), reverse=True)

    total_records = len(records)
    targets = [
        total_records * train_ratio,
        total_records * validation_ratio,
        total_records * test_ratio,
    ]

    partitions: list[list[UpgradeRecord]] = [[], [], []]
    assigned_counts = [0, 0, 0]

    for _, group_records in groups:
        # Select the partition with the largest relative remaining capacity.
        deficits = [
            (targets[index] - assigned_counts[index]) / targets[index]
            for index in range(3)
        ]

        selected = max(range(3), key=lambda index: deficits[index])
        partitions[selected].extend(group_records)
        assigned_counts[selected] += len(group_records)

    return DatasetSplit(
        train=tuple(partitions[0]),
        validation=tuple(partitions[1]),
        test=tuple(partitions[2]),
    )
