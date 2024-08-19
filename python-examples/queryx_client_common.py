#!/usr/bin/python3

"""
Common functions for different flavours of QueryX clients
"""

import os
import time
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
        """ colorama mock class """
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
PRINT_HTTP = False

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

#################
### CONSTANTS ###
#################

BACKEND_SERVER_URL = "https://api-prod.queryx.eu/be"
QUERYX_WEBSITE = "https://queryx.eu/"
QUERYX_SUBSCRIPTION = "https://app.queryx.eu/#/profil#ppage-api-key"
AUTHORIZATION_TOKEN = ""

# Paths below need to be adjusted for public github repo
DATABASE_FOLDER = '../data'

######################################
### PREDEFINED DATABASE STRUCTURES ###
######################################

PREDEFINED_DATABASE_STRUCTURE_LIST = [
    os.path.join(DATABASE_FOLDER, 'student_club', 'student_club.json'),
    os.path.join(DATABASE_FOLDER, 'formula_1', 'formula_1.json'),
]

def get_predefined_database_index(argv) -> int:
    """ Get database index in list of predefined databases from command line arguments """

    if len(argv) > 1:
        try:
            # Accept position in list
            index = int(argv[1])
            if 0 < index <= len(PREDEFINED_DATABASE_STRUCTURE_LIST):
                return index - 1
        except ValueError:
            # Accept name
            db_structure_name = argv[1]
            for i, db_structure in enumerate(PREDEFINED_DATABASE_STRUCTURE_LIST):
                if db_structure_name in db_structure:
                    return i
    return 0

def get_predefined_database_filename(argv) -> str:
    """ Get database structure file name from comamnd line arguments """

    index = get_predefined_database_index(argv)
    return PREDEFINED_DATABASE_STRUCTURE_LIST[index]

def get_predefined_database_structure(argv) -> dict:
    """ Get database structure from command line arguments """

    file_name = get_predefined_database_filename(argv)
    with open(file_name, encoding='utf-8') as json_file:
        database_structure = json.load(json_file)
    return database_structure

#####################
### AUTHORIZATION ###
#####################

def get_authorization_token() -> str:
    """ Get authorization token from environment variable """

    auth_token = os.environ.get('QUERYX_API_KEY', '')
    if auth_token:
        # Client authorized
        print("Please visit", c.Fore.CYAN + QUERYX_WEBSITE + c.Fore.RESET)
    else:
        # Client not authorized (duh)
        print_error("'QUERYX_API_KEY' not set")
        print("\nPlease claim your QueryX API key at",
              c.Fore.CYAN + QUERYX_SUBSCRIPTION + c.Fore.RESET)
        print("Then export as 'QUERYX_API_KEY' environment variable")
        print("  $ export QUERYX_API_KEY=<your API key>")
        auth_token = AUTHORIZATION_TOKEN
    print()
    return auth_token

#########################
### NETWORK FUNCTIONS ###
#########################

HTTP_REQUEST_SESSION = None

def init_requests(auth_token, keep_in_mind=True) -> requests.Session:
    """ Prepare HTTP requests """

    auth_header = {"authorization": auth_token}

    print_info(f"use QueryX backend @ {c.Fore.CYAN}{BACKEND_SERVER_URL}{c.Fore.RESET}")

    request_session = requests.Session()
    request_session.headers.update(auth_header)

    if keep_in_mind:
        global HTTP_REQUEST_SESSION
        HTTP_REQUEST_SESSION = request_session

    return request_session

def send_request(method: str,
                 endpoint: str,
                 uuid: str=None,
                 query_args: list[str]=None,
                 payload: dict=None,
                 request_session: requests.Session=None) -> dict:
    """ Send HTTP request to QueryX backend server, and check response """

    if request_session is None:
        request_session = HTTP_REQUEST_SESSION
    if request_session is None:
        print_error("need to init HTTP request session first")
        return None

    method_dict = {
        'get': request_session.get,
        'post': request_session.post,
        'delete': request_session.delete,
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
            if response.status_code == http.HTTPStatus.REQUEST_ENTITY_TOO_LARGE:
                serialized_payload = json.dumps(payload)
                print_error(f"request payload size = {len(serialized_payload)/1024/1024:.2f} MB")
            try: print_error(f"response = {json.dumps(response.json(), indent=2)}")
            except: pass
    except requests.exceptions.ConnectionError as request_error:
        print_error(f"{method}({endpoint}) request failed")
        print_error(request_error)
    return answer

##################
### MISC TOOLS ###
##################

def get_name(file_name: str) -> str:
    """ Return name from file name, ie. without path and extension """

    return os.path.splitext(os.path.basename(file_name))[0]

def get_timestamp() -> float:
    """ Get timestamp of now """

    return time.perf_counter()

def get_duration(start_timestamp) -> float:
    """ Get duration beween given timestamp and now """

    return round(time.perf_counter() - start_timestamp, 4)
