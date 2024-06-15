# Development Plan

### Step 1: Parse and Serialize Tables from `example_0.xlsx`
1. **Load Excel File**:
   Use `openpyxl` to load the Excel file and extract the worksheet.
   ```python:main.py
   from pathlib import Path
   from helper_functions import get_sheet_from_excel, process_simple_table

   ws = get_sheet_from_excel(Path('example_0.xlsx'), 'Sheet1')
   table = process_simple_table(ws)
   print(table)
   ```

### Step 2: Implement AI Chat Function
1. **Integrate Vercel AI SDK**:
   Install and set up the Vercel AI SDK.
   ```bash
   npm install @vercel/ai
   ```

2. **Create AI Integration**:
   ```javascript:ai_integration.js
   import { createClient } from '@vercel/ai';

   const client = createClient({
     apiKey: process.env.VERCEL_AI_API_KEY,
   });

   export async function askQuestion(question, context) {
     const response = await client.ask({
       question,
       context,
     });
     return response.answer;
   }
   ```

### Step 3: Broaden Functionality to Parse `example_1.xlsx` and `example_2.xlsx`
1. **Generalize Parsing**:
   Update the parsing function to handle multiple files.
   ```python:main.py
   files = ['example_0.xlsx', 'example_1.xlsx', 'example_2.xlsx']
   for file in files:
       ws = get_sheet_from_excel(Path(file), 'Sheet1')
       table = process_simple_table(ws)
       print(table)
   ```

### Step 4: Enhance AI to Answer Inferred Questions
1. **Update AI Integration**:
   Modify the `askQuestion` function to handle more complex queries.
   ```javascript:ai_integration.js
   export async function askComplexQuestion(question, context) {
     const response = await client.ask({
       question,
       context,
       infer: true,
     });
     return response.answer;
   }
   ```

### Step 5: Integrate a Vector Database for Enhanced Search
1. **Choose and Set Up Pinecone**:
   - **Install Pinecone Client**:
     ```bash
     pip install pinecone-client
     ```

   - **Initialize Pinecone**:
     ```python:pinecone_setup.py
     import pinecone

     pinecone.init(api_key='your_pinecone_api_key', environment='us-west1-gcp')
     ```

2. **Index Data**:
   - **Create Index**:
     ```python:pinecone_setup.py
     index_name = 'spreadsheet-index'
     if index_name not in pinecone.list_indexes():
         pinecone.create_index(index_name, dimension=128)  # Adjust dimension as needed
     index = pinecone.Index(index_name)
     ```

   - **Index Spreadsheet Data**:
     ```python:index_data.py
     from helper_functions import get_sheet_from_excel, process_simple_table
     from pinecone_setup import index
     from pathlib import Path

     def index_spreadsheet(file_path, sheet_name):
         ws = get_sheet_from_excel(Path(file_path), sheet_name)
         table = process_simple_table(ws)
         for i, record in enumerate(table):
             vector = generate_vector(record)  # Implement generate_vector to convert record to vector
             index.upsert([(f'{file_path}_{i}', vector)])

     files = ['example_0.xlsx', 'example_1.xlsx', 'example_2.xlsx']
     for file in files:
         index_spreadsheet(file, 'Sheet1')
     ```

3. **Implement Search Functionality**:
   - **Search Function**:
     ```python:search.py
     from pinecone_setup import index

     def search_spreadsheet(query):
         query_vector = generate_vector(query)  # Implement generate_vector to convert query to vector
         results = index.query(query_vector, top_k=5)
         return results

     # Example usage
     query = "Total Cash and Cash Equivalent of Nov. 2023"
     results = search_spreadsheet(query)
     print(results)
     ```

4. **Integrate with AI**:
   - **Update AI Integration**:
     ```javascript:ai_integration.js
     import { searchSpreadsheet } from './search';

     export async function askQuestion(question, context) {
       const searchResults = searchSpreadsheet(question);
       const response = await client.ask({
         question,
         context: searchResults,
       });
       return response.answer;
     }
     ```

### Step 6: Deploy the Smart Spreadsheet AI
1. **Deploy on Vercel**:
   Ensure all necessary environment variables and dependencies are set up.
   ```bash
   vercel deploy
   ```

### Step 7: Additional Considerations
1. **Reduce Hallucinations**:
   Implement validation checks and use structured prompts to minimize hallucinations.

2. **Handle Large Spreadsheets**:
   Implement chunking or pagination to handle large datasets.

3. **Enable Citations**:
   Modify the AI response to include source references.

4. **Enable Numerical Calculations**:
   Ensure the AI can perform accurate calculations by integrating a reliable math library.

### Step 8: Final Steps
1. **Testing**:
   Thoroughly test each feature to ensure functionality and accuracy.

2. **Documentation**:
   Update the `README.md` with setup and usage instructions.

### Deploy
1. Run the Flask application:
   ```bash
   python app.py
   ```

2. Test the endpoint using curl or Postman:
    ```bash
    curl -F "file=@tests/example_0.xlsx" http://127.0.0.1:5000/upload
    ```

### Run tests
1. Run the tests:
   ```bash
   python -m unittest discover -s tests -p '*_test.py'
   ```

## TODO
- [ ] Handle column combination on headers _(eg. `Portfolio Breakdown [USD]` in example_0.xlsx)_