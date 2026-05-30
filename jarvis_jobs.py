import requests
from bs4 import BeautifulSoup
from jarvis_brain import think
from dotenv import load_dotenv
import os

load_dotenv()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

SEARCH_TERMS = [
    "email automation",
    "AI automation python",
    "gmail bot",
    "n8n automation",
    "python automation script"
]

def search_upwork(query):
    """Search Upwork for jobs matching query."""
    try:
        url = f"https://www.upwork.com/nx/search/jobs/?q={query.replace(' ', '%20')}&sort=recency"
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        jobs = []
        # Extract job listings
        listings = soup.find_all('div', {'class': lambda x: x and 'job-tile' in x})
        for listing in listings[:5]:
            title_el = listing.find('h2')
            desc_el = listing.find('p')
            budget_el = listing.find('span', {'class': lambda x: x and 'budget' in str(x).lower()})
            if title_el:
                jobs.append({
                    'title': title_el.get_text(strip=True),
                    'description': desc_el.get_text(strip=True)[:200] if desc_el else 'No description',
                    'budget': budget_el.get_text(strip=True) if budget_el else 'Budget not listed'
                })
        return jobs
    except Exception as e:
        return []

def search_via_serpapi(query):
    """Search for Upwork jobs via SerpAPI."""
    SERPAPI_KEY = os.getenv("SERPAPI_KEY")
    if not SERPAPI_KEY:
        return []
    try:
        params = {
            "q": f"site:upwork.com/jobs {query}",
            "api_key": SERPAPI_KEY,
            "num": 5,
            "engine": "google"
        }
        r = requests.get("https://serpapi.com/search", params=params, timeout=10)
        data = r.json()
        results = data.get("organic_results", [])
        jobs = []
        for result in results[:5]:
            jobs.append({
                'title': result.get('title', 'No title').replace('- Upwork', '').strip(),
                'description': result.get('snippet', 'No description')[:200],
                'budget': 'See listing',
                'link': result.get('link', '')
            })
        return jobs
    except Exception as e:
        return []

def scan_all_jobs():
    """Scan for jobs across all search terms."""
    all_jobs = []
    for term in SEARCH_TERMS:
        jobs = search_via_serpapi(term)
        if jobs:
            for job in jobs:
                job['search_term'] = term
                all_jobs.append(job)
    return all_jobs[:10]  # Return top 10

def format_jobs(jobs):
    """Format jobs into clean readable list."""
    if not jobs:
        return "No jobs found right now. Try again in a few hours."
    lines = ["JOB SCAN RESULTS\n" + "="*30 + "\n"]
    for i, job in enumerate(jobs):
        lines.append(f"{i+1}. {job['title']}")
        lines.append(f"   Budget: {job['budget']}")
        lines.append(f"   {job['description'][:150]}...")
        if job.get('link'):
            lines.append(f"   Link: {job['link']}")
        lines.append("")
    return "\n".join(lines)

def scan_and_report():
    """Full scan — find jobs and return formatted report."""
    jobs = scan_all_jobs()
    formatted = format_jobs(jobs)
    # Ask Jarvis to pick the best 3
    prompt = f"""Here are freelance job listings found online:

{formatted}

I am Selva — a beginner freelancer who builds AI automation tools, email bots, and Python scripts.
My goal is to earn $500 this month.

Pick the TOP 3 jobs that best match my skills.
For each job explain in one sentence why it's a good fit.
Then rank them 1 (apply first) to 3 (apply last)."""
    analysis = think(prompt)
    return formatted + "\n\nJARVIS ANALYSIS:\n" + analysis

def generate_proposal(job_title, job_description):
    """Generate a ready-to-send proposal for a specific job."""
    prompt = f"""Write a winning Upwork proposal for this job:

Job Title: {job_title}
Job Description: {job_description}

About me: I am Selva, a self-taught developer who builds AI automation tools.
I recently built a personal AI assistant that reads Gmail, summarises emails with Claude AI,
executes voice commands, searches the web, and delivers results via Telegram.
GitHub: https://github.com/slv-prog/jarvis-email-bot

Write a proposal that:
- Opens with a specific hook (mention my email bot as proof)
- Lists exactly what I will deliver (3 bullet points)
- Mentions my GitHub as portfolio proof
- Ends with a confident call to action
- Sounds human, not robotic
- Is under 150 words

Return ONLY the proposal text. Nothing else."""
    return think(prompt)