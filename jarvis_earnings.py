import json
import os
from datetime import datetime
from jarvis_brain import think

EARNINGS_FILE = "jarvis_earnings.json"

def load_earnings():
    if os.path.exists(EARNINGS_FILE):
        with open(EARNINGS_FILE, 'r') as f:
            return json.load(f)
    return {
        "goal": 500,
        "currency": "USD",
        "earnings": [],
        "created": str(datetime.now())
    }

def save_earnings(data):
    with open(EARNINGS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def add_earning(amount, client, description):
    """Log a new payment."""
    data = load_earnings()
    entry = {
        "amount": float(amount),
        "client": client,
        "description": description,
        "date": str(datetime.now().strftime("%Y-%m-%d %H:%M")),
        "id": len(data["earnings"]) + 1
    }
    data["earnings"].append(entry)
    save_earnings(data)
    total = sum(e["amount"] for e in data["earnings"])
    goal = data["goal"]
    remaining = max(0, goal - total)
    percent = min(100, int((total / goal) * 100))
    return f"""Payment logged!

Amount: ${amount}
Client: {client}
Description: {description}

GOAL PROGRESS:
${total:.2f} of ${goal} earned ({percent}%)
${remaining:.2f} remaining to hit your goal

{"GOAL ACHIEVED! Time to raise your target!" if total >= goal else f"Keep going! {percent}% there."}"""

def get_report():
    """Generate full earnings report."""
    data = load_earnings()
    earnings = data["earnings"]
    if not earnings:
        return "No earnings logged yet. Use 'earned [amount] from [client] for [description]' to log your first payment."
    total = sum(e["amount"] for e in earnings)
    goal = data["goal"]
    remaining = max(0, goal - total)
    percent = min(100, int((total / goal) * 100))
    # Build progress bar
    filled = int(percent / 10)
    bar = "█" * filled + "░" * (10 - filled)
    lines = [
        "JARVIS EARNINGS REPORT",
        "=" * 30,
        f"\nGOAL: ${goal}",
        f"EARNED: ${total:.2f}",
        f"REMAINING: ${remaining:.2f}",
        f"\n[{bar}] {percent}%\n",
        "=" * 30,
        "\nALL PAYMENTS:\n"
    ]
    for e in earnings:
        lines.append(f"#{e['id']} | {e['date']}")
        lines.append(f"   ${e['amount']} from {e['client']}")
        lines.append(f"   {e['description']}\n")
    # Weekly summary
    from datetime import timedelta
    week_ago = datetime.now() - timedelta(days=7)
    weekly = [e for e in earnings
              if datetime.strptime(e['date'], "%Y-%m-%d %H:%M") > week_ago]
    weekly_total = sum(e["amount"] for e in weekly)
    lines.append("=" * 30)
    lines.append(f"THIS WEEK: ${weekly_total:.2f}")
    lines.append(f"TOTAL PAYMENTS: {len(earnings)}")
    if earnings:
        avg = total / len(earnings)
        lines.append(f"AVERAGE PER CLIENT: ${avg:.2f}")
    return "\n".join(lines)

def set_goal(amount):
    """Update earning goal."""
    data = load_earnings()
    data["goal"] = float(amount)
    save_earnings(data)
    return f"Goal updated to ${amount}. Let's get it Selva!"

def delete_earning(earning_id):
    """Delete an earning entry by ID."""
    data = load_earnings()
    before = len(data["earnings"])
    data["earnings"] = [e for e in data["earnings"] if e["id"] != int(earning_id)]
    if len(data["earnings"]) < before:
        save_earnings(data)
        return f"Entry #{earning_id} deleted."
    return f"Entry #{earning_id} not found."

def parse_earning_command(message):
    """Parse natural language earning commands."""
    prompt = f"""Extract payment details from this message: "{message}"

Return ONLY a JSON object with exactly these fields:
{{"amount": 150, "client": "John Smith", "description": "email automation bot"}}

Rules:
- amount must be a number only, no $ sign
- client is the person or company name
- description is what the work was for
- If any field is unclear use "unknown"

Return ONLY the JSON. No other text."""
    result = think(prompt)
    try:
        import json
        # Clean up response
        result = result.strip()
        if "```" in result:
            result = result.split("```")[1].replace("json", "").strip()
        data = json.loads(result)
        return data.get("amount"), data.get("client"), data.get("description")
    except:
        return None, None, None