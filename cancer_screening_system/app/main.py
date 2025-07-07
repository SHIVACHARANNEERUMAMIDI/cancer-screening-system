import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Tuple, List
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from functools import lru_cache

from models.risk_model import calculate_risk
from engine.guideline_engine import get_screening_guideline
from engine.schedule_manager import get_next_screening_date
from engine.notification_system import send_reminder


# === Constants === #
DATE_FORMAT = "%Y-%m-%d"
CSV_PATH = Path("data/patients.csv")
parse_date = datetime.strptime
today = datetime.today()


# === Patient Data === #
@dataclass(frozen=True, slots=True)
class Patient:
    id: int
    age: int
    family_history: str
    lifestyle: str
    cancer_type: str
    last_screening: str


# === Parsing & Screening Logic === #
@lru_cache(maxsize=512)
def safe_parse_date(date_str: str) -> Optional[datetime]:
    try:
        return parse_date(date_str, DATE_FORMAT)
    except (ValueError, TypeError):
        return None

@lru_cache(maxsize=512)
def should_send_reminder(last: datetime, interval: int, today_: datetime) -> bool:
    return get_next_screening_date(last, interval) <= today_

def evaluate_patient(patient: Patient) -> Optional[Tuple[int, str]]:
    last_screening = safe_parse_date(patient.last_screening)
    if not last_screening:
        return None

    risk_score = calculate_risk(patient.age, patient.family_history, patient.lifestyle)
    interval = get_screening_guideline(patient.cancer_type, risk_score)

    if should_send_reminder(last_screening, interval, today):
        return patient.id, f"Screening due for {patient.cancer_type}."

    return None


# === Batch Processing === #
def process_patients(csv_path: Path) -> None:
    if not csv_path.is_file():
        raise FileNotFoundError(f"CSV not found: {csv_path.resolve()}")

    # Efficient bulk read
    df = pd.read_csv(csv_path, dtype={
        "id": int,
        "age": int,
        "family_history": str,
        "lifestyle": str,
        "cancer_type": str,
        "last_screening": str,
    })

    patients: List[Patient] = [Patient(**row) for row in df.to_dict(orient="records")]

    # Parallel reminder evaluation
    reminders: Dict[int, str] = {}
    with ThreadPoolExecutor(max_workers=8) as executor:
        for result in executor.map(evaluate_patient, patients):
            if result:
                patient_id, message = result
                reminders[patient_id] = message

    # Send reminders
    for pid, msg in reminders.items():
        send_reminder(pid, msg)


# === Entry Point === #
if __name__ == "__main__":
    process_patients(CSV_PATH)
