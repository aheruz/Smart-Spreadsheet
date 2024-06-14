# Table Detection Rules for Excel Sheets

## Top-Left Cell
- **Header Style**: Cell has specific header style (background color, top+side borders).
- **Position**: No header-styled cell immediately above or to the left.

## Top-Right Cell
- **Header Style**: Cell has specific header style.
- **Position**: No header-styled cell immediately to the right.

## Bottom-Right Cell
- **Borders**: Cell has bottom and right borders.
- **Position**: No cell with right border below or bottom+right borders to the right.

## General Detection
- Identify top-left cell using header style.
- Find top-right cell in the same row.
- Find bottom-right cell in the same column as top-right cell.