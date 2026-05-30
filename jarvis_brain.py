import anthropic
import os
from dotenv import load_dotenv
from jarvis_memory import get_facts_as_context, forget_all

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

conversation_history = []

def think(user_message, system_prompt=None):
    memory_context = get_facts_as_context()
    if system_prompt is None:
        system_prompt = f"""You are Jarvis, a personal AI assistant.
You are sharp, concise, and action-oriented.
You help your owner make money online through AI automation freelancing.
Always be direct. No fluff. Max 200 words unless writing a full document.
{memory_context}"""

    conversation_history.append({"role": "user", "content": user_message})
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=system_prompt,
        messages=conversation_history
    )
    reply = response.content[0].text
    conversation_history.append({"role": "assistant", "content": reply})
    if len(conversation_history) > 20:
        conversation_history.pop(0)
        conversation_history.pop(0)
    return reply

def clear_memory():
    conversation_history.clear()
    return forget_all()