const inquirer = require('inquirer');

const defaultPorts = {
  mysql: 3306,
  mariadb: 3306,
  mssql: 1433,
  pg: 5432
};

/**
 * Prompts the user for database configuration details based on the selected database type.
 * 
 * @param {string} dbType - The type of the database (e.g., 'mysql', 'mariadb', 'mssql', 'pg', 'sqlite').
 * @returns {Promise<Object>} The database configuration object containing user input.
 */
async function getDbConfig(dbType) {
  const dbConfigQuestions = [
    {
      type: 'input',
      name: 'host',
      message: 'Enter the database host:',
      when: () => dbType !== 'sqlite',
      default: 'localhost'
    },
    {
      type: 'input',
      name: 'port',
      message: 'Enter the database port:',
      when: () => dbType !== 'sqlite',
      default: defaultPorts[dbType] ? defaultPorts[dbType] : null
    },
    {
      type: 'input',
      name: 'user',
      message: 'Enter the database user:',
      when: () => dbType !== 'sqlite',
    },
    {
      type: 'password',
      name: 'password',
      message: 'Enter the database password:',
      when: () => dbType !== 'sqlite',
    },
    {
      type: 'input',
      name: 'database',
      message: 'Enter the database name:',
    },
    {
      type: 'input',
      name: 'filename',
      message: 'Enter the sqlite filename:',
      when: () => dbType === 'sqlite'
    }
  ];

  return await inquirer.prompt(dbConfigQuestions);
}
/**
 * Creates a knex configuration object based on the database type and configuration details.
 * 
 * @param {string} dbType - The type of the database (e.g., 'mysql', 'mssql', 'pg', 'sqlite').
 * @param {Object} dbConfig - The database configuration details provided by the user.
 * @returns {Object} The knex configuration object.
 */
function createKnexConfig(dbType, dbConfig) {
  let knexConfig = {};

  switch (dbType) {
    case 'mysql':
    case 'mariadb':
      knexConfig = {
        client: dbType,
        connection: {
          host: dbConfig.host,
          port: Number(dbConfig.port),
          user: dbConfig.user,
          password: dbConfig.password,
          database: dbConfig.database
        }
      };
      break;
    case 'mssql':
      knexConfig = {
        client: 'mssql',
        connection: {
          server: dbConfig.host,
          port: Number(dbConfig.port),
          user: dbConfig.user,
          password: dbConfig.password,
          database: dbConfig.database,
          options: {
            enableArithAbort: true
          }
        }
      };
      break;
    case 'pg':
      knexConfig = {
        client: 'pg',
        connection: {
          host: dbConfig.host,
          port: Number(dbConfig.port),
          user: dbConfig.user,
          password: dbConfig.password,
          database: dbConfig.database
        },
        migrations: {
          tableName: 'knex_migrations',
          directory: './migrations'
        },
        seeds: {
          directory: './seeds'
        }
      };
      break;
    case 'sqlite':
      knexConfig = {
        client: 'sqlite3',
        connection: {
          filename: dbConfig.filename
        },
        useNullAsDefault: true
      };
      break;
  }

  return knexConfig;
}

module.exports = { getDbConfig, createKnexConfig, defaultPorts };
