"""Threat-intelligence indicator model and matching helpers."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Indicator:
    value: str
    indicator_type: str
    confidence: str = "Medium"
    source: str = "internal"

def match(value: str, indicators: list[Indicator]) -> list[Indicator]:
    return [i for i in indicators if i.value.strip().lower() == value.strip().lower()]
