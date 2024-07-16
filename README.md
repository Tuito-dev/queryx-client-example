# Queryx-client-example

This project offers client examples in both [JavaScript](./javascript-examples/) and [Python](./python-examples/) to utilize the Text-to-SQL QueryX BE [API](https://app.queryx.eu/#/api-docs) solution developed by [Tuito](https://tuito.fr/query-x/).

For more details about the QueryX project, please visit the [project page](https://tuito.fr/query-x/) and the <a href="https://www.youtube.com/watch?v=K7IU2qlmKPo" target="_blank"> 
    <img src="https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg" alt="YouTube video" style="width:30px;height:30px;">
</a> video.

## Try it on Google Colab (for Python)

- [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1YCuDL65cJJra991NlftCxspdeNI8QQ6n?usp=sharing)

## Try it on CodePen (for JavaScript)

- [![Try it on CodePen for JavaScript](https://img.shields.io/badge/Try%20it%20on-CodePen-orange)](https://codepen.io/Tuito-Intuito/pen/yLWmwLB)

## Table of Contents

- [Queryx-client-example](#queryx-client-example)
  - [Try it on Google Colab](#try-it-on-google-colab-for-python)
  - [Try it on CodePen](#try-it-on-codepen-for-javascript)
  - [Table of Contents](#table-of-contents)
  - [Project Structure](#project-structure)
    - [Database folder](#database-folder)
    - [python-examples](#python-examples)
    - [javascript-examples](#javascript-examples)
    - [structure-extraction](#structure-extraction)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Example datasets](#example-datasets)
    - [Business Rules (Semantic Layer)](#business-rules-semantic-layer)
    - [Use your own database](#use-your-own-database)
  - [Usage](#usage)
  - [API Documentation](#api-documentation)
  - [Contributing](#contributing)
  - [License](#license)

## Project Structure

The project organization is as follows:

```
.
├── data
│   ├── formula_1
│   └── student_club
├── javascript-examples
│   └── structure_extraction
│       └── queries
└── python-examples
    └── structure_extraction

8 directories
```

### [Database folder](./data/)

This folder should contain the database to be queried. Each folder represents a database.

### [python-examples](./python-examples/)

Examples of how to interact with the QueryX API using Python. For more details, visit [python examples](#python-examples).

### [javascript-examples](./javascript-examples/)

Examples of how to interact with the QueryX API using JavaScript. For more details, visit [JavaScript examples](#javascript-examples).

### [structure-extraction](#structure-extraction)

You can find the necessary scripts for generating the database schema in JSON format from your database in both [Python](./python-examples/structure_extraction/) and [JavaScript](./javascript-examples/structure_extraction/)

## Getting Started

To begin with this project, ensure that the necessary [prerequisites](#prerequisites) are installed on your system.

### Prerequisites

1. **Python** (only for Python usage)

    - **Linux**:
  
    ```
      sudo apt update
      sudo apt install python3 python3-pip
    ```

    - **Windows**:
      
      - Download the Python installer from the [official Python website](https://www.python.org/downloads/windows/).
      - Run the installer and follow the instructions.

2. **Node.js** (only for Java Script usage)

    - **Linux**

    ```
    sudo apt update
    sudo apt install nodejs npm
    ```

    - **Windows**

      - Download the Node.js installer from the [official Node.js website](https://nodejs.org/en/download/package-manager).
      - Run the installer and follow the instructions.

3. **API key for the QueryX backend**

    If you don't have a QueryX account, please [create a new one](https://app.queryx.eu/#/login).

    Your API Key is under [My API key section of the Profile page](https://app.queryx.eu/#/profil#ppage-api-key).

### Example datasets

The project includes two sample database structures in JSON format:

- [Formula 1 database](./data/formula_1/formula_1.json): Defines the structure of the "Formula 1" database.
- [Student club database](./data/student_club/student_club.json): Defines the structure of the "Student Club" database.

These files are stored within a dedicated [data](./data/) folder.

### Business Rules (Semantic Layer)

The project also includes **optional** separate text files (*.txt) that define business rules specific to each database:

- [Formula 1 database](./data/formula_1/formula_1-best_business_rules.txt): Business rules for the "Formula 1" database.
- [Student Club database](./data/student_club/student_club-best_business_rules.txt): Business rules for the "Student Club" database.

These business rules act as a guide for understanding the data and making decisions based on it. They are entirely optional and can be tailored to your specific needs.

**Example Business Rule**

Imagine the [Formula 1 database](./data/formula_1/formula_1.json) file contains data about Formula 1 races, including driver information. An example business rule might state:

'A driver is considered "experienced" if they have participated in more than 50 Formula 1 races.'

This rule adds a layer of meaning to the raw data, allowing you to easily identify experienced drivers based on the number of races they've been in. You can define similar rules for other data points in your databases to make them more insightful and actionable.

### Use your own database

To use your own database, please follow the following steps:

1. **Database Type**: Make sure that the database type is supported by the tool (supported database types are: ***'SqLite'***, ***'MySQL'***, or ***'PostGres'***).

2. **Upload your database**: Create a new folder within the [data](./data/) folder and put your database inside it.

3. **Business Rules definition (optional)**: If you want to define your own [Business Rules](#business-rules-semantic-layer), you have to create a text file in the database folder and specify them by line (each line is a Business Rule). An example can be found [here](./data/formula_1/formula_1-best_business_rules.txt).

4. **Structure Generation**: Generate the database structure in a JSON format. Follow either the [Node.js structure generation README](./javascript-examples/structure_extraction/) or the [Python structure generation README](./python-examples/structure_extraction/).

5. **Run**:

Follow the README instructions inside the example directories ([Python](./python-examples/README.md) or [JavaScript](./javascript-examples/README.md))

## Usage

1. Clone the repository:
    ```bash
    git clone https://github.com/Tuito-dev/queryx-client-example.git
    cd queryx-client-example
    ```

2. Navigate to the desired example subfolder ([Python](./python-examples/README.md) or [JavaScript](./javascript-examples/README.md)):
    ```bash
    cd python-examples # For Python
    # or
    cd javascript-examples # For JavaScript
    ```

3. Follow the specific instructions in the subfolder's README.

## API Documentation

For detailed API documentation, refer to the [Api Documentation page](https://app.queryx.eu/#/api-docs)

## Contributing

Contributions are welcome! Please feel free to [open issues](https://github.com/Tuito-dev/queryx-client-example/issues), and [disscussions](https://github.com/Tuito-dev/queryx-client-example/discussions) or give your feedbacks from [Contact us page](https://app.queryx.eu/#/contact)

## License

This project is licensed under the [MIT License](https://github.com/Tuito-dev/queryx-client-example/tree/main?tab=MIT-1-ov-file).

**Keywords**: queryx, api, python, javascript, nodejs, json, examples, backend, openapi, tuito, natural language to sql, sql queries, ai, artificial intelligence, query translation, data querying, sql generation, text2sql, speech2sql, SQL copilot, SQL coder
