# Structure Extraction

This project provides examples demonstrating how to extract the JSON structure of a database (SQLite, MySQL, MSSQL, PostgreSQL, and MariaDB) using Python. The extracted structure can be formatted to be used with the QueryX application on one hand or with the APIs on the other hand, the structure slightly differs for both cases.

## Table of Contents

- [Structure Extraction](#structure-extraction)
  - [Table of Contents](#table-of-contents)
  - [Project Structure](#project-structure)
  - [Usage](#usage)
    - [Extracting Database Structure](#extracting-database-structure)
  - [Expected Output Format](#expected-output-format)
    - [Structure for QueryX application](#structure-for-queryx-chat-application)
  - [Contributing](#contributing)
    - [License](#license)

## Project Structure

The project contains scripts to extract database structures and format them for different purposes.

- `queryx_formatter.py`: Main script to run the extraction.

## Usage

### Extracting Database Structure

To extract the structure of your database, navigate to the [Python strcuture extraction](./) folder then run the following command:
```bash
python queryx_formatter.py <db-file> [<business-rules-file>]
```

- <db-file>: the path to the dataset file.
- <business-rules-file>: the path to the business rule text file (optional)

Follow the prompts to select your database type and enter the necessary configuration details.

## Expected Output Format

### Structure for QueryX Chat application

The structure for QueryX application will be saved within the [input data](../../data/) folder with a filename like <dbName>.json. The JSON format includes tables, constraints, dbName, dbType, and businessRules (empty list if no business_rule file argument is given). The table description, column description, column lables, and the column values example are not automatically extracted and can be added manually.

Example:
```json
{
  "dbName": "flight_2",
  "dbType": "sqlite",
  "tables": [
    {
      "constraints": [],
      "description": "",
      "table_name": "airports",
      "primary_keys": [
        "AirportCode"
      ],
      "columns": [
        {
          "name": "AirportCode",
          "type": "TEXT",
          "nullable": false,
          "labels": "",
          "description": "",
          "values": ["AAF", "ABI", "ABL", "ABQ", "ABR"]
        },
        {
          "name": "AirportName",
          "type": "TEXT",
          "nullable": false,
          "labels": "",
          "description": "",
          "values": []
        }
      ]
    },
    {
      "constraints": [
        {
          "column": "DestAirport",
          "join_column": "AirportCode",
          "join_table": "airports"
        },
        {
          "column": "SourceAirport",
          "join_column": "AirportCode",
          "join_table": "airports"
        }
      ],
      "description": "",
      "table_name": "flights",
      "primary_keys": [],
      "columns": [
        {
          "name": "SourceAirport",
          "type": "TEXT",
          "nullable": false,
          "labels": "",
          "description": "",
          "values": ["APG", "ASY", "CVO", "ACV", "AHD"]
        },
        {
          "name": "DestAirport",
          "type": "TEXT",
          "nullable": false,
          "labels": "",
          "description": "",
          "values": ["ASY", "APG", "ACV", "CVO", "AHT"]
        }
      ]
    }
  ],
  "businessRules": [],
  "dbName": "",
  "dbType": []
}
```

## Contributing
Contributions are welcome! Please feel free to [open issues](https://github.com/Tuito-dev/queryx-client-example/issues), and [disscussions](https://github.com/Tuito-dev/queryx-client-example/discussions) or give your feedbacks from [Contact us page](https://app.queryx.eu/#/contact)

## License

This project is licensed under the [MIT License](https://github.com/Tuito-dev/queryx-client-example/tree/main?tab=MIT-1-ov-file).

**Keywords**: queryx, api, python, javascript, nodejs, json, examples, backend, openapi, tuito, natural language to sql, sql queries, ai, artificial intelligence, query translation, data querying, sql generation, text2sql, speech2sql, SQL copilot, SQL coder
