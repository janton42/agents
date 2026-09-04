import os
from tavily import TavilyClient
from dotenv import load_dotenv

# --- Tool definition ---

def web_search(query: str) -> dict:
    # Load environment variables at runtime, not at module import
    load_dotenv()
    tavily_key = os.getenv('TAVILY_API_KEY')

    # Initialize client at runtime, not at module import
    client = TavilyClient(api_key=tavily_key)
    results = client.search(query=query, max_results=5)
    return results

tool_schema = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Search the web for information about veteran-serving organizations.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query"}
            },
            "required": ["query"]
        }
    }
}