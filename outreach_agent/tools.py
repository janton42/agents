import os
from tavily import TavilyClient

# --- Tool definition ---

def web_search(query: str, api_key) -> dict:

    client = TavilyClient(api_key=api_key)
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