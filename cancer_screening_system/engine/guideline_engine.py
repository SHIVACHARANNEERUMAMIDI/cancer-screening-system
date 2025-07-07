from abc import ABC, abstractmethod
from typing import Callable, Dict
from enum import Enum

# === Enum for fast matching === #
class CancerType(str, Enum):
    BREAST = "breast"
    CERVICAL = "cervical"
    COLORECTAL = "colorectal"

# === Stateless Strategy Functions === #
def breast_guideline(risk: int) -> int:
    return 1 if risk > 4 else 2

def cervical_guideline(risk: int) -> int:
    return 2 if risk > 3 else 3

def colorectal_guideline(risk: int) -> int:
    return 3 if risk > 5 else 5

def default_guideline(risk: int) -> int:
    return 5

# === Fast Lookup Map === #
GUIDELINE_RULES: Dict[CancerType, Callable[[int], int]] = {
    CancerType.BREAST: breast_guideline,
    CancerType.CERVICAL: cervical_guideline,
    CancerType.COLORECTAL: colorectal_guideline,
}

# === Public Interface === #
def get_screening_guideline(cancer_type: str, risk_score: int) -> int:
    try:
        rule = GUIDELINE_RULES[CancerType(cancer_type.lower())]
    except (ValueError, KeyError):
        rule = default_guideline
    return rule(risk_score)
