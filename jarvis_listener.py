import requests
import time
import os
import sys
from dotenv import load_dotenv
from jarvis_commands import handle_command

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"
running = True

def send_message(text):
    chunks = [text[i:i+4000] for i in range(0, len(text), 4000)]
    for chunk in chunks:
        requests.post(f"{BASE_URL}/sendMessage", json={
            "chat_id": CHAT_ID,
            "text": chunk
        })

def get_updates(offset=None):
    params = {"timeout": 5, "offset": offset}
    try:
        r = requests.get(f"{BASE_URL}/getUpdates", params=params, timeout=10)
        return r.json().get("result", [])
    except:
        return []

def run():
    global running
    print("Jarvis is listening... Press Ctrl+C to stop.")
    send_message("Jarvis online. Ready for commands Selva. Type help to see what I can do.")
    offset = None
    try:
        while running:
            updates = get_updates(offset)
            for update in updates:
                offset = update["update_id"] + 1
                msg = update.get("message", {})
                chat_id = str(msg.get("chat", {}).get("id", ""))
                text = msg.get("text", "").strip()
                if chat_id == str(CHAT_ID) and text:
                    print(f"Command received: {text}")
                    send_message("Thinking...")
                    try:
                        response = handle_command(text)
                        send_message(response)
                    except Exception as e:
                        send_message(f"Error: {e}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down Jarvis...")
        send_message("Jarvis going offline. See you soon Selva. Your memory is saved.")
        sys.exit(0)

if __name__ == '__main__':
    run()