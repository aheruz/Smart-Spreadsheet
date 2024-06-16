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
        self._assistant = self._get_assistant() or self._create_assistant()
        self._vector_store = self._get_vector_store() or self._create_vector_store()

    def upload_file(self, filepath: str) -> str:
        """
        Upload a file to the OpenAI API and add it to the vector store
        - If the file is already uploaded, delete it
        - Upload the file
        - Add the file to the vector store
        """
        # Ready the file for upload to OpenAI
        file_stream = open(filepath, "rb")

        # Delete the existing file if it exists
        existing_file = self._get_file_by_name(filepath)
        if existing_file:
            self._delete_file(existing_file.id)

        # Upload the files, and add them to the vector store
        file_batch = self._client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=self._vector_store.id, files=[file_stream]
        )

        # Update the assistant to use the new vector store
        self._assign_vector_to_assistant()

        return file_batch.status
    
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
            instructions="You are an expert financial analyst. Use you knowledge base to answer questions about audited financial statements.",
            model="gpt-4o",
            tools=[{"type": "file_search"}],
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