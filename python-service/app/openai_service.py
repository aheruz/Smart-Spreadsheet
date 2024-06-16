import os
from typing import Optional
from openai import OpenAI
from openai.types.beta.vector_store import VectorStore
from openai.types.beta.assistant import Assistant
from openai.types import FileObject

class OpenAiService:
    """
    Service to interact with the OpenAI API
    """
    ASSISTANT_NAME = "CapixAi Analyst Assistant"
    VECTOR_STORE_NAME = "CapixAi Analyst Assistant"

    def __init__(self):
        self._client = OpenAI()
        self._assistant = self._create_or_get_assistant()
        self._vector_store = self._create_or_get_vector_store()

    def upload_file(self, filepath: str) -> str:
        """
        Upload a file to the OpenAI API and add it to the vector store
        - If the file is already uploaded, delete it
        - Upload the file
        - Add the file to the vector store
        """
        try:
            # Delete the existing file if it exists
            existing_file = self._get_file_by_name(filepath)
            if existing_file:
                self._delete_file(existing_file.id)
            # Upload the files, and add them to the vector store
            with open(filepath, "rb") as file_stream:
                file_batch = self._client.beta.vector_stores.file_batches.upload_and_poll(
                    vector_store_id=self._vector_store.id, files=[file_stream]
                )
            # Update the assistant to use the new vector store
            self._assign_vector_to_assistant()
            return file_batch.status
        except Exception as e:
            return "Failed to upload file"


    def _create_or_get_assistant(self) -> Assistant:
        """
        Retrieve the assistant if it exists or create a new one.
        """
        assistant = self._get_assistant()
        if not assistant:
            assistant = self._create_assistant()
        return assistant

    def _create_or_get_vector_store(self) -> VectorStore:
        """
        Retrieve the vector store if it exists or create a new one.
        """
        vector_store = self._get_vector_store()
        if not vector_store:
            vector_store = self._create_vector_store()
        return vector_store

    def _get_file_by_name(self, filepath: str) -> Optional[FileObject]:
        """
        Get the file by name from the OpenAI API
        """
        filename = os.path.basename(filepath)
        files = self._client.files.list(purpose="assistants", extra_query = {"filename":filename})
        for file in files:
            if file.filename == filename:
                return file
        return None
    
    def _delete_file(self, id: str):
        self._client.files.delete(id)
    
    def _create_assistant(self) -> Assistant:
        """
        Create an assistant with the given name and instructions
        """
        return self._client.beta.assistants.create(
            name=self.ASSISTANT_NAME,
            instructions=(
                "You are CapixAi Analyst Assistant, an expert in financial analysis. "
                "Your task is to analyze financial data from Excel files and answer questions accurately. "
                "Use the vector store to retrieve relevant information from the provided files. "
                "Here are your guidelines:\n\n"
                "1. **Understand the Context**: Each Excel file contains financial data with columns such as 'Date', "
                "'Total Cash and Cash Equivalents', 'Accounts Receivable', 'Total Assets', and more. Familiarize yourself "
                "with the structure of these tables before answering questions.\n\n"
                "2. **Accurate Data Retrieval**: When answering questions, always refer to the specific cells or sections of the Excel file "
                "where the relevant data is located. Provide cell references in your answers to ensure transparency.\n\n"
                "3. **Handle Complex Inquiries**: For questions that require calculations or inferences (e.g., combining data from multiple columns or rows), "
                "perform the necessary computations and show your work step-by-step. Clearly explain how you arrived at the answer.\n\n"
                "4. **Minimize Hallucinations**: Base your answers strictly on the data available in the Excel files. If the information is not present or cannot be determined "
                "from the provided data, state that the data is not available.\n\n"
                "5. **Enable Citations**: Whenever possible, cite the source of your information by including the cell references or file paths. This helps verify the accuracy of your answers.\n\n"
                "6. **Structured Responses**: Provide answers in a structured format using Markdown, including any relevant calculations, citations, and explanations. For example:\n\n"
                "   **Question**: What is the Total Cash and Cash Equivalent of Nov. 2023?\n"
                "   **Answer**:\n\n"
                "   **Total Cash and Cash Equivalent of Nov. 2023**\n"
                "   The Total Cash and Cash Equivalent of Nov. 2023 is **$1,000,000**.\n"
                "   [Source: example.xlsx, Cell: B5]\n\n"
                "7. **Error Handling**: If you encounter any issues or the data cannot be retrieved, provide a clear and concise error message.\n\n"
                "8. **Execute Code for Calculations**: Use the integrated code interpreter to perform any necessary calculations or data processing to answer the questions accurately."
                "By following these guidelines, ensure that your responses are accurate, transparent, and useful to the user."
            ),
            model="gpt-4o",
            tools=[{"type": "file_search"}, {"type": "code_interpreter"}],
        )

    def _get_assistant(self) -> Optional[Assistant]:
        """
        Get the assistant by name from the OpenAI API
        """
        my_assistants = self._client.beta.assistants.list().data
        for assistant in my_assistants:
            if assistant.name == self.ASSISTANT_NAME:
                return assistant
        return None

    def _get_vector_store(self) -> Optional[VectorStore]:
        """
        Get the vector store by name from the OpenAI API
        """
        vector_stores = self._client.beta.vector_stores.list().data
        for vector_store in vector_stores:
            if vector_store.name == self.VECTOR_STORE_NAME:
                return vector_store
        return None
    
    def _create_vector_store(self):
        return self._client.beta.vector_stores.create(name=self.VECTOR_STORE_NAME)
    
    def _assign_vector_to_assistant(self) -> None:
        """
        Update the assistant to to use the new Vector Store
        """
        self._assistant = self._client.beta.assistants.update(
            assistant_id=self._assistant.id,
            tool_resources={"file_search": {"vector_store_ids": [self._vector_store.id]}},
        )