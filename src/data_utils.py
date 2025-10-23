import pandas as pd

def load_products(path):
    try:
        df = pd.read_csv(path)
        print(f"Loaded {len(df)} products from {path}")
        return df
    except Exception as e:
        print("Error loading file:", e)
        return pd.DataFrame()

def save_results(df, path):
    df.to_csv(path, index=False)
    print(f"Saved results to {path}")
