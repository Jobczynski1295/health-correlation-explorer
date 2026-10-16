# Health Correlation Explorer — Build plan

1. Load `nhanes_health.csv` and identify numeric columns; exclude the text `sex` column from correlations.
2. Add sidebar sex and age-range filters, and a Pearson/Spearman selector. Apply filters to every view.
3. Show a short data description and filtered participant table.
4. Add two numeric-variable selectors, pairwise correlation r and complete-pair count n, and a scatter plot with a trend line and optional SBP ≥ 130 color groups.
5. Add a user-selectable correlation heatmap. Annotate coefficients and pairwise n, and fix its colors at −1 and 1.
6. Verify the required checks independently in pandas, test the app, then deploy to Streamlit Community Cloud.

Run locally with `python -m streamlit run app.py` after installing `requirements.txt`. The assignment also provides `uv run --with streamlit,pandas,seaborn,scipy streamlit run app.py`.
