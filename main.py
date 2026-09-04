from outreach_agent.outreach_agent import OutreachAgent
from pathlib import Path

BASE_DIR = Path(__file__).parent

if __name__ == '__main__':
    agent = OutreachAgent(
        db_file_path=BASE_DIR / 'outreach_agent' / 'dev_db' / 'outreach_candidates.db',
        sp_file_path=BASE_DIR / 'outreach_agent' / 'inputs' / 'community_partners.csv',
    )
    menu_options =[
        '1. Execute a search',
        '2. Quit',
    ]

    print('Outreach agent ready.')
    print('Available commands:')
    for i in range(len(menu_options)):
        print(menu_options[i])
    print()
    command = int(input('Enter the number of your choice:\t'))
    if command == 1:
        agent.execute_search()
    elif command == 2:
        print('Good bye.')
        print()
    else:
        print('Invalid command')
        print('Loser...')
