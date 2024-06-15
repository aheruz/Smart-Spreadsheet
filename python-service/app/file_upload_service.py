import os
from werkzeug.utils import secure_filename

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
