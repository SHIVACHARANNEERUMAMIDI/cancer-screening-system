def get_screening_guideline(cancer_type, risk_score):
    if cancer_type == "breast":
        return 1 if risk_score > 4 else 2
    if cancer_type == "cervical":
        return 2 if risk_score > 3 else 3
    return 5  # Default interval in years
