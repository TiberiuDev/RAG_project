# src/csv_loader.py
from pathlib import Path
from typing import List
import pandas as pd

from .config import SETTINGS
from .error_record import ErrorRecord

def load_error_records_from_csv(path: Path | None = None) -> List[ErrorRecord]:
    if path is None:
        path = SETTINGS.excel_path  # rename to point to csv or add a new setting
    # if path is .xlsx change parsing, here we support csv already uploaded
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    # try latin1 encoding (safe for this file)
    df = pd.read_csv(path, encoding="latin1")
    records: List[ErrorRecord] = []

    # Normalize columns: strip names
    cols = {c.strip(): c for c in df.columns}
    # safe getters
    def get_val(r, name):
        return str(r.get(cols.get(name, ""), "")).strip()

    for _, row in df.iterrows():
        # skip empty rows
        if row.isna().all():
            continue

        error_code = get_val(row, "ID")
        sheet = get_val(row, "Integration Flow")
        
        if sheet.lower() == "nan":
            sheet = ""
        
        hire_validation = get_val(row, "Hire Sync Validation")
        error_msg = get_val(row, "Error Message Notification")
        origin_field = get_val(row, "Where to do the correction")
        owner = get_val(row, "Who should do the correction")

        # choose title: prefer error_msg then short hire_validation
        title = error_msg if error_msg else (hire_validation[:120] if hire_validation else "")

        rec = ErrorRecord(
            error_code=error_code,
            sheet=sheet,
            title=title,
            non_technical=hire_validation,
            origin_field=origin_field,
            owner=owner,
            action=""  # optional: can be filled by a rule or synthesised later
        )
        records.append(rec)

    return records
