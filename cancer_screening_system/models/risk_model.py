def calculate_risk(age, family_history, lifestyle):
    score = 0
    if age > 50:
        score += 2
    if family_history:
        score += 3
    if lifestyle == "smoker":
        score += 2
    return score
