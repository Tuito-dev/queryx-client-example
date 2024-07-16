# QueryX Backend Example

## Table of Contents

- [QueryX Backend Example](#queryx-backend-example)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Try it on](#try-it-on)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Quick start](#quick-start)
    - [Use your own database](#use-your-own-database)
  - [Project Structure](#project-structure)
  - [API Endpoints](#api-endpoints)
  - [Contributing](#contributing)
  - [License](#license)

## Introduction

This project demonstrates how to use the QueryX backend with a native web app. It provides examples of various functionalities such as getting database info, setting a database, generating queries, and handling database operations.

## Try it on

[![Try it on CodePen](https://img.shields.io/badge/Try%20it%20on-CodePen-orange)](https://codepen.io/Tuito-Intuito/pen/yLWmwLB)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Tuito-dev/queryx-client-example.git
    ```
2. Navigate to the project directory:
    ```sh
    cd queryx-client-example/javascript-examples/structure_extraction
    ```
3. Install dependencies:
    ```bash
    npm install
    ```

## Usage

### Quick Start

1. Navigate to the right directory

  ```bash
    cd ../structure_extraction
  ```
2. Open `index.html` in your web browser.
3. Enter your API Key in the "Authorization Key" section.
4. Use [this given database example](../data/formula_1/formula_1.json) under the Set Database page.
5. Copy paste the example Business rules in the previous file in the dedicated field (businessRules). The example business rules are defined [here](../data/formula_1/formula_1-best_business_rules.txt).
6. Use the navigation drawer to access different functionalities.

### Use your own database

1. Please follow the [following steps](../README.md#use-your-own-database) for the database Structure generation in JSON format.
2. Open `index.html` in your web browser.
3. Enter your API Key in the "Authorization Key" section.
4. Enter your database in JSON format generated in the step 1 (../../data/<database_name>/<database_name>.json).
5. If needed, copy paste your defined Business rules in the previous file in the dedicated field (businessRules).
6. Use the navigation drawer to access different functionalities.

## Project Structure

- `index.html`: Main HTML file containing the structure of the web app.
- `script.js`: JavaScript file with all the logic for interacting with the QueryX API. # Maybe tell more about the logic
- `styles.css`: CSS file for styling the web app.
- `structure_extraction`: Node.js project to extract the database structure in JSON format.

## API Endpoints

The following API endpoints are used in this project:

- `GET /get-db-list`: Get the list of registered databases.
- `GET /get-db-structure/:dbUuid`: Get the structure of a database by its UUID.
- `POST /set-db`: Set a new database and get its UUID.
- `GET /get-suggested-questions/:dbUuid`: Get suggested questions based on a pre-question.
- `POST /generate-query/:dbUuid`: Generate a query based on a question.
- `POST /validate-query/:dbUuid`: Validate a generated query.
- `POST /reject-query/:dbUuid`: Reject a generated query.
- `POST /fix-query/:dbUuid`: Fix a query that generates an error.
- `DELETE /delete-db-cache/:dbUuid`: Delete the cache of a database.
- `DELETE /delete-db/:dbUuid`: Delete a database.

## Contributing

Contributions are welcome! Please feel free to [open issues](https://github.com/Tuito-dev/queryx-client-example/issues), and [disscussions](https://github.com/Tuito-dev/queryx-client-example/discussions) or give your feedbacks from [Contact us page](https://app.queryx.eu/#/contact)

## License

This project is licensed under the [MIT License](https://github.com/Tuito-dev/queryx-client-example/tree/main?tab=MIT-1-ov-file).