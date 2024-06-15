import json
import os
from flask import jsonify
from pathlib import Path
from src.table_processor import TableProcessor
from src.excel_file import ExcelFile

os.environ['PYTHONPATH'] = os.path.dirname(os.path.abspath(__file__))
# Process the uploaded file
path = os.environ['PYTHONPATH']
excel_file = ExcelFile(Path(f'{path}/tests/example_2.xlsx'))
sheet = excel_file.get_sheet('Analysis Output')
table_processor = TableProcessor(sheet)
all_tables_data = table_processor.process_tables()
# save results in json
with open('results.json', 'w') as f:
    json.dump(all_tables_data, f)
print(all_tables_data)
