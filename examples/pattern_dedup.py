"""Order-preserving deduplication example, not the private service's FAQ engine."""

from __future__ import annotations

from collections.abc import Iterable


def unique_variants(original: str, candidates: Iterable[str]) -> list[str]:
    """Exclude the original and duplicates while preserving first occurrence."""
    ordered: list[str] = []
    seen: set[str] = {original}
    for candidate in candidates:
        if candidate not in seen:
            seen.add(candidate)
            ordered.append(candidate)
    return ordered


if __name__ == "__main__":
    variants = unique_variants(
        "show help",
        ["show help", "explain this service", "help please", "help please"],
    )
    print(variants)
