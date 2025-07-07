from abc import ABC, abstractmethod
from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Literal, Dict
from functools import lru_cache

# === Constants === #
SUPPORTED_UNITS = Literal["years", "months", "weeks"]
DEFAULT_UNIT = "years"

# === Interface === #
class IntervalPolicy(ABC):
    __slots__ = ()

    @abstractmethod
    def get_next_date(self, last_screening: datetime, interval_value: int) -> datetime:
        pass

# === Stateless Singleton Strategies === #
class YearlyInterval(IntervalPolicy):
    __slots__ = ()

    def get_next_date(self, last_screening: datetime, interval_value: int) -> datetime:
        return last_screening + relativedelta(years=interval_value)

class MonthlyInterval(IntervalPolicy):
    __slots__ = ()

    def get_next_date(self, last_screening: datetime, interval_value: int) -> datetime:
        return last_screening + relativedelta(months=interval_value)

class WeeklyInterval(IntervalPolicy):
    __slots__ = ()

    def get_next_date(self, last_screening: datetime, interval_value: int) -> datetime:
        return last_screening + relativedelta(weeks=interval_value)

# === Policy Registry with Lazy Singleton Instantiation === #
class IntervalEngine:
    __slots__ = ("_policies",)

    def __init__(self):
        self._policies: Dict[str, IntervalPolicy] = {
            "years": YearlyInterval(),
            "months": MonthlyInterval(),
            "weeks": WeeklyInterval(),
        }

    @lru_cache(maxsize=128)
    def get_next_screening_date(
        self,
        last_screening: datetime,
        interval_value: int,
        unit: SUPPORTED_UNITS = DEFAULT_UNIT
    ) -> datetime:
        if interval_value <= 0:
            raise ValueError("Interval value must be a positive integer.")

        policy = self._policies.get(unit)
        if not policy:
            raise ValueError(f"Unsupported interval unit: '{unit}'. Must be one of: {list(self._policies.keys())}")

        return policy.get_next_date(last_screening, interval_value)

# === Singleton Instance === #
_interval_engine = IntervalEngine()

# === Public API === #
def get_next_screening_date(
    last_screening_date: datetime,
    interval_value: int,
    unit: SUPPORTED_UNITS = DEFAULT_UNIT
) -> datetime:
    return _interval_engine.get_next_screening_date(last_screening_date, interval_value, unit)
