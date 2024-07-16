const QUERY_TABLES_SQLITE = `SELECT '{\"table\": \"' || m.name || '\", \"column_name\": \"' || p.name || '\", \"column_type\": \"' || p.type || '\", \"description\": \"\", \"isPrimary\": \"' || (CASE WHEN pk = 1 THEN 'true' ELSE 'false' END) || '\"}' AS json_result FROM sqlite_master AS m, pragma_table_info(m.name) AS p WHERE m.type = 'table' LIMIT 10000;`
const QUERY_JOINS_SQLITE = (TABLE) => `SELECT '{\"table\": \"${TABLE}\", \"column\": \"' || k.\"from\" || '\", \"join_table\": \"' || k.\"table\" || '\", \"join_column\": \"' || k.\"to\" || '\"}' AS json_result FROM pragma_foreign_key_list('${TABLE}') AS k LIMIT 10000;`
const QUERY_TABLES_NAMES_SQLITE = `SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';`
const QUERY_COLUMNS_SQLITE = (TABLE) => `PRAGMA table_info('${TABLE}');`
const QUERY_VALUES_SQLITE = (TABLE, COLUMN_NAME) => `SELECT DISTINCT \"${COLUMN_NAME}\" FROM \"${TABLE}\" LIMIT 5;`

module.exports = {
  QUERY_TABLES_SQLITE,
  QUERY_JOINS_SQLITE,
  QUERY_TABLES_NAMES_SQLITE,
  QUERY_COLUMNS_SQLITE,
  QUERY_VALUES_SQLITE,
};