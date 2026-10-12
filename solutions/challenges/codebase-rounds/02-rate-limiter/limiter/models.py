from dataclasses import dataclass


@dataclass(frozen=True)
class Stamp:
    key: str
    at: float
