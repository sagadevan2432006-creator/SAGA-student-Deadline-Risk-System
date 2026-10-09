from datetime import date


def calculate_risk(deadline, effort, priority, progress):
    deadline_date = date.fromisoformat(deadline)
    days_left = (deadline_date - date.today()).days

    remaining_effort = effort * (1 - progress / 100)

    score = 0

    # Deadline factor
    if days_left <= 1:
        score += 40
    elif days_left <= 3:
        score += 30
    elif days_left <= 7:
        score += 15

    # Effort factor
    effort_score = min(30, remaining_effort * 3)
    score += effort_score

    # Priority factor
    if priority == "High":
        score += 20
    elif priority == "Medium":
        score += 10

    # Progress factor
    if progress < 25:
        score += 10

    if score >= 60:
        return "High Risk"
    elif score >= 35:
        return "Medium Risk"
    else:
        return "Low Risk"