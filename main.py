from pathlib import Path
from src.table_processor import TableProcessor
from src.excel_file import ExcelFile

filename = Path('tests/example_2.xlsx')
sheet_name = 'Analysis Output'

excel_file = ExcelFile(filename)
sheet = excel_file.get_sheet(sheet_name)
# For identifying and processing all tables
table_processor = TableProcessor(sheet)
all_tables_data = table_processor.process_tables()
print("All Tables Data:", all_tables_data)