#!/usr/bin/python3

"""
Client code example showing how to interact with Tuito's QueryX backend
"""

import os
import sys
import glob
import json
import yaml
import http
import urllib
import requests
import argparse
import datetime

from collections import OrderedDict

from simple_term_menu import TerminalMenu

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

def get_user_input_string(user_input: str) -> str:
    """ Debug trace string format helper """
    return "WITH INPUT " + user_input if len(user_input) > 0 else ""

#################
### CONSTANTS ###
#################

BACKEND_SERVER_URL = "https://api-prod.queryx.eu/be"
QUERYX_WEBSITE = "https://queryx.eu/"
QUERYX_AUTH_SERVER ="https://app.queryx.eu/#/profil#ppage-api-key"
SCHEMA_SEMANTIC_KEY = 'businessRules'
DATABASE_FOLDER = '../data'

###############################
### STATE MACHINE VARIABLES ###
###############################

class DatabaseId:
    """ Structure gathering database attributes, which are all public and with direct access """

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        """ Reset the database attributes to None """
        self.name = None
        self.file = None
        self.uuid = None
        self.schema = None

CURRENT_DATABASE = DatabaseId()
QUESTION_QUERY_HISTORY = []

######################
### MISC FUNCTIONS ###
######################

def get_name(file_name: str) -> str:
    """ Return name from file name, ie. without path and extension """
    return os.path.splitext(os.path.basename(file_name))[0]

def handle_query(question: str, response: dict) -> None:
    """ Print SQL query response, and save it in history """
    print()
    if len(response['query']) > 0:
        print_info("QUESTION = " + c.Fore.CYAN + question + c.Fore.RESET)
        print_info("   QUERY = " + c.Fore.CYAN + response['query'] + c.Fore.RESET)
        QUESTION_QUERY_HISTORY.append({'question': question, 'query': response['query']})
    elif len(response['answer']) > 0:
        print_info(c.Fore.MAGENTA + response['answer'] + c.Fore.RESET)
    print()

#########################
### NETWORK FUNCTIONS ###
#########################

HTTP_REQUEST_SESSION = None

def init_requests(auth_token):
    """ Prepare HTTP requests """

    auth_header = {"authorization": auth_token}

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

MESSAGE_NEED_DB_SELECTION = c.Fore.RED + "please select a database first" + c.Fore.RESET
MESSAGE_NEED_DB_SET = c.Fore.RED + "please perform a 'set-db' request first" + c.Fore.RESET

def proceed_ping(process_description: str="", user_input: str="") -> bool:
    """ Perform a PING request to QueryX backend server
    used to check it is up and running"""
    print_trace(process_description, get_user_input_string(user_input))

    send_request('get', 'ping')

    return True

def proceed_set_client(process_description: str="", user_input: str="") -> bool:
    """ Perform a SET-CLIENT request to QueryX backend server
    used to declare the client presence """
    print_trace(process_description, get_user_input_string(user_input))

    send_request('post', 'set-client')

    return True

def proceed_set_db(process_description: str="", user_input: str="") -> bool:
    """ Perform a SET-DB request to QueryX backend server
    used to set a database schema """
    print_trace(process_description, get_user_input_string(user_input))

    if CURRENT_DATABASE.name is None:
        print_info(MESSAGE_NEED_DB_SELECTION)
        return False

    db_schema = CURRENT_DATABASE.schema
    response = send_request('post', 'set-db', payload=db_schema)
    if response is None:
        return False

    CURRENT_DATABASE.uuid = response.get('dbUuid', None)

    return True

def proceed_update_db(process_description: str="", user_input: str="") -> bool:
    """ Perform a UPDATE-DB request to QueryX backend server
    used to update the database schema """
    print_trace(process_description, get_user_input_string(user_input))

    if CURRENT_DATABASE.uuid is None:
        print_info(MESSAGE_NEED_DB_SET)
        return False

    response = send_request('post', 'update-db', payload=CURRENT_DATABASE.schema)
    if response is None:
        return False

    CURRENT_DATABASE.uuid = response.get('dbUuid', None)

    return True

def proceed_delete_db(process_description: str="", user_input: str="") -> bool:
    """ Perform a DELETE-DB request to QueryX backend server
    used to remove the database schema """
    print_trace(process_description, get_user_input_string(user_input))

    if CURRENT_DATABASE.uuid is None:
        print_info(MESSAGE_NEED_DB_SET)
        return False

    send_request('delete', 'delete-db', uuid=CURRENT_DATABASE.uuid)

    CURRENT_DATABASE.reset()

    return True

def proceed_delete_db_cache(process_description: str="", user_input: str="") -> bool:
    """ Perform a DELETE-DB-CACHE request to QueryX backend server
    used to erase the history of questions with generated queries """
    print_trace(process_description, get_user_input_string(user_input))

    if CURRENT_DATABASE.uuid is None:
        print_info(MESSAGE_NEED_DB_SET)
        return False

    send_request('delete', 'delete-db-cache', uuid=CURRENT_DATABASE.uuid)

    return True

def proceed_get_db(process_description: str="", user_input: str="") -> bool:
    """ Perform a GET-DB-STRUCTURE request to QueryX backend server
    used to retrieve the database schema for printing """
    print_trace(process_description, get_user_input_string(user_input))

    if CURRENT_DATABASE.uuid is None:
        print_info(MESSAGE_NEED_DB_SET)
        return False

    send_request('get', 'get-db-structure', uuid=CURRENT_DATABASE.uuid)

    return True

def proceed_get_suggestions(process_description: str="", user_input: str="") -> bool:
    """ Perform a GET-SUGGESTED-QUESTIONS request to QueryX backend server
    used to get and print questions that could inspire the user """
    print_trace(process_description, get_user_input_string(user_input))

    if CURRENT_DATABASE.uuid is None:
        print_info(MESSAGE_NEED_DB_SET)
        return False

    query_args = ('preQuestion', user_input)

    send_request('get', 'get-suggested-questions', uuid=CURRENT_DATABASE.uuid, query_args=[query_args])

    return True

def proceed_generate(process_description: str="", user_input: str="") -> bool:
    """ Perform a GENERATE-QUERY request to QueryX backend server
    used to generate a SQL query from a natural language question """
    print_trace(process_description, get_user_input_string(user_input))

    if CURRENT_DATABASE.uuid is None:
        print_info(MESSAGE_NEED_DB_SET)
        return False

    payload = {'question': user_input}
    response = send_request('post', 'generate-query', uuid=CURRENT_DATABASE.uuid, payload=payload)
    if response is None:
        return False

    handle_query(user_input, response)

    return True

def proceed_generate_next(process_description: str="", user_input: str="") -> bool:
    """ Perform a GENERATE-QUERY request to QueryX backend server
    used to generate a SQL query taking previous query into account for context """
    print_trace(process_description, get_user_input_string(user_input))

    payload = {
        'question': user_input,
        'history': QUESTION_QUERY_HISTORY,
    }
    response = send_request('post', 'generate-query', uuid=CURRENT_DATABASE.uuid, payload=payload)
    if response is None:
        return False

    handle_query(user_input, response)

    return True

def proceed_fix(process_description: str="", user_input: str="") -> bool:
    """ Perform a FIX-QUERY request to QueryX backend server
    used to correct the generated SQL query with a change """
    print_trace(process_description, get_user_input_string(user_input))

    last_qq_pair = QUESTION_QUERY_HISTORY.pop()
    payload = {
        "question": last_qq_pair.get('question', ""),
        "query": last_qq_pair.get('query', ""),
        "errors": [user_input],
        "history": QUESTION_QUERY_HISTORY
    }
    response = send_request('post', 'fix-query', uuid=CURRENT_DATABASE.uuid, payload=payload)
    if response is None:
        return False

    QUESTION_QUERY_HISTORY.append({'question': user_input, 'query': response['query']})

    return True

def proceed_validate(process_description: str="", user_input: str="") -> bool:
    """ Perform a VALIDATE-QUERY request to QueryX backend server
    used to set the generated SQL query as valid """
    print_trace(process_description, get_user_input_string(user_input))

    last_qq_pair = QUESTION_QUERY_HISTORY[-1]
    payload = {
        "question": last_qq_pair.get('question', ""),
        "query": last_qq_pair.get('query', ""),
        "threshold": str(1), # rfu
    }
    send_request('post', 'validate-query', uuid=CURRENT_DATABASE.uuid, payload=payload)

    return True

def proceed_reject(process_description: str="", user_input: str="") -> bool:
    """ Perform a VALIDATE-QUERY request to QueryX backend server
    used to set the generated SQL query as invalid """
    print_trace(process_description, get_user_input_string(user_input))

    last_qq_pair = QUESTION_QUERY_HISTORY[-1]
    payload = {
        "question": last_qq_pair.get('question', ""),
        "query": last_qq_pair.get('query', ""),
    }
    send_request('post', 'reject-query', uuid=CURRENT_DATABASE.uuid, payload=payload)

    return True

def proceed_select_db(process_description: str="", user_input: str="") -> bool:
    """ Select a database for all next operations """
    print_trace(process_description, get_user_input_string(user_input))

    if process_description != SUBMENUITEM_KEY_CANCEL:
        CURRENT_DATABASE.file = process_description
        CURRENT_DATABASE.name = get_name(CURRENT_DATABASE.file)

        with open(CURRENT_DATABASE.file, encoding='utf-8') as json_file:
            CURRENT_DATABASE.schema = json.load(json_file)

    return True

def proceed_start(process_description: str="", user_input: str="") -> bool:
    """ Clear question/query history """
    print_trace(process_description, get_user_input_string(user_input))

    if CURRENT_DATABASE.uuid is None:
        print_info(MESSAGE_NEED_DB_SET)
        return False

    return True

def proceed_restart(process_description: str="", user_input: str="") -> bool:
    """ Clear question/query history """
    print_trace(process_description, get_user_input_string(user_input))

    QUESTION_QUERY_HISTORY.clear()

    return True

def proceed_edit_semantics(process_description: str="", user_input: str="") -> bool:
    """ Retrieve the list of semantics of current database
    and show it in a new semantic rule live sub-menu """
    print_trace(process_description, get_user_input_string(user_input))

    # Copy semantics from current database schema to semantics sub-menu of menu definition
    add_semantic_list_to_menu()

    # Build semantics live sub-menu
    build_semantics_submenu()

    return True

def proceed_edit_semantic(process_description: str="", user_input: str="") -> bool:
    """ Edit one single semantic rule """
    print_trace(process_description, get_user_input_string(user_input))

    semantic_list = CURRENT_DATABASE.schema.get(SCHEMA_SEMANTIC_KEY)
    semantic_index = semantic_list.index(process_description)
    if len(user_input) > 0:
        semantic_list[semantic_index] = user_input
        print_info("replaced semantic", process_description, "with", user_input)
    else:
        semantic_list.pop(semantic_index)
        print_info("deleted semantic", process_description)

    return True

def proceed_add_semantic(process_description: str="", user_input: str="") -> bool:
    """ Add a new semantic rule to the list of semantics of current database """
    print_trace(process_description, get_user_input_string(user_input))

    semantic_list = CURRENT_DATABASE.schema.get(SCHEMA_SEMANTIC_KEY)
    if len(user_input) > 0:
        semantic_list.append(user_input)
        print_info("added semantic", user_input)
    else:
        print_info("finally no new semantic")

    return True

def proceed_save_semantics(process_description: str="", user_input: str="") -> bool:
    """ Save the list of semantics into current database schema file """
    print_trace(process_description, get_user_input_string(user_input))

    time_tag = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    file_name = CURRENT_DATABASE.file(".json", f"-{time_tag}.json")
    print_debug("save semantics into", file_name)
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(CURRENT_DATABASE.schema, json_file, indent=2)

    return True

def exit_program(process_description: str="", user_input: str="") -> bool:
    """ Exit program (indeed, this is the best docstring ever) """
    print_trace(process_description, get_user_input_string(user_input))

    print_info("exit program, bye\n")
    sys.exit(0)

#######################
### MENU DEFINITION ###
#######################

SUBMENU_KEY_MAIN = 'MAIN'
SUBMENU_KEY_DATABASE = 'DB'
SUBMENU_KEY_SEMANTICS = 'SEMANTIC'
SUBMENU_KEY_QUESTION = 'QUESTION'
SUBMENU_KEY_QUERY = 'QUERY'

SUBMENUITEM_KEY_NEW = "* new *"
SUBMENUITEM_KEY_START = "* start *"
SUBMENUITEM_KEY_DONE = "* done *"
SUBMENUITEM_KEY_SAVE = "* save *"
SUBMENUITEM_KEY_CANCEL = "* cancel *"
SUBMENUITEM_KEY_BACK = "* back *"
SUBMENUITEM_KEY_EXIT = "* exit *"

ENDMENUITEM_KEY_D = 'description'
ENDMENUITEM_KEY_I = 'need-input'
ENDMENUITEM_KEY_A = 'action'
ENDMENUITEM_KEY_M = 'next-menu'

# SEMANTICS menu is not ready yet
# Need to be inserted between select-db and set-db menuitems
# TODO: insert & fix semantics menu
'''
("* edit semantics *", {
    ENDMENUITEM_KEY_D: "edit semantics of selected database\n(need to select one first)",
    ENDMENUITEM_KEY_I: None,
    ENDMENUITEM_KEY_A: proceed_edit_semantics,
    ENDMENUITEM_KEY_M: SUBMENU_KEY_SEMANTICS,
}),
'''

QUERYX_CLIENT_MENU_DEFINITION = {

    SUBMENU_KEY_MAIN: OrderedDict([
        ("ping", {
            ENDMENUITEM_KEY_D: "check QueryX backend is up and running by sending a 'ping' request",
            ENDMENUITEM_KEY_I: None,
            ENDMENUITEM_KEY_A: proceed_ping,
            ENDMENUITEM_KEY_M: None,
        }),
        ("set-client", {
            ENDMENUITEM_KEY_D: "declare yourself onto the QueryX backend by sending a 'set-client' request",
            ENDMENUITEM_KEY_I: None,
            ENDMENUITEM_KEY_A: proceed_set_client,
            ENDMENUITEM_KEY_M: None,
        }),
        ("* select database *", {
            ENDMENUITEM_KEY_D: "select a database",
            ENDMENUITEM_KEY_I: None,
            ENDMENUITEM_KEY_A: None,
            ENDMENUITEM_KEY_M: SUBMENU_KEY_DATABASE,
        }),
        ("set-db", {
            ENDMENUITEM_KEY_D: "set selected database onto the QueryX backend by sending a 'set-db' request\n(need to select a database first)",
            ENDMENUITEM_KEY_I: None,
            ENDMENUITEM_KEY_A: proceed_set_db,
            ENDMENUITEM_KEY_M: None,
        }),
        ("update-db", {
            ENDMENUITEM_KEY_D: "update the selected database with semantics onto the QueryX backend by sending a 'update-db' request\n(need to set a database first)",
            ENDMENUITEM_KEY_I: None,
            ENDMENUITEM_KEY_A: proceed_update_db,
            ENDMENUITEM_KEY_M: None,
        }),
        ("delete-db", {
            ENDMENUITEM_KEY_D: "unselect the database & delete from QueryX backend by sending a 'delete-db' request\n(need to set a database first)",
            ENDMENUITEM_KEY_I: None,
            ENDMENUITEM_KEY_A: proceed_delete_db,
            ENDMENUITEM_KEY_M: None,
        }),
        (SUBMENUITEM_KEY_START, {
            ENDMENUITEM_KEY_D: "enter the 'query generation' menu to start to generate some queries\n(need to set a database first)",
            ENDMENUITEM_KEY_I: None,
            ENDMENUITEM_KEY_A: proceed_start,
            ENDMENUITEM_KEY_M: SUBMENU_KEY_QUESTION,
        }),
        (SUBMENUITEM_KEY_EXIT, {
            ENDMENUITEM_KEY_D: "exit QueryX client program",
            ENDMENUITEM_KEY_I: None,
            ENDMENUITEM_KEY_A: exit_program,
            ENDMENUITEM_KEY_M: None,
        }),
    ]),

    SUBMENU_KEY_DATABASE: OrderedDict([
        (SUBMENUITEM_KEY_CANCEL, {
            ENDMENUITEM_KEY_D: "cancel database selection",
            ENDMENUITEM_KEY_I: None,
            ENDMENUITEM_KEY_A: None,
            ENDMENUITEM_KEY_M: SUBMENU_KEY_MAIN,
        }),
    ]),

    SUBMENU_KEY_SEMANTICS: OrderedDict([
        (SUBMENUITEM_KEY_NEW, {
            ENDMENUITEM_KEY_D: "add a new semantic rule",
            ENDMENUITEM_KEY_I: "enter the new semantic rule",
            ENDMENUITEM_KEY_A: proceed_add_semantic,
            ENDMENUITEM_KEY_M: SUBMENU_KEY_SEMANTICS,
        }),
        (SUBMENUITEM_KEY_DONE, {
            ENDMENUITEM_KEY_D: "validate these semantics",
            ENDMENUITEM_KEY_I: None,
            ENDMENUITEM_KEY_A: None,
            ENDMENUITEM_KEY_M: SUBMENU_KEY_MAIN,
        }),
        (SUBMENUITEM_KEY_SAVE, {
            ENDMENUITEM_KEY_D: "save these semantics to schema file",
            ENDMENUITEM_KEY_I: None,
            ENDMENUITEM_KEY_A: proceed_save_semantics,
            ENDMENUITEM_KEY_M: None,
        }),
    ]),

    SUBMENU_KEY_QUESTION: OrderedDict([
        ("get-db-structure", {
            ENDMENUITEM_KEY_D: "show database structure by sending a 'get-db-structure' request",
            ENDMENUITEM_KEY_I: None,
            ENDMENUITEM_KEY_A: proceed_get_db,
            ENDMENUITEM_KEY_M: None,
        }),
        ("get-suggested-questions", {
            ENDMENUITEM_KEY_D: "get examples of questions from scratch, or from a question fragment, by sending a 'get-suggested-questions' request",
            ENDMENUITEM_KEY_I: "enter a question fragment (or press enter to get from scratch)",
            ENDMENUITEM_KEY_A: proceed_get_suggestions,
            ENDMENUITEM_KEY_M: None,
        }),
        ("generate-query", {
            ENDMENUITEM_KEY_D: "generate a SQL query from a question expressed in natural language by sending a 'generate-query' request",
            ENDMENUITEM_KEY_I: "enter a question to query the database",
            ENDMENUITEM_KEY_A: proceed_generate,
            ENDMENUITEM_KEY_M: SUBMENU_KEY_QUERY,
        }),
        ("delete-db-cache", {
            ENDMENUITEM_KEY_D: "erase question/query history on QueryX backend by sending a 'delete-db-cache' request",
            ENDMENUITEM_KEY_I: None,
            ENDMENUITEM_KEY_A: proceed_delete_db_cache,
            ENDMENUITEM_KEY_M: None,
        }),
        (SUBMENUITEM_KEY_BACK, {
            ENDMENUITEM_KEY_D: "back to 'database selection' menu",
            ENDMENUITEM_KEY_I: None,
            ENDMENUITEM_KEY_A: None,
            ENDMENUITEM_KEY_M: SUBMENU_KEY_MAIN,
        }),
    ]),

    SUBMENU_KEY_QUERY: OrderedDict([
        ("get-db-structure", {
            ENDMENUITEM_KEY_D: "show database structure by sending a 'get-db-structure' request",
            ENDMENUITEM_KEY_I: None,
            ENDMENUITEM_KEY_A: proceed_get_db,
            ENDMENUITEM_KEY_M: None,
        }),
        ("fix-query", {
            ENDMENUITEM_KEY_D: "fix the last generated SQL query by sending a 'fix-query' request",
            ENDMENUITEM_KEY_I: "describe the error in the last generated SQL query",
            ENDMENUITEM_KEY_A: proceed_fix,
            ENDMENUITEM_KEY_M: None,
        }),
        ("validate-query", {
            ENDMENUITEM_KEY_D: "validate the last generated SQL query by sending a 'validate-query' request",
            ENDMENUITEM_KEY_I: None,
            ENDMENUITEM_KEY_A: proceed_validate,
            ENDMENUITEM_KEY_M: None,
        }),
        ("reject-query", {
            ENDMENUITEM_KEY_D: "reject the last generated SQL query by sending a 'reject-query' request",
            ENDMENUITEM_KEY_I: None,
            ENDMENUITEM_KEY_A: proceed_reject,
            ENDMENUITEM_KEY_M: None,
        }),
        ("get-suggested-questions", {
            ENDMENUITEM_KEY_D: "get examples of questions from scratch, or from a question fragment, by sending a 'get-suggested-questions' request",
            ENDMENUITEM_KEY_I: "enter a question fragment (or press enter to get from scratch)",
            ENDMENUITEM_KEY_A: proceed_get_suggestions,
            ENDMENUITEM_KEY_M: None,
        }),
        ("generate-query", {
            ENDMENUITEM_KEY_D: "generate a SQL query from a new question and using current query by sending a 'generate-query' request",
            ENDMENUITEM_KEY_I: "enter a question taking previous one into account",
            ENDMENUITEM_KEY_A: proceed_generate_next,
            ENDMENUITEM_KEY_M: None,
        }),
        ("delete-db-cache", {
            ENDMENUITEM_KEY_D: "erase question/query history on QueryX backend by sending a 'delete-db-cache' request",
            ENDMENUITEM_KEY_I: None,
            ENDMENUITEM_KEY_A: proceed_delete_db_cache,
            ENDMENUITEM_KEY_M: None,
        }),
        ("* restart with another query *", {
            ENDMENUITEM_KEY_D: "back to 'query generation' menu to generate another query, loosing current context",
            ENDMENUITEM_KEY_I: None,
            ENDMENUITEM_KEY_A: proceed_restart,
            ENDMENUITEM_KEY_M: SUBMENU_KEY_QUESTION,
        }),
    ]),
}

#######################
### MENU MANAGEMENT ###
#######################

QUERYX_CLIENT_MENU_LIVE = { }
SUBMENU_KEY = SUBMENU_KEY_MAIN

def preview_description(key: str) -> str:
    """ Preview the menu item description """

    return QUERYX_CLIENT_MENU_DEFINITION[SUBMENU_KEY][key][ENDMENUITEM_KEY_D]

def build_menu() -> None:
    """ Build the QueryX client live menu following menu definition """

    add_database_list_to_menu(DATABASE_FOLDER)

    for submenu_key, submenu in QUERYX_CLIENT_MENU_DEFINITION.items():
        menu_item_list = submenu.keys()
        print_debug("submenu '", submenu_key, "' list =", menu_item_list)
        QUERYX_CLIENT_MENU_LIVE[submenu_key] = TerminalMenu(menu_item_list,
                                                            raise_error_on_interrupt=True,
                                                            cycle_cursor=False,
                                                            preview_command=preview_description)

def build_semantics_submenu() -> None:
    """ Build the semantics live sub-menu following menu definition """

    del QUERYX_CLIENT_MENU_LIVE[SUBMENU_KEY_SEMANTICS]
    menu_item_list = QUERYX_CLIENT_MENU_DEFINITION[SUBMENU_KEY_SEMANTICS].keys()
    print_debug("submenu ' semantics ' list =", menu_item_list)
    QUERYX_CLIENT_MENU_LIVE[SUBMENU_KEY_SEMANTICS] = TerminalMenu(menu_item_list,
                                                                  raise_error_on_interrupt=True,
                                                                  cycle_cursor=False)

def add_semantic_list_to_menu() -> None:
    """ Retrieve the list of semantic rules available in of current database schema
    and insert in the menu definition, as semantics sub-menu """

    # First, remove all semantics from menu definition (but keep 'cancel', 'new', 'save')
    semantics_submenu = QUERYX_CLIENT_MENU_DEFINITION[SUBMENU_KEY_SEMANTICS]
    print_debug("add", len(semantics_submenu), "items to semantics menu")
    while len(semantics_submenu) > 3:
        for semantic_rule, semantic_menu_item in semantics_submenu.items():
            if semantic_rule not in [SUBMENUITEM_KEY_NEW, SUBMENUITEM_KEY_DONE, SUBMENUITEM_KEY_SAVE]:
                del semantic_menu_item
                break
    print_debug("semantics menu after clean-up =", semantics_submenu)

    # Then, rebuild semantic list within menu definition
    if CURRENT_DATABASE.schema is not None:
        semantic_list = CURRENT_DATABASE.schema.get(SCHEMA_SEMANTIC_KEY, [])
        for semantic_rule in semantic_list:
            semantics_submenu[semantic_rule] = {
                ENDMENUITEM_KEY_D: semantic_rule,
                ENDMENUITEM_KEY_I: "type the new version of the semantic rule, keep empty to delete",
                ENDMENUITEM_KEY_A: proceed_edit_semantic,
                ENDMENUITEM_KEY_M: SUBMENU_KEY_SEMANTICS,
            }
    print_debug("semantics menu at the end =", semantics_submenu)

def add_database_list_to_menu(database_folder: str) -> None:
    """ Retrieve the list of databases available in database folder
    and insert in the menu definition, as database sub-menu """

    db_file_list = glob.glob(os.path.join(database_folder, "**", "*" + '.json'), recursive=True)
    print_debug("database file list =", db_file_list)

    database_submenu = QUERYX_CLIENT_MENU_DEFINITION[SUBMENU_KEY_DATABASE]
    for db_file in db_file_list:
        db_name = get_name(db_file)
        print_debug("add", db_name)
        database_submenu[db_name] = {
            ENDMENUITEM_KEY_D: db_file,
            ENDMENUITEM_KEY_I: None,
            ENDMENUITEM_KEY_A: proceed_select_db,
            ENDMENUITEM_KEY_M: SUBMENU_KEY_MAIN,
        }

def get_menu_item_key(submenu: OrderedDict, index: int) -> str:
    """ Get key in sub-menu definition (ordered dictionary) based on index """

    # This function would be not needed if the TerminalMenu object could provide labels from index
    # but don't know if it does, need to check, so meanwhile here it is

    for i, key in enumerate(submenu):
        if i == index:
            return key
    return None # could have checked index with len(submenu) before, but it's ok

#################
### MENU LOOP ###
#################

def read_user_input(prompt: str) -> str:
    """ Read user input from standard input """
    return input("$ " + prompt + " > ")

def menu_loop(database_file: str=None) -> None:
    """ Main menu loop """

    build_menu()

    if database_file is not None:
        CURRENT_DATABASE.file = database_file
        CURRENT_DATABASE.name = get_name(CURRENT_DATABASE.file)

    global SUBMENU_KEY
    SUBMENU_KEY = SUBMENU_KEY_MAIN

    while SUBMENU_KEY is not None:

        if CURRENT_DATABASE.uuid is not None:
            print("current database:", c.Fore.GREEN + CURRENT_DATABASE.name + c.Fore.RESET, "/", c.Fore.GREEN + CURRENT_DATABASE.uuid + c.Fore.RESET)
        elif CURRENT_DATABASE.name is not None:
            print("current database:", c.Fore.GREEN + CURRENT_DATABASE.name + c.Fore.RESET, "(not yet set)")
        else:
            print("current database: none selected")

        valid = True # going to next menu can be invalided by process
        submenu = QUERYX_CLIENT_MENU_DEFINITION[SUBMENU_KEY]
        index = QUERYX_CLIENT_MENU_LIVE[SUBMENU_KEY].show()
        submenu_item_key = get_menu_item_key(submenu, index)
        if submenu_item_key is None:
            print_error("menu definition mismatch,", index, "is out of range")
            continue # more an assert for us than a user input
        print_debug("menu item key =", submenu_item_key)
        submenu_item = submenu[submenu_item_key]

        user_input = ""
        if submenu_item[ENDMENUITEM_KEY_I] is not None:
            print_debug(ENDMENUITEM_KEY_D, "needs user input")
            user_input = read_user_input(submenu_item[ENDMENUITEM_KEY_I])

        if submenu_item[ENDMENUITEM_KEY_A] is not None:
            print_debug("execute", ENDMENUITEM_KEY_D, get_user_input_string(user_input))
            valid = submenu_item[ENDMENUITEM_KEY_A](submenu_item[ENDMENUITEM_KEY_D], user_input)

        if submenu_item[ENDMENUITEM_KEY_M] is not None and valid:
            SUBMENU_KEY = submenu_item[ENDMENUITEM_KEY_M]
            print_debug("go to submenu", SUBMENU_KEY)

###################
### SCRIPT MAIN ###
###################

if __name__ == "__main__":

    program_name = get_name(sys.argv[0])

    parser = argparse.ArgumentParser(prog=program_name,
                                     description="simple QueryX client for QueryX backend")
    parser.add_argument("-db", "--database",
                        type=str,
                        metavar="<database-file>",
                        default=None,
                        help="Select database file, will be done dynamically if not provided")
    command_line_args = parser.parse_args()

    print(c.Fore.MAGENTA)
    print("   #############################")
    print("   ### Tuito's QueryX client ###")
    print("   #############################")
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

    init_requests(authorization_token)
    PRINT_HTTP = True

    try:
        menu_loop(command_line_args.database)
    except KeyboardInterrupt:
        print(c.Fore.RED + "user interruption" + c.Fore.RESET)

    print("\nexit", program_name, "program, bye\n")
    sys.exit(0)
