import json
import os
from datetime import datetime

MEMORY_FILE = "jarvis_memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    return {"facts": []}

def save_memory(memory):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f, indent=2)

def remember(fact):
    memory = load_memory()
    memory["facts"].append({
        "fact": fact,
        "saved_at": str(datetime.now())
    })
    save_memory(memory)
    return f"Remembered: {fact}"

def recall_all():
    memory = load_memory()
    facts = memory.get("facts", [])
    if not facts:
        return "Nothing saved in memory yet."
    lines = ["Here is what I remember:\n"]
    for i, f in enumerate(facts):
        lines.append(f"{i+1}. {f['fact']}")
    return "\n".join(lines)

def forget_all():
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)
    return "Memory wiped. Fresh start."

def get_facts_as_context():
    memory = load_memory()
    facts = memory.get("facts", [])
    if not facts:
        return ""
    lines = ["Things I know about my owner:"]
    for f in facts:
        lines.append(f"- {f['fact']}")
    return "\n".join(lines)