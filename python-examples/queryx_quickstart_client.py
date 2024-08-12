#!/usr/bin/python3

"""
Client code example showing how to interact with Tuito's QueryX backend
"""

import os
import sys
import json

from queryx_interactive_client import DATABASE_FOLDER, get_authorization_token
from queryx_interactive_client import c, print_info, print_error, get_name
from queryx_interactive_client import init_requests, send_request

#################
### CONSTANTS ###
#################

QUERYX_PROMPT = "Enter your question > "
DATABASE_STRUCTURE_FILE = os.path.join(DATABASE_FOLDER, 'student_club', 'student_club.json')

#########################
### PROCESS FUNCTIONS ###
#########################

def generate_queries(db_structure: dict, db_name: str) -> None:
    """
    Connect to QuaryX backend, and enter an infinite loop of question / SQL query generations
    """

    print_info("Check QueryX backend server is reachable")
    response = send_request('get', 'ping')
    if response is None:
        print_error("cannot reach QueryX backend")
        return

    print_info("Declare client")
    response = send_request('post', 'set-client')
    if response is None:
        print_error("cannot declare client")
        return

    print_info("Declare structure of", c.Fore.GREEN + db_name + c.Fore.RESET, "database")
    response = send_request('post', 'set-db', payload=db_structure)
    if response is None:
        print_error("cannot declare database structure")
        return

    db_uuid = response['dbUuid']

    print_info("System ready\n")

    while True:
        user_input = input(QUERYX_PROMPT)
        if len(user_input) == 0:
            continue  # skip empty user_input
        if user_input in ['q', 'quit', 'exit', 'bye', 'done']:
            break

        payload = {'question': user_input}
        response = send_request('post', 'generate-query', uuid=db_uuid, payload=payload)
        if response is None:
            print_error("SQL query generation failed")
            return

        print()
        if len(response['query']) > 0:
            print_info("QUESTION = " + c.Fore.CYAN + user_input + c.Fore.RESET)
            print_info("   QUERY = " + c.Fore.CYAN + response['query'] + c.Fore.RESET)
        elif len(response['answer']) > 0:
            print_info(c.Fore.MAGENTA + response['answer'] + c.Fore.RESET)
        print()

###################
### SCRIPT MAIN ###
###################

if __name__ == "__main__":

    program_name = get_name(sys.argv[0])

    print(c.Fore.MAGENTA)
    print("   #########################################")
    print("   ### Tuito's QueryX quick start client ###")
    print("   #########################################")
    print(c.Fore.RESET)

    authorization_token = get_authorization_token()
    if authorization_token:

        with open(DATABASE_STRUCTURE_FILE, encoding='utf-8') as json_file:
            database_structure = json.load(json_file)

        init_requests(authorization_token)
        PRINT_HTTP = False

        try:
            generate_queries(database_structure, get_name(DATABASE_STRUCTURE_FILE))
        except KeyboardInterrupt:
            print(c.Fore.RED + "user interruption" + c.Fore.RESET)

        print("\nexit", program_name, "program, bye\n")
