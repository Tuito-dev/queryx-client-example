const QUERY_TABLES_PG = (DB_NAME, offset, chunkSize) => `
SELECT
    c.table_name as table,
    c.column_name,
    c.data_type AS column_type,
    COALESCE(col_description(format('%s.%s', c.table_schema, c.table_name)::regclass::oid, c.ordinal_position), '') AS description,
    CASE 
        WHEN tc.constraint_type = 'PRIMARY KEY' THEN 'true'
        ELSE 'false'
    END AS isPrimary
FROM 
    information_schema.columns c
LEFT JOIN 
    information_schema.key_column_usage kcu
    ON 
        c.table_schema = kcu.table_schema
        AND c.table_name = kcu.table_name
        AND c.column_name = kcu.column_name
LEFT JOIN 
    information_schema.table_constraints tc
    ON 
        kcu.constraint_name = tc.constraint_name
        AND kcu.table_schema = tc.table_schema
        AND kcu.table_name = tc.table_name
WHERE 
    c.table_schema = 'public' -- specify schema if needed
ORDER BY 
    c.table_name, c.ordinal_position
LIMIT ${chunkSize}
OFFSET ${offset};`

const QUERY_JOINS_PG = (DB_NAME, offset, chunkSize) => `
SELECT
    tc.table_name AS table,
    kcu.column_name AS column,
    ccu.table_name AS join_table,
    ccu.column_name AS join_column
FROM 
    information_schema.table_constraints AS tc
JOIN 
    information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema = kcu.table_schema
JOIN 
    information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
    AND ccu.table_schema = tc.table_schema
WHERE 
    tc.constraint_type = 'FOREIGN KEY'
ORDER BY 
    tc.table_name, kcu.column_name
LIMIT ${chunkSize}
OFFSET ${offset};;
`

const QUERY_TABLES_NAMES_PG = (DB_NAME) => `
SELECT
    table_name
FROM
    information_schema.tables
WHERE
    table_schema = 'public'
    AND table_type = 'BASE TABLE'
ORDER BY
    table_name;`

const QUERY_COLUMNS_PG = (DB_NAME, TABLE) => `
SELECT
    column_name
FROM
    information_schema.columns
WHERE
    table_schema = 'public'
    AND table_name = '${TABLE}'
ORDER BY
    ordinal_position;`

const QUERY_VALUES_PG = (DB_NAME, TABLE, COLUMN_NAME) => `
SELECT DISTINCT ${COLUMN_NAME}
FROM ${TABLE}
LIMIT 5;`

module.exports = {
  QUERY_TABLES_PG,
  QUERY_JOINS_PG,
  QUERY_TABLES_NAMES_PG,
  QUERY_COLUMNS_PG,
  QUERY_VALUES_PG,
};