import pandas as pd

def read_raw_data():
    df = pd.read_csv("data/raw/amazon.csv")
    print("Raw Amazon data loaded")
    return df

def basic_processing(df):
    # Drop rows with missing Order_ID
    if "Order_ID" in df.columns:
        df = df[df["Order_ID"].notna()]

    # Convert Order_Date if exists
    if "Order_Date" in df.columns:
        df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")

    # Remove negative sales if column exists
    if "Sales" in df.columns:
        df = df[df["Sales"] >= 0]

    print("Basic processing completed")
    return df

def write_curated_data(df):
    df.to_csv("data/curated/amazon_base_curated.csv", index=False)
    print("Curated data written")

def run_base_pipeline():
    df = read_raw_data()
    df = basic_processing(df)
    write_curated_data(df)

if __name__ == "__main__":
    run_base_pipeline()
