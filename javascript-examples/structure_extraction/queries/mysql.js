// MYSQL and MARIADB
const QUERY_TABLES_MYSQL = (DB_NAME) => `
SELECT CONCAT('{\"table\": \"', tables.TABLE_NAME, 
'\", \"column_name\": \"', columns.COLUMN_NAME,
'\", \"column_type\": \"', columns.COLUMN_TYPE,
'\", \"description\": \"', columns.COLUMN_COMMENT,
'\", \"isPrimary\": \"', IF(columns.COLUMN_KEY = 'PRI', 'true', 'false'), '\"}') AS json_result
FROM INFORMATION_SCHEMA.TABLES AS tables
JOIN INFORMATION_SCHEMA.COLUMNS AS columns ON tables.TABLE_SCHEMA = columns.TABLE_SCHEMA AND tables.TABLE_NAME = columns.TABLE_NAME
WHERE tables.TABLE_SCHEMA = '${DB_NAME}'
AND tables.TABLE_TYPE = 'BASE TABLE'
LIMIT 10000;`
const QUERY_JOINS_MYSQL = (DB_NAME) => `
SELECT CONCAT(
  '{\"table\": \"', kcu.TABLE_NAME, 
  '\", \"column\": \"', kcu.COLUMN_NAME, 
  '\", \"join_table\": \"', kcu.REFERENCED_TABLE_NAME, 
  '\", \"join_column\": \"', kcu.REFERENCED_COLUMN_NAME, '\"}'
) AS json_result
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS kcu
JOIN INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS AS rc 
  ON kcu.CONSTRAINT_NAME = rc.CONSTRAINT_NAME 
  AND kcu.TABLE_SCHEMA = rc.CONSTRAINT_SCHEMA
WHERE kcu.TABLE_SCHEMA = '${DB_NAME}'
  AND kcu.REFERENCED_TABLE_NAME IS NOT NULL
LIMIT 10000;`
const QUERY_TABLES_NAMES_MYSQL = (DB_NAME) => `SHOW TABLES;`
const QUERY_COLUMNS_MYSQL = (DB_NAME,TABLE) => `
SELECT c.column_name FROM information_schema.tables t
JOIN information_schema.columns c ON t.table_schema = c.table_schema AND t.table_name = c.table_name
WHERE t.table_schema = '${DB_NAME}' AND t.table_name = '${TABLE}' AND t.table_type = 'BASE TABLE';`
const QUERY_VALUES_MYSQL = (DB_NAME, TABLE, COLUMN_NAME) => `SELECT DISTINCT \`${COLUMN_NAME}\` FROM \`${TABLE}\` LIMIT 5;`


module.exports = {
  QUERY_TABLES_MYSQL,
  QUERY_JOINS_MYSQL,
  QUERY_TABLES_NAMES_MYSQL,
  QUERY_COLUMNS_MYSQL,
  QUERY_VALUES_MYSQL,
};