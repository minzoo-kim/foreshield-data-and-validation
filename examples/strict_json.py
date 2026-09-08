"""A standalone reconstruction of a strict JSON input boundary."""

from __future__ import annotations

import json
import math
from typing import Any


def _reject_constant(value: str) -> None:
    raise ValueError(f"Non-standard JSON constant: {value}")


def _finite_float(value: str) -> float:
    parsed = float(value)
    if not math.isfinite(parsed):
        raise ValueError(f"Non-finite JSON number: {value}")
    return parsed


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for key, _ in pairs:
        if key in seen:
            duplicates.add(key)
        seen.add(key)
    if duplicates:
        raise ValueError(f"Duplicate object keys: {sorted(duplicates)}")
    return dict(pairs)


def parse_strict_json(content: bytes) -> Any:
    """Parse UTF-8 JSON while rejecting duplicate keys and non-finite numbers."""
    text = content.decode("utf-8")
    return json.loads(
        text,
        parse_constant=_reject_constant,
        parse_float=_finite_float,
        object_pairs_hook=_unique_object,
    )


if __name__ == "__main__":
    for sample in (b'{"score": 0.25}', b'{"score": 0.25, "score": 0.75}'):
        try:
            print("accepted:", parse_strict_json(sample))
        except ValueError as error:
            print("rejected:", error)
