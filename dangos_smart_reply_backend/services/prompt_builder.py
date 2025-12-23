def build_prompt(tasks: dict, question: str) -> str:
    context = ""

    for assignee, items in tasks.items():
        context += f"- {assignee} has {len(items)} tasks:\n"
        for item in items:
            context += f"  • {item['title']} ({item['status']})\n"

    return f"""
        You are an assistant analyzing project task distribution.

        Project context:
        {context}

        User question:
        "{question}"

        Answer based strictly on the context.
        If user asks to add or assign task, respond with a recommendation, not an action.
    """
