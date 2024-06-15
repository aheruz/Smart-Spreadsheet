import json
import os
from pathlib import Path
from werkzeug.utils import secure_filename
from typing import List

class FileUploadService:
    UPLOAD_FOLDER = 'storage/'

    def __init__(self, upload_folder=None):
        if upload_folder:
            self.UPLOAD_FOLDER = upload_folder
        os.makedirs(self.UPLOAD_FOLDER, exist_ok=True)

    def save_file(self, file):
        if not file:
            raise ValueError("No file provided")
        if file.filename == '':
            raise ValueError("No selected file")

        # Save the file to the upload folder
        filename = secure_filename(file.filename)
        filepath = os.path.join(self.UPLOAD_FOLDER, filename)
        file.save(filepath)

        return filepath

    def save_processed_data(self, data: List, filename: str):
        # Save the processed data to a file
        if not data:
            raise ValueError("No data provided")
        if not filename:
            raise ValueError("No filename provided")

        # Secure the filename
        filename = Path(filename).stem
        filename = secure_filename(f"{filename}.json")
        filepath = os.path.join(self.UPLOAD_FOLDER, filename)

        try:
            with open(filepath, 'w') as file:
                file.write(json.dumps(data))
        except Exception as e:
            raise ValueError(f"Error saving processed data: {e}")

        return filepath
