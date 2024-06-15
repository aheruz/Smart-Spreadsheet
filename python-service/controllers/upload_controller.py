from flask import Blueprint, request, jsonify
from pathlib import Path

from app.excel_file import ExcelFile
from app.file_upload_service import FileUploadService
from app.openai_service import OpenAiService
from app.table_processor import TableProcessor

class UploadController:
    def __init__(self):
        self._upload_bp = Blueprint('upload', __name__)
        self.file_upload_service = FileUploadService()
        self.openai_service = OpenAiService()
        self._upload_bp.add_url_rule('/upload', 'upload_file', self.upload_file, methods=['POST'])

    def upload_file(self):
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        filepath = self.file_upload_service.save_file(file)
        # Process the file
        excel_file = ExcelFile(Path(filepath))
        sheet = excel_file.get_sheet('Analysis Output')
        table_processor = TableProcessor(sheet)
        all_tables_data = table_processor.process_tables()
        # Save the processed data
        filepath = self.file_upload_service.save_processed_data(all_tables_data, file.filename)
        file_id = self.openai_service.upload_file(filepath)
        return jsonify(file_id)

    def __call__(self):
        return self._upload_bp
