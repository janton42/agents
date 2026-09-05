import json

from utils.tools import outreach_agent_tool_schema, web_search
from .system_prompt import funding_agent_system_prompt


# --- Agent loop ---
def agent_loop(api_key, model, provider):
    tools = [outreach_agent_tool_schema]
    messages = [
        {"role": "system", "content": funding_agent_system_prompt},
        {"role": "user", "content": "Find up to 10 funding opportunities for a non-profit."}
    ]

    while True:
        response = provider.chat(
            model=model,
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
                result = web_search(args["query"], api_key)

                messages.append({
                    "role": "tool",
                    "content": json.dumps(result),
                    "name": "web_search"
                })
