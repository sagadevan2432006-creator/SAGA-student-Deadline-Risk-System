from datetime import date, timedelta


def generate_schedule(tasks, daily_hours=4):
    schedule = []

    for task in tasks:
        task_id = task[0]
        title = task[1]
        deadline = date.fromisoformat(task[2])
        effort = task[3]
        progress = task[5]

        remaining = effort * (1 - progress / 100)

        if remaining <= 0:
            continue

        current_date = date.today()

        while remaining > 0 and current_date <= deadline:
            hours = min(remaining, daily_hours)

            schedule.append({
                "date": current_date,
                "task": title,
                "hours": round(hours, 1)
            })

            remaining -= hours
            current_date += timedelta(days=1)

    return schedule