# SkinSeoul Dummy AI E-Commerce Project

This is a simple demo showing how AI can classify skincare products automatically.

## Steps to run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY=sk-yourkey
   ```

3. Run the pipeline:
   ```bash
   python -m src.pipeline
   ```

4. Check the outputs:
   - `data/categorized_products.csv`
   - `data/sales_trends.csv`

3. Run the app ins streamlit:
   ```bash
   streamlit run app.py
   ```
