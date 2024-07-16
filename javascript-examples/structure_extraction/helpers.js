/**
 * Fetches data from the database in chunks to handle large datasets efficiently.
 * 
 * @param {Object} db - The knex database instance.
 * @param {Function} queryFunction - The function to generate the query for fetching data.
 * @param {string} dbName - The name of the database.
 * @param {number} [chunkSize=10] - The size of each chunk of data to fetch.
 * @returns {Promise<Array>} The concatenated data fetched in chunks.
 */
async function fetchChunkedData(db, queryFunction, dbName, chunkSize = 10) {
  let data = [];
  let offset = 0;
  let chunk;

  do {
    chunk = await db.raw(queryFunction(dbName, offset, chunkSize));
    let chunkData = JSON.parse(chunk[0][Object.keys(chunk[0])[0]] || '[]');
    data = data.concat(chunkData);
    offset += chunkSize;
  } while (chunkData.length > 0);

  return data;
}

/**
 * Parses the raw JSON structure to a formatted API JSON structure.
 * 
 * @param {string} fileContent - The raw JSON file content.
 * @param {string} dbType - The type of the database (e.g., 'mysql', 'mariadb', 'mssql', 'pg', 'sqlite').
 * @param {string} dbName - The name of the database.
 * @returns {Object|null} The parsed API JSON structure or null if parsing fails.
 */
function parseUiJsonStructureToApiJson(fileContent, dbType, dbName) {
  try {
    const rawStructure = parseRawStructure(fileContent)
    const structure = {dbName, dbType, tables: [], businessRules: rawStructure.businessRules}
    if (rawStructure){
      for (const tableName of Object.keys(rawStructure.tables)) {
        let constraints = []
        let primary_keys = rawStructure.tables[tableName].columns.filter((x) => x.is_primary === "true").map((x) => x.name)
        const columns = rawStructure.tables[tableName].columns.map((x) => {
          let values = []
          if(rawStructure.values && rawStructure.values[tableName] != null && 
            rawStructure.values[tableName] !== undefined && rawStructure.values[tableName][x.name] != null && 
            rawStructure.values[tableName][x.name] !== undefined)
          {
              values = rawStructure.values[tableName][x.name].map((x) => !x ? x: x.toString())
          }
          return {
            name: x.name,
            type: x.type,
            nullable: false,
            labels: x.labels ?? '',
            description: x.description,
            values
          }
        })        
        
        if(Object.keys(rawStructure.constraints).includes(tableName)){
          constraints = rawStructure.constraints[tableName].map((c) => {return {column: c.column, join_column: c.join_column, join_table: c.join_table}})
        }
        structure.tables.push({
          constraints,
          description: rawStructure.tables[tableName].description || '',
          table_name: tableName,
          primary_keys,
          columns
        })
      }
      return structure
    }else{
      return null
    }
  } catch (error) {
    console.error(error)
    return null
  }
}

/**
 * Parses the raw JSON structure content to a structured format.
 * 
 * @param {string} fileContent - The raw JSON file content.
 * @returns {Object|null} The structured format of the raw JSON or null if parsing fails.
 */
function parseRawStructure(fileContent) {
  try {
    const parsed_content = JSON.parse(fileContent)
    if (!(parsed_content['tables'] || parsed_content['constraints'])){
      return null
    }
    let structure = {
      tables: {},
      constraints: {},
      values: {},
      businessRules: parsed_content?.businessRules || []
    }
    for (const constraint of parsed_content['constraints']) {
      if (! structure.constraints[constraint['table']]){
        structure.constraints[constraint['table']] = []
      }
      structure.constraints[constraint['table']].push({
        column: constraint['column'],
        join_table: constraint['join_table'],
        join_column: constraint['join_column'],
        condition: `${constraint['table']}.${constraint['column']}=${constraint['join_table']}.${constraint['join_column']}`
      })
    }
    if(parsed_content['values']){
      for (const valuesExample of parsed_content['values']) {
        if (! structure.values[valuesExample['table']]){
          structure.values[valuesExample['table']] = {}
        }
        structure.values[valuesExample['table']][valuesExample['column']] = valuesExample['values']
      }
    }
    for (const table of parsed_content['tables']) {
      if (! structure.tables[table['table']]){
        structure.tables[table['table']] = {description: '', columns: []}
      }
      let details = ''
      if (table['isPrimary']) {
        details+='PRIMARY KEY'
      }
      if(Object.keys(structure.constraints).includes(table['table'])) {
        const conditions = structure.constraints[table['table']].filter((x) => x.column === table['column_name']).map((x) => x.condition)
        details = [details, conditions.join(' AND ')].join(' ')
      }
      structure.tables[table['table']].columns.push({
        name: table['column_name'],
        type: table['column_type'].toLocaleUpperCase(),
        details,
        description: table['description'],
        labels: Object.keys(table).includes('labels') ? table['labels'] : '',
        values: [], // here will add values examples
        is_primary: table['isPrimary']
      })
    }

    if (Object.keys(parsed_content).includes('descriptions')){
      for (const tableDesc of parsed_content['descriptions']) {
        if(Object.keys(structure.tables).includes(tableDesc?.table)){
          structure.tables[tableDesc.table].description = tableDesc.description
        }
      }
    }
    return structure
  } catch (error) {
    console.error(error)
    return null
  }
}

module.exports = { fetchChunkedData, parseUiJsonStructureToApiJson }