from db_interactions import coordinate_candidate_db
from agent_loop import agent_loop
from response_parser import web_search_parser


class OutreachAgent:
    def __init__(self, **kwargs):
        self.db_file_path = kwargs['db_file_path']
        self.sp_file_path = kwargs['sp_file_path']
        self.final_output = None
        self.candidates = None
        self.confirmation = None

    def run_agent_loop(self):
        self.final_output = agent_loop()

    def parse_web_search(self):
        self.candidates = web_search_parser(self.final_output)

    def save_to_db(self):
        self.confirmation = coordinate_candidate_db(self.candidates, self.db_file_path, self.sp_file_path)

    def execute_search(self):
        self.run_agent_loop()
        self.parse_web_search()
        self.save_to_db()
        if self.confirmation:
            print(self.confirmation)
        else:
            print('Failed... You suck... Or I do...')
            print('Blame AI.')

if __name__ == '__main__':
    agent = OutreachAgent(
        db_file_path='./dev_db/outreach_candidates.db',
        sp_file_path='community_partners.csv',
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
