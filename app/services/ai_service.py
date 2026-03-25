from anthropic import Anthropic
from app.config import settings

client = Anthropic(api_key=settings.anthropic_api_key)

def summarize(content: str) -> str:
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system="You are a research assistant. Summarize the given article in one concise paragraph focusing on key findings, arguments, and conclusions. Cover major details as much as possible",
        messages=[{
            "role": "user",
            "content": content
        }]
    )
    return message.content[0].text