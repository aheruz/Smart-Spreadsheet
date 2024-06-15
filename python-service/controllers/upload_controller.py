from flask import Blueprint, request, jsonify
from pathlib import Path
from app.table_processor import TableProcessor
from app.excel_file import ExcelFile
from app.file_upload_service import FileUploadService

class UploadController:
    def __init__(self):
        self._upload_bp = Blueprint('upload', __name__)
        self.file_upload_service = FileUploadService()
        self._upload_bp.add_url_rule('/upload', 'upload_file', self.upload_file, methods=['POST'])

    def upload_file(self):
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        try:
            filepath = self.file_upload_service.save_file(file)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        # Process the uploaded file
        excel_file = ExcelFile(Path(filepath))
        sheet = excel_file.get_sheet('Analysis Output')
        table_processor = TableProcessor(sheet)
        all_tables_data = table_processor.process_tables()
        
        return jsonify(all_tables_data)

    def __call__(self):
        return self._upload_bp
