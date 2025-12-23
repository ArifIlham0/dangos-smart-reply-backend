def normalize_tasks(raw_tasks: list) -> dict:
    result = {}

    for task in raw_tasks:
        assignee = task.get("assignee") or "Unassigned"
        result.setdefault(assignee, []).append({
            "title": task["title"],
            "status": task["status"]
        })

    return result
