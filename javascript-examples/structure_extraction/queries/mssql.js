const QUERY_TABLES_MSSQL = (DB_NAME, offset, chunkSize) => `\
SET NOCOUNT ON; \
WITH PrimaryKeys AS ( \
    SELECT \
        KU.COLUMN_NAME, \
        KU.TABLE_NAME \
    FROM \
        INFORMATION_SCHEMA.TABLE_CONSTRAINTS TC \
        JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE KU \
        ON TC.CONSTRAINT_NAME = KU.CONSTRAINT_NAME \
    WHERE \
        TC.CONSTRAINT_TYPE = 'PRIMARY KEY' \
) \
SELECT  \
    C.TABLE_NAME AS [table], \
    C.COLUMN_NAME AS [column_name], \
    C.DATA_TYPE AS [column_type], \
    ISNULL(C.COLUMN_DEFAULT, '') AS [description], \
    CASE WHEN PK.COLUMN_NAME IS NOT NULL THEN 'true' ELSE 'false' END AS [isPrimary] \
FROM INFORMATION_SCHEMA.COLUMNS C \
LEFT JOIN PrimaryKeys PK \
ON C.TABLE_NAME = PK.TABLE_NAME AND C.COLUMN_NAME = PK.COLUMN_NAME \
WHERE C.TABLE_CATALOG = '${DB_NAME}' \
ORDER BY C.TABLE_NAME, C.COLUMN_NAME \
OFFSET ${offset} ROWS FETCH NEXT ${chunkSize} ROWS ONLY \
FOR JSON PATH;`

const QUERY_JOINS_MSSQL = (DB_NAME, offset, chunkSize) => `
USE ${DB_NAME};
IF OBJECT_ID('tempdb..#ForeignKeysTMPTABLE') IS NOT NULL
      DROP TABLE #ForeignKeysTMPTABLE;
SELECT 
fk.name AS ConstraintName,
OBJECT_NAME(fk.parent_object_id) AS TableName,
COL_NAME(fkc.parent_object_id, fkc.parent_column_id) AS ColumnName,
OBJECT_NAME(fk.referenced_object_id) AS ReferencedTableName,
COL_NAME(fkc.referenced_object_id, fkc.referenced_column_id) AS ReferencedColumnName
INTO #ForeignKeysTMPTABLE
FROM 
sys.foreign_keys AS fk
INNER JOIN sys.foreign_key_columns AS fkc ON fk.object_id = fkc.constraint_object_id;

SELECT 
TableName AS [table],
ColumnName AS [column],
ReferencedColumnName AS join_column,
ReferencedTableName AS join_table
FROM 
#ForeignKeysTMPTABLE
ORDER BY TableName, ColumnName
OFFSET ${offset} ROWS FETCH NEXT ${chunkSize} ROWS ONLY
FOR JSON PATH;

DROP TABLE #ForeignKeysTMPTABLE;
`

const QUERY_TABLES_NAMES_MSSQL = (DB_NAME) => `USE ${DB_NAME}; SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';`
const QUERY_COLUMNS_MSSQL = (DB_NAME, TABLE) => `SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_CATALOG = '${DB_NAME}' AND TABLE_NAME = '${TABLE}';`
const QUERY_VALUES_MSSQL = (DB_NAME, TABLE, COLUMN_NAME) => `USE ${DB_NAME}; SELECT DISTINCT TOP 5 ${COLUMN_NAME} FROM ${TABLE};`


module.exports = {
  QUERY_TABLES_MSSQL,
  QUERY_JOINS_MSSQL,
  QUERY_TABLES_NAMES_MSSQL,
  QUERY_COLUMNS_MSSQL,
  QUERY_VALUES_MSSQL,
};
