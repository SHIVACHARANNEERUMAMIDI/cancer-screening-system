import pandas as pd
from models.risk_model import calculate_risk
from engine.guideline_engine import get_screening_guideline
from engine.schedule_manager import get_next_screening_date
from engine.notification_system import send_reminder
from datetime import datetime

data = pd.read_csv('data/patients.csv')

for _, row in data.iterrows():
    risk = calculate_risk(row['age'], row['family_history'], row['lifestyle'])
    interval = get_screening_guideline(row['cancer_type'], risk)
    last_screening = datetime.strptime(row['last_screening'], "%Y-%m-%d")
    next_screening = get_next_screening_date(last_screening, interval)

    if next_screening <= datetime.today():
        send_reminder(row['id'], f"Screening due for {row['cancer_type']}.")
