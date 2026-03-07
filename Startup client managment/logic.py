from datetime import date

def deadline_alert(deadline, role):
    days_left = (deadline - date.today()).days

    if role == "Manager" and days_left == 1:
        return "⚠ Deadline Tomorrow"
    if role in ["Team Lead", "Team Member"] and days_left == 5:
        return "⚠ Deadline in 5 Days"
    return None

def overloaded_team(task_count, limit=2):
    return task_count > limit
