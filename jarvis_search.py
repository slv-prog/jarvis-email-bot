import os
import requests
from dotenv import load_dotenv

load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def web_search(query):
    """Search the web and return a clean summary."""
    if not SERPAPI_KEY:
        return "No search API key found. Add SERPAPI_KEY to your .env file."
    try:
        params = {
            "q": query,
            "api_key": SERPAPI_KEY,
            "num": 5,
            "engine": "google"
        }
        r = requests.get("https://serpapi.com/search", params=params, timeout=10)
        data = r.json()
        results = data.get("organic_results", [])
        if not results:
            return "No results found."
        lines = [f"Search results for: {query}\n"]
        for i, result in enumerate(results[:5]):
            title = result.get("title", "No title")
            snippet = result.get("snippet", "No description")
            link = result.get("link", "")
            lines.append(f"{i+1}. {title}")
            lines.append(f"   {snippet}")
            lines.append(f"   {link}\n")
        return "\n".join(lines)
    except Exception as e:
        return f"Search failed: {e}"

def search_and_summarise(query):
    """Search the web then summarise results with Jarvis brain."""
    from jarvis_brain import think
    raw_results = web_search(query)
    prompt = f"""Here are web search results for: {query}

{raw_results}

Summarise the key findings in 5 bullet points.
Be concise and practical. Focus on what's useful for a freelancer building an AI automation business."""
    return think(prompt)