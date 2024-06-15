import unittest
from pathlib import Path
from openpyxl import load_workbook
from app.table_processor import TableProcessor
from app.excel_file import ExcelFile
import json

class TestTableProcessor(unittest.TestCase):
    def setUp(self):
        # Load example Excel files
        self.example_0_path = Path('tests/example_0.xlsx')
        self.example_1_path = Path('tests/example_1.xlsx')
        self.example_2_path = Path('tests/example_2.xlsx')

    def test_example_0(self):
        excel_file = ExcelFile(self.example_0_path)
        sheet = excel_file.get_sheet('Analysis Output')
        table_processor = TableProcessor(sheet)
        tables = table_processor.process_tables()

        with open('tests/example_0.json', 'r') as f:
            expected_tables = json.load(f)
        self.assertEqual(len(tables), 8, f"{self.example_0_path.name} should generate 8 tables, got {len(tables)}")
        self.assertEqual(tables, expected_tables, f"{self.example_0_path.name} should match the expected JSON output")

    def test_example_1(self):
        excel_file = ExcelFile(self.example_1_path)
        sheet = excel_file.get_sheet('Analysis Output')
        table_processor = TableProcessor(sheet)
        tables = table_processor.process_tables()

        with open('tests/example_1.json', 'r') as f:
            expected_tables = json.load(f)

        self.assertEqual(len(tables), 4, f"{self.example_1_path.name} should generate 4 tables, got {len(tables)}")
        self.assertEqual(tables, expected_tables, f"{self.example_1_path.name} should match the expected JSON output")

    def test_example_2(self):
        excel_file = ExcelFile(self.example_2_path)
        sheet = excel_file.get_sheet('Analysis Output')
        table_processor = TableProcessor(sheet)
        tables = table_processor.process_tables()

        with open('tests/example_2.json', 'r') as f:
            expected_tables = json.load(f)

        self.assertEqual(len(tables), 4, f"{self.example_2_path.name} should generate 4 tables, got {len(tables)}")
        self.assertEqual(tables, expected_tables, f"{self.example_2_path.name} should match the expected JSON output")

if __name__ == '__main__':
    unittest.main()
