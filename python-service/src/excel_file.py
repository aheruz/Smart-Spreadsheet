from pathlib import Path
from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet  

class ExcelFile:
    """
    Load an Excel file and get a worksheet from it.
    """

    def __init__(self, filename: Path):
        self.workbook = load_workbook(filename, data_only=True)

    def get_sheet(self, sheet_name: str) -> Worksheet:
        """
        Retrieve a sheet from the workbook.

        Args:
            sheet_name (str): The name of the worksheet

        Returns:
            Worksheet: The requested sheet object.
        """
        return self.workbook[sheet_name]
