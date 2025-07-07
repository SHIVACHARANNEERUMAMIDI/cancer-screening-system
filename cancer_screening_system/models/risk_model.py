from typing import Callable, Dict, Any, Tuple, Protocol, runtime_checkable
from enum import IntEnum
from dataclasses import dataclass
from functools import lru_cache
import threading


# === Protocol for Rule Functions === #
@runtime_checkable
class RuleFunc(Protocol):
    def __call__(self, value: Any) -> int: ...


# === Enum with Bitmask Weighting === #
class Lifestyle(IntEnum):
    SMOKER = 1 << 1       # 2
    ALCOHOLIC = 1 << 2    # 4
    SEDENTARY = 1 << 3    # 8
    HEALTHY = 0

    @classmethod
    def score(cls, value: str) -> int:
        try:
            return cls[value.upper()].value
        except KeyError:
            return 0


# === DataClass for Rule === #
@dataclass(frozen=True, slots=True)
class RiskRule:
    key: str
    apply: RuleFunc


# === Super Optimized Risk Calculator === #
class RiskCalculator:
    __slots__ = ("_rules", "_lock")

    def __init__(self):
        self._rules: Dict[str, RiskRule] = {}
        self._lock = threading.Lock()
        self._register_defaults()

    def _register_defaults(self) -> None:
        self._rules = {
            "age": RiskRule("age", self._age_rule),
            "family_history": RiskRule("family_history", self._family_history_rule),
            "lifestyle": RiskRule("lifestyle", self._lifestyle_rule),
        }

    def register_custom_rule(self, key: str, func: RuleFunc) -> None:
        with self._lock:
            self._rules[key] = RiskRule(key, func)

    @lru_cache(maxsize=1024)
    def calculate(self, data: Tuple[Tuple[str, Any], ...]) -> int:
        return sum(self._rules[k].apply(v) for k, v in data if k in self._rules)

    # === Rule Implementations === #
    @staticmethod
    def _age_rule(age: int) -> int:
        return (age > 50) * 2

    @staticmethod
    def _family_history_rule(history: Any) -> int:
        return 3 if bool(history) else 0

    @staticmethod
    def _lifestyle_rule(lifestyle: str) -> int:
        return Lifestyle.score(lifestyle)


# === Thread-safe Singleton === #
class RiskCalculatorSingleton:
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get_instance(cls) -> RiskCalculator:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = RiskCalculator()
        return cls._instance


# === Public Interface (Immutable, Cached) === #
def calculate_risk(age: int, family_history: Any, lifestyle: str) -> int:
    data: Tuple[Tuple[str, Any], ...] = (
        ("age", age),
        ("family_history", family_history),
        ("lifestyle", lifestyle),
    )
    return RiskCalculatorSingleton.get_instance().calculate(data)
