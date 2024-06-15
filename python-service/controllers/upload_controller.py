from flask import Blueprint, request, jsonify
from pathlib import Path
from src.table_processor import TableProcessor
from src.excel_file import ExcelFile
from werkzeug.utils import secure_filename
import os

upload_bp = Blueprint('upload', __name__)
UPLOAD_FOLDER = 'uploads/'

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Process the uploaded file
        excel_file = ExcelFile(Path(filepath))
        sheet = excel_file.get_sheet('Analysis Output')
        table_processor = TableProcessor(sheet)
        all_tables_data = table_processor.process_tables()
        
        return jsonify({"tables": all_tables_data})