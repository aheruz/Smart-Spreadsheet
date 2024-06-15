from flask import Blueprint, request, jsonify
from pathlib import Path
from app.table_processor import TableProcessor
from app.excel_file import ExcelFile
from app.file_upload_service import FileUploadService

upload_bp = Blueprint('upload', __name__)
file_upload_service = FileUploadService()

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    try:
        filepath = file_upload_service.save_file(file)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    # Process the uploaded file
    excel_file = ExcelFile(Path(filepath))
    sheet = excel_file.get_sheet('Analysis Output')
    table_processor = TableProcessor(sheet)
    all_tables_data = table_processor.process_tables()
    
    return jsonify(all_tables_data)