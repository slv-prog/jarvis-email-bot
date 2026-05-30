import anthropic
from dotenv import load_dotenv
import os
from gmail_fetch import fetch_emails

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def summarise_email(email):
    prompt = f"""You are an email assistant. Read this email and respond with EXACTLY this format:

SUMMARY: [1-2 sentences describing what this email is about and what action if any is needed]
URGENT: [YES or NO - is a response or action needed today?]
FROM: {email['sender']}
SUBJECT: {email['subject']}

EMAIL BODY:
{email['body'][:400]}

Be concise. No extra text."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=150,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

def build_digest():
    print("Fetching emails...")
    emails = fetch_emails()
    if not emails:
        return "No emails in the last 24 hours."
    digest_parts = ["YOUR MORNING EMAIL DIGEST", "="*35]
    urgent = []
    normal = []
    print(f"\nSummarising {len(emails)} emails with Claude...")
    for i, email in enumerate(emails):
        print(f"  Processing {i+1}/{len(emails)}...")
        summary = summarise_email(email)
        if "URGENT: YES" in summary:
            urgent.append(summary)
        else:
            normal.append(summary)
    if urgent:
        digest_parts.append("\nNEEDS YOUR ATTENTION\n")
        digest_parts.extend(urgent)
    if normal:
        digest_parts.append("\nOTHER EMAILS\n")
        digest_parts.extend(normal)
    digest_parts.append(f"\n{len(emails)} emails processed. Have a great day.")
    return "\n\n".join(digest_parts)

if __name__ == '__main__':
    digest = build_digest()
    print("\n" + digest)