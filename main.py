import json
from flask import jsonify
from pathlib import Path
from src.table_processor import TableProcessor
from src.excel_file import ExcelFile

# Process the uploaded file
excel_file = ExcelFile(Path('tests/example_2.xlsx'))
sheet = excel_file.get_sheet('Analysis Output')
table_processor = TableProcessor(sheet)
all_tables_data = table_processor.process_tables()
# save results in json
with open('results.json', 'w') as f:
    json.dump(all_tables_data, f)
print(all_tables_data)
