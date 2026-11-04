"""Conservative Maven-style version comparison for common release forms.

This is a deliberately bounded implementation, not Apache Maven's full
ComparableVersion implementation. Exotic or ambiguous forms return UNKNOWN.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum


class Comparison(str, Enum):
    UPGRADE = "upgrade"
    DOWNGRADE = "downgrade"
    EQUAL = "equal"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class VersionComparison:
    current_version: str
    target_version: str
    result: Comparison
    explanation: str
    current_parts: tuple[int, ...] | None = None
    target_parts: tuple[int, ...] | None = None


_QUALIFIER_ORDER = {
    "alpha": 0, "a": 0,
    "beta": 1, "b": 1,
    "milestone": 2, "m": 2,
    "rc": 3, "cr": 3,
    "snapshot": 4,
    "": 5, "final": 5, "ga": 5, "release": 5,
    "sp": 6,
}
_TOKEN = re.compile(r"\d+|[A-Za-z]+")
_VALID_CHARS = re.compile(r"^[0-9A-Za-z._+-]+$")


def _parse(version: str):
    if not isinstance(version, str) or not version.strip():
        return None
    value = version.strip().lower()
    if not _VALID_CHARS.fullmatch(value):
        return None
    # Maven's common separator forms are handled; repeated/leading separators
    # and unknown qualifiers are conservatively treated as ambiguous.
    raw = _TOKEN.findall(value)
    if not raw or "".join(raw) != re.sub(r"[._+-]", "", value):
        return None

    tokens = []
    for token in raw:
        if token.isdigit():
            tokens.append((0, int(token)))
        else:
            normalized = token
            if normalized not in _QUALIFIER_ORDER:
                return None
            tokens.append((1, _QUALIFIER_ORDER[normalized], normalized))

    # Remove trailing numeric zero tokens. A trailing release qualifier is
    # equivalent to no qualifier for the supported common release forms.
    while tokens and tokens[-1] == (0, 0):
        tokens.pop()
    while tokens and tokens[-1][0] == 1 and tokens[-1][1] == 5:
        tokens.pop()

    # Numeric core is used only for magnitude classification by the rule engine.
    numeric = []
    for kind, *rest in tokens:
        if kind != 0:
            break
        numeric.append(rest[0])
    return tuple(tokens), tuple(numeric)


def compare_versions(current_version: str, target_version: str) -> VersionComparison:
    current = _parse(current_version)
    target = _parse(target_version)
    if current is None or target is None:
        return VersionComparison(
            current_version, target_version, Comparison.UNKNOWN,
            "At least one version uses an unsupported or ambiguous format."
        )

    left, right = current[0], target[0]
    # Compare token positions using Maven-like numeric/qualifier precedence.
    max_len = max(len(left), len(right))
    for i in range(max_len):
        a = left[i] if i < len(left) else (0, 0)
        b = right[i] if i < len(right) else (0, 0)
        if a == b:
            continue
        # A numeric item is later than a qualifier at the same position.
        if a[0] != b[0]:
            ordering = 1 if a[0] == 0 else -1
        elif a[0] == 0:
            ordering = (a[1] > b[1]) - (a[1] < b[1])
        else:
            ordering = (a[1] > b[1]) - (a[1] < b[1])
            if ordering == 0:
                ordering = (a[2] > b[2]) - (a[2] < b[2])
        if ordering > 0:
            result = Comparison.DOWNGRADE
        elif ordering < 0:
            result = Comparison.UPGRADE
        else:
            result = Comparison.EQUAL
        return VersionComparison(
            current_version, target_version, result,
            f"Supported Maven-style token comparison indicates {result.value}.",
            current[1], target[1],
        )

    return VersionComparison(
        current_version, target_version, Comparison.EQUAL,
        "Versions are equivalent under the supported Maven-style comparison.",
        current[1], target[1],
    )
