import ollama
import json

from tools import tool_schema, web_search
from system_prompt import system_prompt


# --- Agent loop ---
def agent_loop():
    tools = [tool_schema]
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
            return final_output

        for call in tool_calls:
            if call["function"]["name"] == "web_search":
                args = call["function"]["arguments"]
                result = web_search(args["query"])

                messages.append({
                    "role": "tool",
                    "content": json.dumps(result),
                    "name": "web_search"
                })
