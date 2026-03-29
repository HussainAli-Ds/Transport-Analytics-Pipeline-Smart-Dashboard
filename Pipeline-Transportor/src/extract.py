import pandas as pd

def read_excel(file_path):
    df = pd.read_excel(file_path)

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df