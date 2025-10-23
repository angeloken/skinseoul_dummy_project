from src.data_utils import load_products, save_results
from src.categorizer import categorize_product
def run_pipeline():
    df = load_products("data/products.csv")
    categories = []
    confidences = []
    for _, row in df.iterrows():
        print(f"Processing {row['product_name']}...")
        cat, conf = categorize_product(row["product_name"], row["description"])
        categories.append(cat)
        confidences.append(conf)
    df["category"] = categories
    df["confidence"] = confidences
    save_results(df, "data/categorized_products.csv")
    print("Pipeline completed successfully!")

if __name__ == "__main__":
    run_pipeline()
