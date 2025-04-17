import pandas as pd

# Replace with your published-CSV URL
SHEET_CSV_URL = (
    "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID"
    "/export?format=csv&gid=0"
)

def load_reference():
    """
    Reads the Google Sheet CSV into a DataFrame with columns ['item', 'max_price']
    Ensure your sheet has headers exactly: item, max_price
    """
    df = pd.read_csv(SHEET_CSV_URL)
    df = df.rename(columns=str.strip)
    df['max_price'] = df['max_price'].astype(float)
    return df