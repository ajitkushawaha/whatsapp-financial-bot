import pandas as pd

CSV_FILE = "final_user_queries.csv"

def create_csv_with_inputs(user_inputs):
    """
    Create a CSV file with a column 'user_input' from a list of inputs.
    Initially, the 'response' column will be empty.
    """
    df = pd.DataFrame({"user_input": user_inputs, "response": [""] * len(user_inputs)})
    df.to_csv(CSV_FILE, index=False)

def read_queries():
    """Read the CSV and return it as a DataFrame."""
    return pd.read_csv(CSV_FILE)

def write_response(df):
    """
    Save the entire DataFrame (with responses) to the CSV file.
    """
    df.to_csv(CSV_FILE, index=False)
