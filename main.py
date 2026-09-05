import os
import ollama as llama

from outreach_agent.outreach_agent import OutreachAgent
from funding_agent.funding_agent import FundingAgent
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
load_dotenv()

agent_options = [
    '1. Coding Boot Camp Partner Outreach Agent',
    '2. Funding Research Agent',
]

db_file_path = BASE_DIR / '.db' / 'research.db'
def main():
    print('Available Agents:')
    for i in range(len(agent_options)):
        print(agent_options[i])
    print()
    choice = input('Enter the number of your choice:\t')

    if choice == '1':
        api_key = os.getenv('TAVILY_API_KEY')
        model = os.getenv('MODEL')
        agent = OutreachAgent(
            api_key=api_key,
            provider=llama,
            model=model,
            db_file_path=db_file_path,
            sp_file_path=BASE_DIR / 'outreach_agent' / 'inputs' / 'community_partners.csv',
        )
        agent.execute_search()

    elif choice == '2':
        api_key = os.getenv('TAVILY_API_KEY')
        model = os.getenv('MODEL')
        agent = FundingAgent(
            api_key=api_key,
            provider=llama,
            model=model,
            db_file_path=db_file_path,
        )
        agent.execute_search()

    else:
        print('Invalid command')
        print('Loser...')


if __name__ == '__main__':
    main()
