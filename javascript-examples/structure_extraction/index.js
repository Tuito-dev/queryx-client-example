// Import required modules

const inquirer = require('inquirer');
const knex = require('knex');
const fs = require('fs');
const { getDbConfig, createKnexConfig } = require('./dbConfig');
const { fetchChunkedData, parseUiJsonStructureToApiJson } = require('./helpers')
const {
  QUERY_TABLES_MSSQL, QUERY_JOINS_MSSQL, QUERY_TABLES_NAMES_MSSQL, QUERY_COLUMNS_MSSQL, QUERY_VALUES_MSSQL
} = require('./queries/mssql');
const {
  QUERY_TABLES_PG, QUERY_JOINS_PG, QUERY_TABLES_NAMES_PG, QUERY_COLUMNS_PG, QUERY_VALUES_PG
} = require('./queries/pg');
const {
  QUERY_TABLES_MYSQL, QUERY_JOINS_MYSQL, QUERY_TABLES_NAMES_MYSQL, QUERY_COLUMNS_MYSQL, QUERY_VALUES_MYSQL
} = require('./queries/mysql');
const {
  QUERY_TABLES_SQLITE, QUERY_JOINS_SQLITE, QUERY_TABLES_NAMES_SQLITE, QUERY_COLUMNS_SQLITE, QUERY_VALUES_SQLITE
} = require('./queries/sqlite');

const OUTPUT_FOLDER = '../../data'

// Main function to run the script
async function main() {
  // Database types available
  const dbTypes = ['mysql', 'mssql', 'sqlite', 'mariadb', 'pg'];
  // Prompt user to select the database type
  const { dbType } = await inquirer.prompt([
    {
      type: 'list',
      name: 'dbType',
      message: 'Select the type of database to connect to:',
      choices: dbTypes,
    }
  ]);
  // Get the database configuration and create knex configuration
  const dbConfig = await getDbConfig(dbType);
  const knexConfig = createKnexConfig(dbType, dbConfig);
  const db = knex(knexConfig);
  // Prompt user for data extraction permission
  const { extract } = await inquirer.prompt([
    {
      type: 'confirm',
      name: 'extract',
      message: 'Can we extract a few examples of your database to improve the accuracy?',
      default: true
    }
  ]);

  console.info(`Connected to ${dbType} database name ${dbConfig.database}`);
  // Define output file names
  const outputNameUi = `structure_${dbType}_${dbConfig.database}.json`;
  const outputNameAPI = `${dbConfig.database}.json`;
  let tables = [];
  let constraints = [];
  let values = [];

  switch (dbType) {
    case 'mysql':
    case 'mariadb':
      // Fetch tables and constraints for MySQL and MariaDB
      tables = (await db.raw(QUERY_TABLES_MYSQL(dbConfig.database)))[0].map(x => JSON.parse(x.json_result));
      constraints = (await db.raw(QUERY_JOINS_MYSQL(dbConfig.database)))[0].map(x => JSON.parse(x.json_result));
      
      if (extract) {
        // Fetch tables names and columns for extraction
        const tablesNames = (await db.raw(QUERY_TABLES_NAMES_MYSQL(dbConfig.database)))[0].map(x => x[Object.keys(x)[0]]);
        for (const tn of tablesNames) {
          const columns = (await db.raw(QUERY_COLUMNS_MYSQL(dbConfig.database, tn)))[0].map(x => x.column_name);
          for (const col of columns) {
            values.push({
              table: tn,
              column: col,
              values: (await db.raw(QUERY_VALUES_MYSQL(dbConfig.database, tn, col)))[0].map(x => x[col])
            });
          }
        }
      }
      break;
    case 'mssql':
      // Fetch tables and constraints for MSSQL
      tables = await fetchChunkedData(db, QUERY_TABLES_MSSQL, dbConfig.database);
      constraints = await fetchChunkedData(db, QUERY_JOINS_MSSQL, dbConfig.database);

      if (extract) {
        // Fetch tables names and columns for extraction
        const tablesNames = (await db.raw(QUERY_TABLES_NAMES_MSSQL(dbConfig.database))).map(x => x.TABLE_NAME);
        for (const tn of tablesNames) {
          const columns = (await db.raw(QUERY_COLUMNS_MSSQL(dbConfig.database, tn))).map(x => x.COLUMN_NAME);
          for (const col of columns) {
            values.push({
              table: tn,
              column: col,
              values: (await db.raw(QUERY_VALUES_MSSQL(dbConfig.database, tn, col))).map(x => x[col])
            });
          }
        }
      }
      break;
    case 'pg':
      // Fetch tables and constraints for PostgreSQL
      tables = await fetchChunkedData(db, QUERY_TABLES_PG, dbConfig.database);
      constraints = await fetchChunkedData(db, QUERY_JOINS_PG, dbConfig.database);

      if (extract) {
        // Fetch tables names and columns for extraction
        const tablesNames = (await db.raw(QUERY_TABLES_NAMES_PG(dbConfig.database))).rows.map(x => x.table_name);
        for (const tn of tablesNames) {
          const columns = (await db.raw(QUERY_COLUMNS_PG(dbConfig.database, tn))).rows.map(x => x.column_name);
          for (const col of columns) {
            values.push({
              table: tn,
              column: col,
              values: (await db.raw(QUERY_VALUES_PG(dbConfig.database, tn, col))).rows.map(x => x[col])
            });
          }
        }
      }
      break;
    case 'sqlite':
      // Fetch tables and constraints for SQLite
      tables = (await db.raw(QUERY_TABLES_SQLITE)).map(x => JSON.parse(x.json_result));
      const tablesNames = (await db.raw(QUERY_TABLES_NAMES_SQLITE)).map(x => x.name);

      for (const tn of tablesNames) {
        const c = (await db.raw(QUERY_JOINS_SQLITE(tn))).map(x => JSON.parse(x.json_result));
        constraints.push(...c);

        if (extract) {
          // Fetch columns and values for extraction
          const columns = (await db.raw(QUERY_COLUMNS_SQLITE(tn))).map(x => x.name);
          for (const col of columns) {
            values.push({
              table: tn,
              column: col,
              values: (await db.raw(QUERY_VALUES_SQLITE(tn, col))).map(x => x[col])
            });
          }
        }
      }
      break;
    default:
      break;
  }

  // Create output folder if it doesn't exist
  if(!fs.existsSync(OUTPUT_FOLDER)){
    fs.mkdirSync(OUTPUT_FOLDER)
  }

  // Create output folder if it doesn't exist
  if(!fs.existsSync(`${OUTPUT_FOLDER}/${dbConfig.database}`)){
    fs.mkdirSync(`${OUTPUT_FOLDER}/${dbConfig.database}`)
  }

  // Create JSON input for UI and API
  const uiJsonInput = JSON.stringify({ tables, constraints, values }, null, 2)

  const fileconi = fs.readFileSync('outputs/structure_sqlite_flight_22.json')
  const apiJsonInput = JSON.stringify(parseUiJsonStructureToApiJson(fileconi, dbType, dbConfig.database), null, 2)
  // const apiJsonInput = JSON.stringify(parseUiJsonStructureToApiJson(uiJsonInput, dbType, dbConfig.database), null, 2)

  // Write JSON input to files
  fs.writeFileSync(`${OUTPUT_FOLDER}/${dbConfig.database}/${outputNameUi}`, uiJsonInput);
  fs.writeFileSync(`${OUTPUT_FOLDER}/${dbConfig.database}/${outputNameAPI}`, apiJsonInput);
  console.log(`structure for QueryX Chat application input saved to ${OUTPUT_FOLDER}/${dbConfig.database}/${outputNameUi}`);
  console.log(`structure for API input saved to ${OUTPUT_FOLDER}/${dbConfig.database}/${outputNameAPI}`);
  await db.destroy();
  console.log('Process completed.');
}

// Catch any errors and log them
main().catch(error => {
  console.error('An error occurred:', error);
});
