import os
import sys
import pandas as pd
from unittest.mock import patch
from PyQt6.QtWidgets import QApplication, QDialog

# Ensure absolute path matches workspace
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Import classes from ledger_app
from ledger_app import LedgerApp, TransactionDialog, CreatePartyDialog

def run_test():
    print("Initializing test environment...")
    
    # Clean up any existing ledger.xlsx file
    excel_path = "ledger.xlsx"
    if os.path.exists(excel_path):
        try:
            os.remove(excel_path)
            print("Removed old ledger.xlsx to start fresh.")
        except Exception as e:
            print(f"Warning: Could not remove old file: {e}")

    # Create QApplication instance (required for Qt widgets)
    app = QApplication(sys.argv)
    
    # Instantiate the application
    print("Instantiating LedgerApp...")
    window = LedgerApp()

    # 1. Test "Create Party" programmatically
    print("Creating 'ACME Corp' party...")
    with patch.object(CreatePartyDialog, 'exec', return_value=True):
        with patch.object(CreatePartyDialog, 'get_name', return_value="ACME Corp"):
            window.add_party()

    print("Creating 'Globex' party...")
    with patch.object(CreatePartyDialog, 'exec', return_value=True):
        with patch.object(CreatePartyDialog, 'get_name', return_value="Globex"):
            window.add_party()

    # Verify parties are created in the Excel sheets and QListWidget
    xl = pd.ExcelFile(excel_path)
    print(f"Excel sheets found: {xl.sheet_names}")
    assert "ACME Corp" in xl.sheet_names, "ACME Corp sheet should be created!"
    assert "Globex" in xl.sheet_names, "Globex sheet should be created!"
    
    # 2. Test "Create Transaction" programmatically for ACME Corp (Qty+Rate)
    print("Adding transaction for 'ACME Corp'...")
    mock_data = {
        "Date": "2026-06-08",
        "Party Name": "ACME Corp",
        "Description": "Initial supply delivery",
        "Quantity": 15.0,
        "Rate": 12.5,
        "Total": 187.5  # Auto-calculated: 15 * 12.5
    }
    with patch.object(QDialog, 'exec', return_value=True):
        with patch.object(TransactionDialog, 'get_data', return_value=mock_data):
            window.add_transaction()

    # 3. Test "Create Transaction" programmatically for Globex (Total only)
    print("Adding transaction for 'Globex' (Total only)...")
    mock_data_globex = {
        "Date": "2026-06-07",
        "Party Name": "Globex",
        "Description": "Consulting services",
        "Quantity": 0.0,
        "Rate": 0.0,
        "Total": 500.0  # Entered directly, no Qty/Rate
    }
    with patch.object(QDialog, 'exec', return_value=True):
        with patch.object(TransactionDialog, 'get_data', return_value=mock_data_globex):
            window.add_transaction()

    # 4. Load all and verify combined transaction details
    print("Loading combined data...")
    df = window.load_all_data()
    print("\nCombined Dataframe Content:")
    print(df)
    
    assert len(df) == 2, "Should have 2 transactions total."
    
    # Verify values and automatic calculations in refresh_view
    window.refresh_view()
    
    # Row 0 should be ACME Corp (sorted chronologically descending/ascending)
    # Our refresh_view sorts descending: df = df.sort_values(by='Date', ascending=False)
    # ACME Corp: 2026-06-08, Globex: 2026-06-07
    # So index 0 (top row) in table should be ACME Corp, index 1 should be Globex.
    
    # Let's double check columns from QTableWidget
    table_row_0_party = window.table.item(0, 1).text()
    table_row_0_total = window.table.item(0, 5).text()
    table_row_1_party = window.table.item(1, 1).text()
    table_row_1_total = window.table.item(1, 5).text()

    print(f"\nTable verified successfully:")
    print(f"Row 0 (Newest): Party={table_row_0_party}, Total={table_row_0_total}")
    print(f"Row 1 (Older): Party={table_row_1_party}, Total={table_row_1_total}")

    assert table_row_0_party == "ACME Corp"
    assert table_row_0_total == "187.5" # 15.0 * 12.5 = 187.5
    assert table_row_1_party == "Globex"
    assert table_row_1_total == "500.0" # 5.0 * 100.0 = 500.0
    
    print("\nAll programmatic automation tests passed flawlessly!")

if __name__ == "__main__":
    run_test()
