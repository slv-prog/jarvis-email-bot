from jarvis_memory import remember, recall_all
from jarvis_brain import think, clear_memory
from summariser import build_digest
from jarvis_search import web_search, search_and_summarise
from jarvis_jobs import scan_and_report, generate_proposal
from jarvis_earnings import add_earning, get_report, set_goal, delete_earning, parse_earning_command

def handle_command(message):
    msg = message.lower().strip()

    # MEMORY - check these FIRST
    if msg.startswith('remember '):
        fact = message[9:].strip()
        return remember(fact)

    elif msg in ['what do you remember', 'recall', 'what do you know']:
        return recall_all()

    elif msg in ['forget everything', 'wipe', 'clear memory']:
        return clear_memory()

    # SEARCH
    elif msg.startswith('search '):
        query = message[7:].strip()
        return search_and_summarise(query)

    elif msg.startswith('raw search '):
        query = message[11:].strip()
        return web_search(query)

    # JOBS - before EMAIL to avoid keyword conflicts
    elif msg.startswith('proposal for '):
        job_title = message[13:].strip()
        return generate_proposal(job_title, "")

    elif any(word in msg for word in ['scan jobs', 'scan for jobs', 'find me jobs', 'job scan']):
        return scan_and_report()

    elif any(word in msg for word in ['find jobs', 'search jobs', 'opportunities']):
        return cmd_find_jobs(message)

    # EMAIL
    elif any(word in msg for word in ['summarise my emails', 'summarize my emails', 'check my inbox', 'morning digest']):
        return cmd_summarise_emails()

    elif any(word in msg for word in ['draft', 'reply', 'respond', 'write back']):
        return cmd_draft_reply(message)

    # BUSINESS
    elif any(word in msg for word in ['upwork', 'apply']):
        return cmd_write_proposal(message)

    elif any(word in msg for word in ['fiverr', 'gig']):
        return cmd_write_gig(message)
    
    # EARNINGS
    elif any(word in msg for word in ['earned', 'got paid', 'received payment', 'payment received']):
        amount, client, description = parse_earning_command(message)
        if amount:
            return add_earning(amount, client, description)
        else:
            return "Could not parse payment. Try: earned $150 from John for email bot setup"

    elif any(word in msg for word in ['earnings report', 'how much have i earned', 'my earnings', 'show earnings', 'income report']):
        return get_report()

    elif msg.startswith('set goal '):
        amount = msg.replace('set goal ', '').replace('$', '').strip()
        return set_goal(amount)

    elif msg.startswith('delete earning '):
        earning_id = msg.replace('delete earning ', '').strip()
        return delete_earning(earning_id)

    # UTILITY
    elif msg in ['clear', 'reset']:
        return "Conversation cleared."

    elif any(word in msg for word in ['help', 'commands']):
        return cmd_help()

    # DEFAULT
    else:
        return think(message)


def cmd_summarise_emails():
    try:
        return build_digest()
    except Exception as e:
        return f"Could not fetch emails: {e}"


def cmd_draft_reply(message):
    prompt = f"""Draft a professional email reply for: {message}
Include subject line, body, sign-off. Under 150 words."""
    return think(prompt)


def cmd_write_proposal(message):
    prompt = f"""Write a winning Upwork proposal for: {message}
- Hook opening (mention similar work done)
- 3 bullet points of deliverables
- Timeline and price
- Call to action
Under 150 words. Sound human."""
    return think(prompt)


def cmd_write_gig(message):
    prompt = f"""Write a Fiverr gig description for: {message}
- Attention grabbing opening
- What buyer gets (bullets)
- Why choose me
- Call to action
Under 200 words. Focus on buyer benefit."""
    return think(prompt)


def cmd_find_jobs(message):
    prompt = f"""I build AI automation tools and email bots. Request: {message}
List 5 specific Upwork/Fiverr job titles to search right now.
For each: title, typical budget, one tip to win it."""
    return think(prompt)


def cmd_help():
    return """JARVIS COMMANDS:

EMAIL:
  summarise my emails
  draft a reply to [description]

JOBS:
  scan jobs
  proposal for [job title and description]
  find me jobs for [skill]

BUSINESS:
  write me an upwork proposal for [job]
  write me a fiverr gig for [service]

SEARCH:
  search [anything]
  raw search [anything]

MEMORY:
  remember [anything]
  what do you remember
  forget everything

EARNINGS:
  earned $[amount] from [client] for [description]
  my earnings report
  set goal [amount]
  delete earning [id]

Or just talk to me naturally."""