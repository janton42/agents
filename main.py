import os
import ollama as llama

from utils.agent_classes.agents import SearchAgent
from pathlib import Path
from dotenv import load_dotenv
from utils.tools.tool_schemas import outreach_agent_tool_schema, funding_agent_tool_schema
from utils.tools.tool_registry import tool_registry
from utils.messages import outreach_agent_messages, funding_agent_messages

BASE_DIR = Path(__file__).parent
load_dotenv()

agent_options = [
    '1. Coding Boot Camp Partner Outreach Agent',
    '2. Funding Research Agent',
]

db_file_path = BASE_DIR / '.db' / 'research.db'
input_spreadsheet_path = BASE_DIR / 'utils' / 'inputs' / 'community_partners.csv'

def main():
    print('Available Agents:')
    for i in range(len(agent_options)):
        print(agent_options[i])
    print()
    choice = input('Enter the number of your choice:\t')

    if choice == '1':
        api_key = os.getenv('TAVILY_API_KEY')
        model = os.getenv('MODEL')
        agent = SearchAgent(
            purpose='outreach',
            api_key=api_key,
            provider=llama,
            model=model,
            tool_schema=outreach_agent_tool_schema,
            tool_registry=tool_registry,
            messages=outreach_agent_messages,
            db_file_path=db_file_path,
            input_file_path=input_spreadsheet_path,
        )
        agent.execute_search()

    elif choice == '2':
        api_key = os.getenv('TAVILY_API_KEY')
        model = os.getenv('MODEL')
        agent = SearchAgent(
            purpose='funding',
            api_key=api_key,
            provider=llama,
            model=model,
            tool_schema=funding_agent_tool_schema,
            tool_registry=tool_registry,
            messages=funding_agent_messages,
            db_file_path=db_file_path,
            input_file_path=None,
        )
        agent.execute_search()

    else:
        print('Invalid command')
        print('Loser...')


if __name__ == '__main__':
    main()
