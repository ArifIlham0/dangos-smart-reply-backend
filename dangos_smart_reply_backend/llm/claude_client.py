import anthropic
import os

client = anthropic.Anthropic(
    api_key=os.getenv("CLAUDE_API_KEY")
)

def ask_claude(prompt: str) -> str:
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text
