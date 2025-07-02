"""Utility functions for working with text values."""
import re


def remove_sequence_of(symbol: str, string: str) -> str:
    """Return *string* with consecutive *symbol* collapsed into one."""
    parts = [s for s in string.split(symbol) if s]
    return symbol.join(parts)


def slugify(name: str) -> str:
    """Return a slug suitable for Fibery branch names."""
    cleaned = re.sub(r"[^\w\d-]|[()\[\]{}]", "-", name.strip().lower())
    return remove_sequence_of("-", cleaned)
