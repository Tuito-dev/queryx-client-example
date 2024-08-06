#!/usr/bin/python3

"""
Client code example showing how to interact with Tuito's QueryX backend
"""

import os
import json
import http
import urllib
import requests

#######################
### PRINT UTILITIES ###
#######################

try:
    import colorama as c
except ModuleNotFoundError:
    class c:
        class Fore:
            GREEN = ""
            YELLOW = ""
            RED = ""
            CYAN = ""
            MAGENTA = ""
        class Style:
            RESET = ""

PRINT_HEADER = "QueryX Client"

# This print management is really basic & naive (sorry about that)
# It should be improved, use logging ?

PRINT_TRACE = False
PRINT_DEBUG = False
PRINT_INFO = True
PRINT_ERROR = True
PRINT_HTTP = True

def print_trace(*args) -> None:
    """ Basic print function """
    if PRINT_TRACE:
        print(PRINT_HEADER + " TRACE:", *args)

def print_debug(*args) -> None:
    """ Basic print function """
    if PRINT_DEBUG:
        print(PRINT_HEADER + " DEBUG:", *args)

def print_info(*args) -> None:
    """ Basic print function """
    if PRINT_INFO:
        print(PRINT_HEADER + ":", *args)

def print_error(*args) -> None:
    """ Basic print function """
    if PRINT_ERROR:
        print(PRINT_HEADER + c.Fore.RED + " ERROR:" + c.Fore.RESET, *args)

def print_request(*args) -> None:
    """ Basic print function """
    if PRINT_HTTP:
        print(PRINT_HEADER + c.Fore.YELLOW + " REQ:" + c.Fore.RESET, *args)

def print_response(*args) -> None:
    """ Basic print function """
    if PRINT_HTTP:
        print(PRINT_HEADER +  c.Fore.YELLOW + " RES:    " + c.Fore.RESET, *args)

def get_user_input_string(user_input: str) -> str:
    """ Debug trace string format helper """
    return "WITH INPUT " + user_input if len(user_input) > 0 else ""

#################
### CONSTANTS ###
#################

# Claim your authorization token at https://app.queryx.eu/#/profil#ppage-api-key
# and copy/paste here
AUTHORIZATION_TOKEN = os.environ.get('QUERYX_API_KEY', '')

if not AUTHORIZATION_TOKEN:
    print_error("Please export your QueryX API key as an environment variable: QUERYX_API_KEY (export QUERYX_API_KEY=YOUR_API_KEY)")
    exit(1)

QUERYX_WEBSITE = "https://queryx.eu/"
BACKEND_SERVER_URL = "https://api-prod.queryx.eu/be"
DATABASE_STRUCTURE_FILE = "../data/student_club/student_club.json"
QUERYX_PROMPT = "Enter your question > "

#########################
### NETWORK FUNCTIONS ###
#########################

HTTP_REQUEST_SESSION = None

def init_requests():
    """ Prepare HTTP requests """

    auth_header = {"authorization": AUTHORIZATION_TOKEN}

    global HTTP_REQUEST_SESSION
    HTTP_REQUEST_SESSION = requests.Session()
    HTTP_REQUEST_SESSION.headers.update(auth_header) # unnecessary for ping request, but won't hurt

def send_request(method: str,
                 endpoint: str,
                 uuid: str=None,
                 query_args: list[str]=None,
                 payload: dict=None) -> dict:
    """ Send HTTP request to QueryX backend server, and check response """

    method_dict = {
        'get': HTTP_REQUEST_SESSION.get,
        'post': HTTP_REQUEST_SESSION.post,
        'delete': HTTP_REQUEST_SESSION.delete,
    }

    if method not in method_dict:
        # This is more an assert than a user error
        print_error(f"method {method} is not supported")
        return None

    answer = None
    try:
        url = f"{BACKEND_SERVER_URL}/{endpoint}"
        if uuid is not None:
            url += "/" + uuid
        if query_args is not None:
            arg_separator = "?"
            while len(query_args) > 0:
                query_arg = query_args.pop(0)
                url += arg_separator + query_arg[0] + "=" + urllib.parse.quote_plus(query_arg[1])
                arg_separator = "&"
        print_request(f"send {method}({url})")
        if payload is None:
            response = method_dict[method](url)
        else:
            response = method_dict[method](url, json=payload)
        print_debug("got", response)
        if response.status_code == http.HTTPStatus.OK:
            answer = response.json()
            print_response(json.dumps(answer, indent=2))
        else:
            print_error(f"{method}({endpoint}) request returned {response.status_code}")
            print_error(f"response = {json.dumps(response.json(), indent=2)}")
    except requests.exceptions.ConnectionError as request_error:
        print_error(f"{method}({endpoint}) request failed")
        print_error(request_error)
    return answer

#########################
### PROCESS FUNCTIONS ###
#########################

def generate_queries(db_structure: dict) -> None:
    """
    Connect to QuaryX backend, and enter an infinite loop of question / SQL query generations
    """

    init_requests()

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

    print(c.Fore.MAGENTA)
    print("   ##########################################")
    print("   ### Tuito's QueryX quick start example ###")
    print("   ##########################################")
    print(c.Fore.RESET)
    print("Please visit", c.Fore.CYAN + QUERYX_WEBSITE + c.Fore.RESET)
    print()

    with open(DATABASE_STRUCTURE_FILE, encoding='utf-8') as json_file:
        database_structure = json.load(json_file)

    try:
        generate_queries(database_structure)
    except KeyboardInterrupt:
        print(c.Fore.RED + "user interruption" + c.Fore.RESET)
