def detect_platform(value: str) -> str:
    if "notion.site" in value:
        return "notion"
    if "trello.com" in value:
        return "trello"
    if "atlassian.net" in value:
        return "jira"
    if "clickup.com" in value:
        return "clickup"
    raise ValueError("Unsupported platform")
