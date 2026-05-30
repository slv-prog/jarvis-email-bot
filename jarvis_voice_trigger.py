import requests
import os
from dotenv import load_dotenv
from jarvis_voice import listen_and_transcribe
from jarvis_commands import handle_command

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(text):
    chunks = [text[i:i+4000] for i in range(0, len(text), 4000)]
    for chunk in chunks:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": chunk}
        )

def run_voice_command():
    print("Jarvis Voice Mode - Press Enter to speak, Ctrl+C to quit")
    while True:
        input("\nPress Enter to speak...")
        send_telegram("Listening...")
        try:
            # Record and transcribe
            text = listen_and_transcribe()
            if not text:
                send_telegram("Could not hear anything. Try again.")
                continue
            print(f"You said: {text}")
            send_telegram(f"You said: {text}")
            # Process command
            send_telegram("Thinking...")
            response = handle_command(text)
            send_telegram(response)
        except Exception as e:
            send_telegram(f"Voice error: {e}")

if __name__ == '__main__':
    run_voice_command()