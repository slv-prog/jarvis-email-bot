import requests
import os
from dotenv import load_dotenv
from summariser import build_digest

load_dotenv()

def send_telegram(text):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    chunks = [text[i:i+4000] for i in range(0, len(text), 4000)]
    for chunk in chunks:
        url = f"https://api.telegram.org/bot8669826611:AAEplf6KtSi7-3tzkBGWGTCEqEx2RB5oqEo/sendMessage"
        r = requests.post(url, json={"chat_id": chat_id, "text": chunk})
        if r.status_code == 200:
            print("Telegram: delivered!")
        else:
            print(f"Telegram error: {r.text}")

def run_jarvis():
    print("Jarvis is running...")
    try:
        digest = build_digest()
        send_telegram(digest)
        print("Done!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    run_jarvis()