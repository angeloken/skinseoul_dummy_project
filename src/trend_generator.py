import pandas as pd
import numpy as np

def create_sales_data(df, months=6):
    rows = []
    months_list = pd.date_range("2025-10-01", periods=months, freq="M")
    for _, row in df.iterrows():
        for m in months_list:
            rows.append({
                "product_name": row["product_name"],
                "category": row["category"],
                "month": m.strftime("%Y-%m"),
                "sales": np.random.randint(10, 300)
            })
    sales_df = pd.DataFrame(rows)
    sales_df.to_csv("data/sales_trends.csv", index=False)
    print("Generated sales_trends.csv")
