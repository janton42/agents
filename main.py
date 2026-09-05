import os

from outreach_agent.outreach_agent import OutreachAgent
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent

agent_options = [
    '1. Outreach Agent',
]


def main():
    print('Available Agents:')
    for i in range(len(agent_options)):
        print(agent_options[i])
    print()
    choice = input('Enter the number of your choice:\t')

    if choice == '1':
        load_dotenv()
        api_key = os.getenv('TAVILY_API_KEY')
        agent = OutreachAgent(
            api_key=api_key,
            db_file_path=BASE_DIR / 'outreach_agent' / 'dev_db' / 'outreach_candidates.db',
            sp_file_path=BASE_DIR / 'outreach_agent' / 'inputs' / 'community_partners.csv',
        )
        agent.execute_search()

    else:
        print('Invalid command')
        print('Loser...')


if __name__ == '__main__':
    main()
