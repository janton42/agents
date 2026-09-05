import os
import ollama as llama

from outreach_agent.outreach_agent import OutreachAgent
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
load_dotenv()

agent_options = [
    '1. Coding Boot Camp Partner Outreach Agent',
    '2. Funding Research Agent',
]


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
            db_file_path=BASE_DIR / 'outreach_agent' / 'dev_db' / 'outreach_candidates.db',
            sp_file_path=BASE_DIR / 'outreach_agent' / 'inputs' / 'community_partners.csv',
        )
        agent.execute_search()

    elif choice == 2:
        # api_key = os.getenv('TAVILY_API_KEY')
        # model = os.getenv('MODEL')
        pass
    else:
        print('Invalid command')
        print('Loser...')


if __name__ == '__main__':
    main()
