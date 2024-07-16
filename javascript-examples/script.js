// Constants: Base API URL

const API_URL = 'https://api-qa-queryX.prod.tuito.fr/be'

// html elements: 

const pages = document.querySelectorAll('.page');
const drawerButtons = document.querySelectorAll('.drawer-btn');
const authorizationDom = document.getElementById('authorization')
const apiKeyInput = document.getElementById('apiKeyInput')
const errorApiKey = document.getElementById('errorApiKey')

// Generate Query
const getDbListBtn = document.getElementById('getDbListBtn')
const getDbListResult = document.getElementById('getDbListResult')
const getDbStructureBtn = document.getElementById('getDbStructureBtn')
const getDbStructureResult = document.getElementById('getDbStructureResult')

// Set Database
const setDatabaseBtn = document.getElementById('setDatabaseBtn')
const structureJsonInput = document.querySelector('#structureJsonInput')
const structureErrorText = document.getElementById('structureErrorText')
const dbUuidResult = document.getElementById('dbUuidResult')
const DatabaseUuid = document.getElementById('DatabaseUuid')
const dbUuid = document.getElementById('dbUuid')
const errorDbUuid = document.getElementById('errorDbUuid')

// Generate Query
const questionInput = document.getElementById('questionInput')
const queryErrorText = document.getElementById('queryErrorText')
const getQueryBtn = document.getElementById('getQueryBtn')
const queryResult = document.getElementById('queryResult')
const getQueryBtnValidate = document.getElementById('getQueryBtnValidate')
const getQueryBtnReject = document.getElementById('getQueryBtnReject')

// Suggested questions
const suggestedquestionInput = document.getElementById('suggestedquestionInput')
const suggestedErrorText = document.getElementById('suggestedErrorText')
const suggestedBtn = document.getElementById('suggestedBtn')
const suggestedResult = document.getElementById('suggestedResult')

// Fix query
const fixQueryInputQuestion = document.getElementById('fixQueryInputQuestion')
const fixQueryInputQuery = document.getElementById('fixQueryInputQuery')
const fixQueryInputError = document.getElementById('fixQueryInputError')
const fixQueryErrorText = document.getElementById('fixQueryErrorText')
const fixQueryBtn = document.getElementById('fixQueryBtn')
const fixQueryResult = document.getElementById('fixQueryResult')

// Generate query with context
const QueryContextInputQuestion = document.getElementById('QueryContextInputQuestion')
const QueryContextInputHistory = document.getElementById('QueryContextInputHistory')
const QueryContextErrorText = document.getElementById('QueryContextErrorText')
const QueryContextBtn = document.getElementById('QueryContextBtn')
const QueryContextResult = document.getElementById('QueryContextResult')

// Handle database
const handleDBBtnCache = document.getElementById('handleDBBtnCache')
const handleDBBtnDelete = document.getElementById('handleDBBtnDelete')
const handleDBResult = document.getElementById('handleDBResult')


// Function to toggle page visibility based on the selected page
function showPage(pageId) {
  // If the selected page ID is 'page1', hide the element with ID 'DatabaseUuid'
  if(pageId === 'page-home') {
    DatabaseUuid.style.display = 'none';
    authorizationDom.style.display = 'none';
  } else if(pageId === 'page1') {
    DatabaseUuid.style.display = 'none';
    authorizationDom.style.display = '';
  } else {
    // Otherwise, make the 'DatabaseUuid' element visible
    DatabaseUuid.style.display = '';
    authorizationDom.style.display = '';
  }
  
  // Hide all pages
  pages.forEach(page => {
      page.style.display = 'none';
  });
  
  // Show the selected page
  const selectedPage = document.getElementById(pageId);
  if (selectedPage) {
      selectedPage.style.display = 'block';
  }
}

// Function to set dbUuid every where
function setDbUuid(pageId) {
  // Hide all pages
  pages.forEach(page => {
      page.style.display = 'none';
  });
  // Show the selected page
  const selectedPage = document.getElementById(pageId);
  if (selectedPage) {
      selectedPage.style.display = 'block';
  }
}

// Event listener for drawer buttons
drawerButtons.forEach(btn => {
  // Add a click event listener to each drawer button
  btn.addEventListener('click', function() {
      // Get the page ID from the data-page attribute of the clicked button
      const pageId = btn.getAttribute('data-page');
      // Call the showPage function with the retrieved page ID
      showPage(pageId);
  });
});

// Set Long placeholders
structureJsonInput.setAttribute('placeholder', `Json format must be :\n \
{\n \
  "dbType": string, // the type of the databse, one of: mysql, mssql, sqlite, pg, mariadb\n \
  "dbName": string, // the desired name of the database\n \
  "tables": [\n \
    {\n \
      "table": "string", // The name of the table\n \
      "columns": [\n \
        {\n \
          "name": "string", // The name of the column\n \
          "type": "string", // The type of the column\n \
          "nullable": "boolean", // Whether the column can be null\n \
          "labels": "string", // Comma-separated labels of the columns\n \
          "description": "string", // Brief description of the column\n \
          "constraints": [\n \
            {\n \
              "column": "string", // The name of the column\n \
              "join_column": "string", // The name of the join column\n \
              "join_table": "string" // The name of the join table\n \
            }\n \
          ],\n \
          "values": ["string"] // List of distinct example values for the column\n \
        }\n \
      ],\n \
      "primary_keys": ["string"], // List of primary key columns\n \
      "description": "string" // Brief description of the table\n \
    }\n \
  ],\n \
  "constraints": [\n \
    {\n \
      "table": "string", // The name of the table\n \
      "column": "string", // The name of the column\n \
      "join_column": "string", // The name of the join column\n \
      "join_table": "string" // The name of the join table\n \
    }\n \
  ],\n \
  "businessRules": [\n \
    "string" // Description of the business rule\n \
  ]\n \
}
`)

QueryContextInputHistory.setAttribute('placeholder', 'context History\nExample:\n \
[\n \
  {\n \
    "query": "SELECT * FROM users;",\n \
    "question": "give all users"\n \
  },\n \
  {\n \
    "query": "SELECT COUNT(*) FROM member WHERE position = \'Admin\';",\n \
    "question": "how many of them are admins?"\n \
  }\n \
]\n \
')

// Initially show the first page (optional)
showPage('page-home');

// Page 0: Get Databases Infos
getDbListBtn.addEventListener('click', async () => {
  const apiKey = apiKeyInput.value.trim();

  // Clear any previous error messages and show processing message
  errorApiKey.textContent = null;
  getDbListResult.textContent = 'Processing...';

  // Check if API key is provided
  if ((!apiKey) || apiKey === '') {
    errorApiKey.textContent = 'Please fill The API Key';
    return;
  }

  try {
    // Make a GET request to fetch the database list
    const response = await fetch(`${API_URL}/get-db-list`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `${apiKey}`
      }
    });
    const data = await response.json();

    // Display the result based on the response status
    if (response.status === 200) {
      getDbListResult.textContent = JSON.stringify(data, null, 4);
    } else if (response.status === 401) {
      getDbListResult.textContent = `Error: API Key - ${data.status}`;
    } else {
      console.debug(response, data);
      getDbListResult.textContent = `Error: ${data.status}`;
    }
  } catch (error) {
    // Handle any errors that occurred during the fetch request
    console.error('Error:', error);
    getDbListResult.textContent = `An error occurred. ${error}`;
  }
});

getDbStructureBtn.addEventListener('click', async () => {
  const apiKey = apiKeyInput.value.trim();

  // Clear any previous error messages and show processing message
  errorApiKey.textContent = null;
  getDbStructureResult.textContent = 'Processing...';

  // Check if API key is provided
  if ((!apiKey) || apiKey === '') {
    errorApiKey.textContent = 'Please fill The API Key';
    return;
  }

  // Check if Database UUID is provided
  if (!dbUuid.value.trim()) {
    getDbStructureResult.textContent = 'Please fill The Database Uuid';
    return;
  }

  try {
    // Make a GET request to fetch the database structure
    const response = await fetch(`${API_URL}/get-db-structure/${dbUuid.value.trim()}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `${apiKey}`
      }
    });
    const data = await response.json();

    // Display the result based on the response status
    if (response.status === 200) {
      getDbStructureResult.textContent = JSON.stringify(data, null, 4);
    } else if (response.status === 401) {
      getDbStructureResult.textContent = `Error: API Key - ${data.status}`;
    } else {
      console.debug(response, data);
      getDbStructureResult.textContent = `Error: ${data.status}`;
    }
  } catch (error) {
    // Handle any errors that occurred during the fetch request
    console.error('Error:', error);
    getDbStructureResult.textContent = `An error occurred. ${error}`;
  }
});


// Page 1: Set Database
setDatabaseBtn.addEventListener('click', async () => {
  const apiKey = apiKeyInput.value.trim();
  const jsonInput = structureJsonInput.value.trim();

  // Clear any previous error messages and show processing message
  errorApiKey.textContent = null;
  structureErrorText.textContent = null;
  dbUuidResult.textContent = 'Processing...';

  // Check if API key is provided
  if ((!apiKey) || apiKey === '') {
    errorApiKey.textContent = 'Please fill The API Key';
    return;
  }

  try {
    // Make a POST request to set the database
    const response = await fetch(`${API_URL}/set-db`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `${apiKey}`
      },
      body: jsonInput
    });
    const data = await response.json();
    dbUuidResult.textContent = null;

    // Display the result based on the response status
    if (response.status === 200) {
      dbUuid.value = data.dbUuid;
      dbUuidResult.textContent = `dbUuid: ${data.dbUuid}`;
    } else if (response.status === 401) {
      errorApiKey.textContent = `API Key: ${data.status}`;
    } else {
      console.debug(response, data);
      structureErrorText.textContent = `Error: ${data.status}`;
    }
  } catch (error) {
    // Handle any errors that occurred during the fetch request
    console.error('Error:', error);
    dbUuidResult.textContent = null;
    structureErrorText.textContent = `An error occurred. ${error}`;
  }
});


// Page 2: Get suggested Questions
suggestedBtn.addEventListener('click', async () => {
  const apiKey = apiKeyInput.value.trim();
  const preQuestion = suggestedquestionInput.value.trim();

  // Clear any previous error messages and show processing message
  errorApiKey.textContent = null;
  suggestedErrorText.textContent = null;
  suggestedResult.textContent = 'Processing...';

  // Check if API key is provided
  if ((!apiKey) || apiKey === '') {
    errorApiKey.textContent = 'Please fill The API Key';
    return;
  }

  try {
    // Construct the URL with query parameters
    const url = new URL(`${API_URL}/get-suggested-questions/${dbUuid.value.trim()}`);
    url.searchParams.append('preQuestion', preQuestion);

    // Make a GET request to fetch the suggested questions
    const response = await fetch(url.toString(), {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `${apiKey}`
      }
    });
    const data = await response.json();
    suggestedResult.textContent = null;

    // Display the result based on the response status
    if (response.status === 200) {
      suggestedResult.textContent = JSON.stringify(data, null, 4);
    } else if (response.status === 401) {
      errorApiKey.textContent = `API Key: ${data.status}`;
    } else {
      console.debug(response, data);
      suggestedErrorText.textContent = `Error: ${data.status}`;
    }
  } catch (error) {
    // Handle any errors that occurred during the fetch request
    console.error('Error:', error);
    suggestedErrorText.textContent = `An error occurred. ${error}`;
    suggestedResult.textContent = null;
  }
});


// Page 3: Generate Query
getQueryBtn.addEventListener('click', async () => {
  const apiKey = apiKeyInput.value.trim();
  const question = questionInput.value.trim();

  // Clear any previous error messages and show processing message
  errorApiKey.textContent = null;
  queryErrorText.textContent = null;
  queryResult.textContent = 'Processing...';

  // Check if API key is provided
  if ((!apiKey) || apiKey === '') {
    errorApiKey.textContent = 'Please fill The API Key';
    return;
  }

  try {
    const body = JSON.stringify({
      question, history: null
    });
    const response = await fetch(`${API_URL}/generate-query/${dbUuid.value.trim()}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `${apiKey}`
      },
      body
    });
    const data = await response.json();
    queryResult.textContent = null;

    // Display the result based on the response status
    if (response.status === 200) {
      queryResult.textContent = JSON.stringify(data, null, 4);
    } else if (response.status === 401) {
      errorApiKey.textContent = `API Key: ${data.status}`;
    } else {
      console.debug(response, data);
      queryErrorText.textContent = `Error: ${data.status}`;
    }
  } catch (error) {
    // Handle any errors that occurred during the fetch request
    console.error('Error:', error);
    queryErrorText.textContent = `An error occurred. ${error}`;
    queryResult.textContent = null;
  }
});

getQueryBtnValidate.addEventListener('click', async () => {
  const apiKey = apiKeyInput.value.trim();
  const question = questionInput.value.trim();
  const queryBox = queryResult.textContent.trim();

  // Clear any previous error messages
  errorApiKey.textContent = null;

  // Check if API key is provided
  if ((!apiKey) || apiKey === '') {
    errorApiKey.textContent = 'Please fill The API Key';
    return;
  }

  try {
    const queryBoxJson = JSON.parse(queryBox);
    const query = queryBoxJson?.query;
    if (!(query && query !== undefined && query.trim() !== '')) {
      swal.fire('Error', 'No query was found!', "error");
      return;
    }
    const body = JSON.stringify({
      question,
      threshold: 1.0001,
      query
    });
    const response = await fetch(`${API_URL}/validate-query/${dbUuid.value.trim()}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `${apiKey}`
      },
      body
    });
    const data = await response.json();

    // Display the result based on the response status
    if (response.status === 200) {
      swal.fire('Success', `Query validated with success, response: ${JSON.stringify(data, null, 4)}`);
    } else if (response.status === 401) {
      swal.fire('Error', `API Key: ${data.status}`, "error");
    } else {
      console.debug(response, data);
      swal.fire(`Error: ${data.status}`, "error");
    }
  } catch (error) {
    // Handle any errors that occurred during the fetch request
    console.error('Error:', error);
    swal.fire('Error', `An error occurred. ${error}`, "error");
  }
});

getQueryBtnReject.addEventListener('click', async () => {
  const apiKey = apiKeyInput.value.trim();
  const question = questionInput.value.trim();
  const queryBox = queryResult.textContent.trim();

  // Clear any previous error messages
  errorApiKey.textContent = null;

  // Check if API key is provided
  if ((!apiKey) || apiKey === '') {
    errorApiKey.textContent = 'Please fill The API Key';
    return;
  }

  try {
    const queryBoxJson = JSON.parse(queryBox);
    const query = queryBoxJson?.query;
    if (!(query && query !== undefined && query.trim() !== '')) {
      swal.fire('Error', 'No query was found!', "error");
      return;
    }
    const body = JSON.stringify({
      question,
      query
    });
    const response = await fetch(`${API_URL}/reject-query/${dbUuid.value.trim()}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `${apiKey}`
      },
      body
    });
    const data = await response.json();

    // Display the result based on the response status
    if (response.status === 200) {
      swal.fire('Success', `Query Rejected with success, response: ${JSON.stringify(data, null, 4)}`);
    } else if (response.status === 401) {
      swal.fire('Error', `API Key: ${data.status}`, "error");
    } else {
      console.debug(response, data);
      swal.fire(`Error: ${data.status}`, "error");
    }
  } catch (error) {
    // Handle any errors that occurred during the fetch request
    console.error('Error:', error);
    swal.fire('Error', `An error occurred. ${error}`, "error");
  }
});


// Page 4: Generate Query with context
QueryContextBtn.addEventListener('click', async () => {
  const apiKey = apiKeyInput.value.trim();
  const question = QueryContextInputQuestion.value.trim();
  const history = QueryContextInputHistory.value.trim();

  // Clear any previous error messages and show processing message
  errorApiKey.textContent = null;
  QueryContextErrorText.textContent = null;
  QueryContextResult.textContent = 'Processing...';

  // Check if API key is provided
  if ((!apiKey) || apiKey === '') {
    errorApiKey.textContent = 'Please fill The API Key';
    return;
  }

  try {
    const body = JSON.stringify({
      question, history: history ? JSON.parse(history) : null
    });
    const response = await fetch(`${API_URL}/generate-query/${dbUuid.value.trim()}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `${apiKey}`
      },
      body
    });
    const data = await response.json();
    QueryContextResult.textContent = null;

    // Display the result based on the response status
    if (response.status === 200) {
      QueryContextResult.textContent = JSON.stringify(data, null, 4);
    } else if (response.status === 401) {
      errorApiKey.textContent = `API Key: ${data.status}`;
    } else {
      console.debug(response, data);
      QueryContextErrorText.textContent = `Error: ${data.status}`;
    }
  } catch (error) {
    // Handle any errors that occurred during the fetch request
    console.error('Error:', error);
    QueryContextErrorText.textContent = `An error occurred. ${error}`;
    QueryContextResult.textContent = null;
  }
});

// Page 5: Fix Query
fixQueryBtn.addEventListener('click', async () => {
  const apiKey = apiKeyInput.value.trim();
  const question = fixQueryInputQuestion.value.trim();
  const query = fixQueryInputQuery.value.trim();
  const errors = fixQueryInputError.value.trim();

  // Clear any previous error messages and show processing message
  errorApiKey.textContent = null;
  fixQueryErrorText.textContent = null;
  fixQueryResult.textContent = 'Processing...';

  // Check if API key is provided
  if ((!apiKey) || apiKey === '') {
    errorApiKey.textContent = 'Please fill The API Key';
    return;
  }

  try {
    const body = JSON.stringify({question, query, errors, history: null});
    const response = await fetch(`${API_URL}/fix-query/${dbUuid.value.trim()}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `${apiKey}`
      },
      body
    });
    const data = await response.json();
    fixQueryResult.textContent = null;

    // Display the result based on the response status
    if (response.status === 200) {
      fixQueryResult.textContent = JSON.stringify(data, null, 4);
    } else if (response.status === 401) {
      errorApiKey.textContent = `API Key: ${data.status}`;
    } else {
      console.debug(response, data);
      fixQueryErrorText.textContent = `Error: ${data.status}`;
    }
  } catch (error) {
    // Handle any errors that occurred during the fetch request
    console.error('Error:', error);
    fixQueryErrorText.textContent = `An error occurred. ${error}`;
    fixQueryResult.textContent = null;
  }
});


// Page 6: Handle database - Delete Cache
handleDBBtnCache.addEventListener('click', async () => {
  const apiKey = apiKeyInput.value.trim();

  // Clear any previous error messages and show processing message
  errorApiKey.textContent = null;
  handleDBResult.textContent = 'Processing...';

  // Check if API key is provided
  if ((!apiKey) || apiKey === '') {
    errorApiKey.textContent = 'Please fill The API Key';
    return;
  }

  try {
    const response = await fetch(`${API_URL}/delete-db-cache/${dbUuid.value.trim()}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `${apiKey}`
      }
    });
    const data = await response.json();

    // Display the result based on the response status
    if (response.status === 200) {
      handleDBResult.textContent = JSON.stringify(data, null, 4);
    } else if (response.status === 401) {
      handleDBResult.textContent = `Error: API Key - ${data.status}`;
    } else {
      console.debug(response, data);
      handleDBResult.textContent = `Error: ${data.status}`;
    }
  } catch (error) {
    // Handle any errors that occurred during the fetch request
    console.error('Error:', error);
    handleDBResult.textContent = `An error occurred. ${error}`;
  }
});

// Page 6: Handle database - Delete Database
handleDBBtnDelete.addEventListener('click', async () => {
  const apiKey = apiKeyInput.value.trim();

  // Clear any previous error messages and show processing message
  errorApiKey.textContent = null;
  handleDBResult.textContent = 'Processing...';

  // Check if API key is provided
  if ((!apiKey) || apiKey === '') {
    errorApiKey.textContent = 'Please fill The API Key';
    return;
  }

  try {
    const response = await fetch(`${API_URL}/delete-db/${dbUuid.value.trim()}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `${apiKey}`
      }
    });
    const data = await response.json();

    // Display the result based on the response status
    if (response.status === 200) {
      handleDBResult.textContent = JSON.stringify(data, null, 4);
    } else if (response.status === 401) {
      handleDBResult.textContent = `Error: API Key - ${data.status}`;
    } else {
      console.debug(response, data);
      handleDBResult.textContent = `Error: ${data.status}`;
    }
  } catch (error) {
    // Handle any errors that occurred during the fetch request
    console.error('Error:', error);
    handleDBResult.textContent = `An error occurred. ${error}`;
  }
});
