import ollama
import json
import sqlite3
import csv
import os
import re

from tavily import TavilyClient
from dotenv import load_dotenv
# --- Environment Variables ---

load_dotenv()
tavily_key = os.getenv('TAVILY_API_KEY')

# --- Tool definition ---

def web_search(query: str) -> str:
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

tools = [tool_schema]

system_prompt = """You are a research assistant helping a nonprofit find veteran-serving organizations
for outreach partnerships.

CRITERION: A valid candidate is an employee or volunteer at any organization that serves veterans in some capacity
(e.g. VSOs, VA-affiliated groups, veteran nonprofits, county veteran commissions,
veteran resource centers, transition assistance programs).

For each valid candidate you find, gather these fields:
- org_name
- contact_email
- social_links (check Facebook, LinkedIn, and X only — up to 3 platforms)
- justification (one sentence on why this org fits the criterion)

Exclude general email addresses (e.g. info@, customerservice@, or {orgabbreviation}@). Find individual employee's work
emails only. If they are a volunteer, like the case of a county veteran commissioner, a personal email is acceptable. 

Prioritize professional, organizational (e.g. @va.gov, @dav.org, amvets.org) over personal email addresses (e.g. 
@hotmail.com, @gmail.com, @yahoo.com).

Social links should only be organizational or professional, not personal. For example, if a person has an official X account
associated with their office, include that. If they only have a personal account, use an organizational social account instead.

Use the web_search tool to find candidates and verify each one meets the criterion
before including it.

Stop searching once you have found exactly 10 valid candidates. Do not continue
searching after reaching 10.

Return the final list as structured JSON: a list of objects with keys
org_name, contact_email, social_links, justification. Return ONLY the JSON, no
other text.
"""

# --- Agent loop ---

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "Find 10 veteran-serving organizations for outreach partnerships."}
]

while True:
    response = ollama.chat(
        model="minimax-m3:cloud",
        messages=messages,
        tools=tools
    )

    messages.append(response["message"])

    tool_calls = response["message"].get("tool_calls")

    if not tool_calls:
        final_output = response["message"]["content"]
        break

    for call in tool_calls:
        if call["function"]["name"] == "web_search":
            args = call["function"]["arguments"]
            result = web_search(args["query"])

            messages.append({
                "role": "tool",
                "content": json.dumps(result),
                "name": "web_search"
            })

# --- Parse ---
match = re.search(r"```(?:json)?\s*(.*?)```", final_output, re.DOTALL)
if match:
    cleaned = match.group(1).strip()
else:
    cleaned = final_output.strip()

candidates = json.loads(cleaned)
# --- Load existing emails from spreadsheet ---

existing_emails = set()

csv_path = "community_partners.csv"
if os.path.exists(csv_path):
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            email = row.get("EMAIL")
            if email:
                existing_emails.add(email.strip().lower())

# --- Set up db ---

conn = sqlite3.connect("outreach_candidates.db")
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        org_name TEXT,
        contact_email TEXT UNIQUE,
        social_links TEXT,
        justification TEXT
    )
""")

# --- Load existing emails already in db ---

cur.execute("SELECT contact_email FROM candidates")
existing_emails.update(
    row[0].strip().lower() for row in cur.fetchall() if row[0]
)

# --- Filter and insert ---

inserted = 0
skipped = 0

for c in candidates:
    email = (c.get("contact_email") or "").strip().lower()

    if not email or email in existing_emails:
        skipped += 1
        continue

    cur.execute(
        "INSERT INTO candidates (org_name, contact_email, social_links, justification) VALUES (?, ?, ?, ?)",
        (c.get("org_name"), email, json.dumps(c.get("social_links")), c.get("justification"))
    )
    existing_emails.add(email)
    inserted += 1

conn.commit()
conn.close()

print(f"Inserted: {inserted}, Skipped (duplicate/missing email): {skipped}")
