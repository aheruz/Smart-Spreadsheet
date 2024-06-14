import unittest
from pathlib import Path
from openpyxl import load_workbook
from src.table_processor import TableProcessor
from src.excel_file import ExcelFile

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
        tables = table_processor.identify_tables()
        self.assertEqual(len(tables), 8, "example_0.xlsx should generate 8 tables")

    def test_example_1(self):
        excel_file = ExcelFile(self.example_1_path)
        sheet = excel_file.get_sheet('Analysis Output')
        table_processor = TableProcessor(sheet)
        tables = table_processor.identify_tables()
        self.assertEqual(len(tables), 4, "example_1.xlsx should generate 4 tables")

    def test_example_2(self):
        excel_file = ExcelFile(self.example_2_path)
        sheet = excel_file.get_sheet('Analysis Output')
        table_processor = TableProcessor(sheet)
        tables = table_processor.identify_tables()
        self.assertEqual(len(tables), 4, "example_2.xlsx should generate 4 tables")

if __name__ == '__main__':
    unittest.main()
