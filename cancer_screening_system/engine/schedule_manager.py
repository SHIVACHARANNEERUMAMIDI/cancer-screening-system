from datetime import datetime, timedelta

def get_next_screening_date(last_screening_date, interval_years):
    return last_screening_date + timedelta(days=interval_years * 365)
