#!/usr/bin/python3

"""
Client code example showing how to interact with Tuito's QueryX backend
"""

import sys
import json

from queryx_client_common import c, print_info, print_error, get_name
from queryx_client_common import get_predefined_database_list, get_predefined_database_filename
from queryx_client_common import get_authorization_token
from queryx_client_common import init_requests, send_request

#################
### CONSTANTS ###
#################

QUERYX_PROMPT = "Enter your question > "

##############
### CONFIG ###
##############

DELETE_CACHE = True

#############################
### QUERY GENERATION LOOP ###
#############################

def generate_queries(db_structure: dict, db_name: str) -> None:
    """
    Connect to QueryX backend, and enter an infinite loop of question / SQL query generations
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

    if DELETE_CACHE:
        print_info("Delete database cache")
        response = send_request('delete', 'delete-db-cache', uuid=db_uuid)
        if response is None:
            print_error("cannot delete database cache")
            return

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

    if len(sys.argv) > 1 and sys.argv[1] == "db":
        db_list = get_predefined_database_list()
        print("Available databases:")
        for db in db_list:
            print("  ", c.Fore.CYAN + str(db[0]) + c.Fore.RESET, "-", db[1])
        print()
        sys.exit(0)

    authorization_token = get_authorization_token()
    if authorization_token:

        db_filename = get_predefined_database_filename(sys.argv)
        with open(db_filename, encoding='utf-8') as json_file:
            database_structure = json.load(json_file)

        init_requests(authorization_token)
        PRINT_HTTP = False

        try:
            generate_queries(database_structure, get_name(db_filename))
        except KeyboardInterrupt:
            print(c.Fore.RED + "user interruption" + c.Fore.RESET)

        print("\nexit", program_name, "program, bye\n")
