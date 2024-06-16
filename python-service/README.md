# README

The goal is to build a Retrieval-Augmented Generation (RAG) system. All files are parsed by custom code, uploaded to OpenAI's vector database, and integrated with the Assistant for enhanced functionality.

## Run the project
1. Run the Flask application:
   ```bash
   python app.py
   ```

2. Test the endpoint using curl or Postman:
    ```bash
    curl -F "file=@tests/example_0.xlsx" http://127.0.0.1:5000/upload
    ```

## Run tests
1. Run the tests:
   ```bash
   python -m unittest discover -s tests -p '*_test.py'
   ```
