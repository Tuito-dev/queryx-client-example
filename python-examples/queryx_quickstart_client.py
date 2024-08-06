#!/usr/bin/python3

"""
Client code example showing how to interact with Tuito's QueryX backend
"""

import os
import sys
import json

from queryx_interactive_client import c, print_info, print_error, get_name
from queryx_interactive_client import init_requests, send_request

#################
### CONSTANTS ###
#################

BACKEND_SERVER_URL = "https://api-prod.queryx.eu/be"
QUERYX_WEBSITE = "https://queryx.eu/"
DATABASE_STRUCTURE_FILE = "../data/student_club/student_club.json"
QUERYX_PROMPT = "Enter your question > "

#########################
### PROCESS FUNCTIONS ###
#########################

def generate_queries(db_structure: dict) -> None:
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

    print_info("Declare database structure")
    response = send_request('post', 'set-db', payload=db_structure)
    if response is None:
        print_error("cannot declare database structure")
        return

    db_uuid = response['dbUuid']

    print_info("System ready\n")

    while True:
        user_input = input(QUERYX_PROMPT)

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
    print("   ##########################################")
    print("   ### Tuito's QueryX quick start example ###")
    print("   ##########################################")
    print(c.Fore.RESET)

    # Claim your API key at https://app.queryx.eu/#/profil#ppage-api-key
    # and export to environment
    authorization_token = os.environ.get('QUERYX_API_KEY', '')
    if not authorization_token:
        print_error("'QUERYX_API_KEY' not set")
        print("\nPlease export your QueryX API key as 'QUERYX_API_KEY' environment variable")
        print("  export QUERYX_API_KEY=<your API key>\n")
        exit(1)

    print("Please visit", c.Fore.CYAN + QUERYX_WEBSITE + c.Fore.RESET)
    print()

    with open(DATABASE_STRUCTURE_FILE, encoding='utf-8') as json_file:
        database_structure = json.load(json_file)

    init_requests(authorization_token)

    try:
        generate_queries(database_structure)
    except KeyboardInterrupt:
        print(c.Fore.RED + "user interruption" + c.Fore.RESET)

    print("\nexit", program_name, "program, bye\n")
    sys.exit(0)
