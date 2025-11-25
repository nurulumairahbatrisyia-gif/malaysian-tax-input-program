import os
import pandas as pd
from typing import Optional, Dict

# --- Utility data (tuple list used to show a tuple data type) ---
# Brackets expressed as (upper_limit, rate) where upper_limit is cumulative.
# The calculation will apply each bracket incrementally to the chargeable income.
TAX_BRACKETS = (
    (5_000, 0.00),
    (20_000, 0.01),
    (35_000, 0.03),
    (50_000, 0.06),
    (70_000, 0.11),
    (100_000, 0.19),
    (400_000, 0.25),
    (600_000, 0.26),
    (2_000_000, 0.28),
    (float('inf'), 0.30),
)

CSV_HEADER = ["ic_number", "income", "tax_relief", "tax_payable"]

def verify_user(ic_number: str, password: str) -> bool:
    """
    Verify the user's credentials:
    - IC number must be 12 digits (string of digits).
    - Password must match last 4 digits of the IC number.
    Returns True if valid, False otherwise.
    """
    if not isinstance(ic_number, str) or not isinstance(password, str):
        return False
    if not ic_number.isdigit() or len(ic_number) != 12:
        return False
    return ic_number[-4:] == password

def calculate_tax(income: float, tax_relief: float) -> float:
    """
    Calculate Malaysian personal income tax (resident) using progressive brackets.
    Steps:
    - compute chargeable income = max(0, income - tax_relief)
    - apply progressive taxation over the bracket increments
    Returns the tax payable (rounded to 2 decimals).
    """
    try:
        income = float(income)
        tax_relief = float(tax_relief)
    except (TypeError, ValueError):
        raise ValueError("Income and tax_relief must be numbers.")

    chargeable = max(0.0, income - tax_relief)
    remaining = chargeable
    prev_limit = 0.0
    tax = 0.0

    for limit, rate in TAX_BRACKETS:
        if remaining <= 0:
            break
        # Incremental width for this bracket
        bracket_width = limit - prev_limit
        taxable_in_this_bracket = min(remaining, bracket_width)
        tax += taxable_in_this_bracket * rate
        remaining -= taxable_in_this_bracket
        prev_limit = limit

    return round(tax, 2)

def save_to_csv(data: Dict[str, object], filename: str) -> None:
    """
    Save the user's data to CSV.
    data: dict containing keys 'ic_number', 'income', 'tax_relief', 'tax_payable'
    filename: csv file path
    If file doesn't exist, create with header. If exists, append.
    Uses pandas for CSV operations.
    """
    df = pd.DataFrame([{
        "ic_number": str(data.get("ic_number", "")),
        "income": float(data.get("income", 0.0)),
        "tax_relief": float(data.get("tax_relief", 0.0)),
        "tax_payable": float(data.get("tax_payable", 0.0)),
    }])
    if not os.path.isfile(filename):
        df.to_csv(filename, index=False, columns=CSV_HEADER)
    else:
        df.to_csv(filename, mode="a", header=False, index=False, columns=CSV_HEADER)

def read_from_csv(filename: str) -> Optional[pd.DataFrame]:
    """
    Read CSV and return a pandas DataFrame, or None if file does not exist.
    """
    if not os.path.isfile(filename):
        return None
    df = pd.read_csv(filename)
    return df