# Party Ledger Manager

A lightweight offline desktop app for managing party transactions and ledgers with single Excel file storage.

Built with **PyQt6** (UI), **Pandas** (data operations), **openpyxl** (Excel engine), packaged via **PyInstaller**.

## Features

- **Two-pane layout**: Party list sidebar + transaction table
- **Party management**: Create and remove parties
- **Inline transaction entry**: Add transactions directly in the table (Date, Description, Qty, Rate, Total)
- **Smart entry**: Enter Qty×Rate for auto-calculated Total, or enter Total directly (disables Qty/Rate)
- **Party filtering**: Click a party in the sidebar to filter; click again to show all
- **Date filter**: Filter transactions by date range with auto-reverse
- **PDF export**: Generate printable PDF reports (respects active filters)
- **Grand total**: Running total at the bottom of the table and PDF
- **Single-file storage**: All data in one `ledger.xlsx` file, one sheet per party
- **Standalone .exe**: No Python installation required for end users

## Download & Installation

### Run from source

1. Install Python 3.10+
2. Clone the repo:
   ```
   git clone https://github.com/mihirpanara11/transaction_app.git
   cd transaction_app
   ```
3. Install dependencies:
   ```
   pip install PyQt6 pandas openpyxl pyinstaller
   ```
4. Run:
   ```
   python ledger_app.py
   ```

## Usage

1. Run `dist\PartyLedger.exe` (pre-built) or `python ledger_app.py`
2. Create parties using the sidebar buttons
3. Select a party to add transactions inline
4. Use Date Filter button for date-range filtering
5. Export Report saves a PDF of current view

## Project Files

- `ledger_app.py` – Main application source
- `run_and_test.py` – Automated integration tests
- `PartyLedger.spec` – PyInstaller build configuration
