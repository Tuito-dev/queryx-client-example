# Python Examples

## Table of Contents

- [Python Examples](#python-examples)
  - [Introduction](#introduction)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Quick Start](#quick-start)
    - [Complete example](#complete-example)
  - [Use your own database](#use-your-own-database)
  - [Complete Example Menu](#complete-example-menu)
    - [Menu Presentation](#menu-presentation)
  - [Contributing](#contributing)
  - [License](#license)

## Introduction

This Python script is a QueryX client example. It demonstrates how to interact with the QueryX backend API to finally generate SQL queries from questions asked in natural language.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Tuito-dev/python-examples.git
    ```

2. Navigate to the project directory:
    ```sh
    cd python-examples
    ```

3. Create virtual environement (optional but recommended)
    ```sh
    python3 -m venv queryx-venv # Create a virtual environement named queryx-venv
    source queryx-venv/bin/activate # Activate the created virtual environement
    pip install --upgrade pip setuptools wheel # Make sure having the latest pip setup
    ```

4. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

This project offers two ways to explore its functionalities: a [quick start](#quick-start) example and a [more complete](#complete-example) example showcasing QueryX BE API usage.

You can use either the [provided example databases](#example-datasets) or apply it to your [own databases](#use-your-own-database).

### Quick start

1. **Set your API key**: Please export your QueryX API Key as follows:
    ```sh
     export QUERYX_API_KEY=YOUR_API_KEY
    ```

2. Run the following:

```sh
python queryx_quickstart_example.py
```

Follow the instructions displayed in the script's output to ask your questions in natural language.

### Complete example

1. **Set your API key**: Please export your QueryX API Key as follows:
    ```sh
     export QUERYX_API_KEY=YOUR_API_KEY
    ```

2. Run the following:

```sh
python python-examples/queryx_client.py
```

For detailed instructions on using the complete example, refer to the section on [menu navigation part](#menu-navigation).

### Use your own database

1. **Generate the database JSON structure**: please follow [these steps](../README.md#use-your-own-database).

2. **Run**:

  - **Quick start mode**: please point to your generated database structured JSON format [in this line](https://github.com/Tuito-dev/queryx-client-example/blob/main/python-examples/queryx_quickstart_example.py#L89), then follow the [steps here](#quick-start).

  - **Complete mode**: follow the [steps here](#complete-example).

## Complete Example Menu

The QueryX client UI is a menu where one can navigate using arrows and `enter` keys.

![Complete Example Menu dataset demo](../assets/demo.gif)

### Menu presentation

- Menu items surrounded by '*  *' characters do not perform any request to QueryX backend, they're just used to navigate, while all others perform a request

The menu contains 3 sub-menus:

- Database selection menu:

```
current database: none selected
> ping
  set-client
  * select database *
  set-db
  update-db
  delete-db
  * start *
  * exit *
```

Before generating a query, following actions must be done:

  - Declare yourself as client with set-client request
  - Select a database among all available database schema json files

```
> * cancel * 
  student_club
  formula_1      
```

  - Declare the database on QueryX backend with set-db request
  - Then go to 'New query' menu with * start * menuitem

- New query menu

```
> get-db-structure
  get-suggested-questions 
  generate-query
  delete-db-cache
  * back *
```

- In order to access the 'Query management' menu, generate a first SQK query

- Query management menu

```
> get-db-structure
  fix-query
  validate-query
  reject-query
  get-suggested-questions
  generate-query
  delete-db-cache
  * restart with another query *
```

## Contributing

Contributions are welcome! Please feel free to [open issues](https://github.com/Tuito-dev/queryx-client-example/issues), and [disscussions](https://github.com/Tuito-dev/queryx-client-example/discussions) or give your feedbacks from [Contact us page](https://app.queryx.eu/#/contact)

## License

This project is licensed under the [MIT License](https://github.com/Tuito-dev/queryx-client-example/tree/main?tab=MIT-1-ov-file).

**Keywords**: queryx, api, python, javascript, nodejs, json, examples, backend, openapi, tuito, natural language to sql, sql queries, ai, artificial intelligence, query translation, data querying, sql generation, text2sql, speech2sql, SQL copilot, SQL coder
