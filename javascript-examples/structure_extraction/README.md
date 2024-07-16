# Structure Extraction

This project provides examples demonstrating how to extract the JSON structure of a database (SQLite, MySQL, MSSQL, PostgreSQL, and MariaDB) using Node.js. The extracted structure can be formatted to be used with the QueryX application on one hand or with the APIs on the other hand, the structure slightly differs for both cases.

## Table of Contents

- [Structure Extraction](#structure-extraction)
  - [Table of Contents](#table-of-contents)
  - [Project Structure](#project-structure)
  - [Usage](#usage)
    - [Extracting Database Structure](#extracting-database-structure)
  - [Expected Output Format](#expected-output-format)
    - [Structure for QueryX application](#structure-for-queryx-chat-application)
    - [Structure for API](#structure-for-api)
  - [Contributing](#contributing)
    - [License](#license)

## Project Structure

The project contains scripts to extract database structures and format them for different purposes.

- `index.js`: Main script to run the extraction.
- `dbConfig.js`: Handles database configuration prompts and knex configuration.
- `helpers.js`: Contains helper functions for fetching data and parsing structures.
- `queries/`: Contains query files for different databases.

## Usage

### Extracting Database Structure

To extract the structure of your database, navigate to the [JS strcuture extraction](./) folder then run the following command:
```bash
npm start
```

Follow the prompts to select your database type and enter the necessary configuration details.

## Expected Output Format

### Structure for QueryX Chat application

The structure for QueryX application will be saved in the outputs folder with a filename like structure_<dbType>_<dbName>.json. The JSON format includes tables, constraints, and values.

Example:
```javascript
{
  "tables": [
    {
      "table": "airports",
      "column_name": "AirportCode",
      "column_type": "TEXT",
      "description": "",
      "isPrimary": "true"
    },
    {
      "table": "airports",
      "column_name": "AirportName",
      "column_type": "TEXT",
      "description": "",
      "isPrimary": "false"
    },
    {
      "table": "flights",
      "column_name": "SourceAirport",
      "column_type": "TEXT",
      "description": "",
      "isPrimary": "false"
    },
    {
      "table": "flights",
      "column_name": "DestAirport",
      "column_type": "TEXT",
      "description": "",
      "isPrimary": "false"
    }
  ],
  "constraints": [
    {
      "table": "flights",
      "column": "DestAirport",
      "join_table": "airports",
      "join_column": "AirportCode"
    },
    {
      "table": "flights",
      "column": "SourceAirport",
      "join_table": "airports",
      "join_column": "AirportCode"
    }
  ],
  "values": [
    {
      "table": "airports",
      "column": "AirportCode",
      "values": ["AAF", "ABI", "ABL", "ABQ", "ABR"]
    },
    {
      "table": "flights",
      "column": "SourceAirport",
      "values": ["APG", "ASY", "CVO", "ACV", "AHD"]
    },
    {
      "table": "flights",
      "column": "DestAirport",
      "values": ["ASY", "APG", "ACV", "CVO", "AHT"]
    }
  ]
}
```
### Structure for API

The structure for API input will be saved in the outputs folder with a filename like api_input_structure_<dbType>_<dbName>.json. The JSON format is tailored for API input.

Example:
```javascript
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
  "businessRules": []
}
```

## Contributing
Contributions are welcome! Please feel free to [open issues](https://github.com/Tuito-dev/queryx-client-example/issues), and [disscussions](https://github.com/Tuito-dev/queryx-client-example/discussions) or give your feedbacks from [Contact us page](https://app.queryx.eu/#/contact)

### License

This project is licensed under the [MIT License](https://github.com/Tuito-dev/queryx-client-example/tree/main?tab=MIT-1-ov-file).

**Keywords**: queryx, api, python, javascript, nodejs, json, examples, backend, openapi, tuito, natural language to sql, sql queries, ai, artificial intelligence, query translation, data querying, sql generation, text2sql, speech2sql, SQL copilot, SQL coder
