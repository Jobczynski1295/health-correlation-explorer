import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Health Correlation Explorer", layout="wide")
st.title("Health Correlation Explorer")
st.caption("CDC NHANES 2017–2018 • Adults age 20+ • Sample correlations, not national estimates")

@st.cache_data
def load_data():
    return pd.read_csv("nhanes_health.csv")

data = load_data()
numeric_columns = data.select_dtypes(include="number").columns.tolist()

st.sidebar.header("Filters")
sex_choice = st.sidebar.selectbox("Sex", ["All", "Female", "Male"])
minimum_age, maximum_age = int(data.age.min()), int(data.age.max())
age_range = st.sidebar.slider("Age range", minimum_age, maximum_age, (minimum_age, maximum_age))
method_label = st.sidebar.radio("Correlation method", ["Pearson", "Spearman"])
method = method_label.lower()

filtered = data[data["age"].between(*age_range)].copy()
if sex_choice != "All":
    filtered = filtered[filtered["sex"] == sex_choice].copy()

st.subheader("Data preview")
st.write("Each row represents one adult participant. The dataset includes demographic, body measurement, blood pressure, cholesterol, blood sugar, sleep and sedentary time measures.")
st.write(f"Participants after filtering: **{len(filtered):,}**")
st.dataframe(filtered, use_container_width=True)

st.subheader("Pairwise correlation")
col1, col2, col3 = st.columns(3)
with col1:
    x = st.selectbox("X variable", numeric_columns, index=numeric_columns.index("age"))
with col2:
    y = st.selectbox("Y variable", numeric_columns, index=numeric_columns.index("systolic_bp"))
with col3:
    color_by_bp = st.checkbox("Color by SBP ≥ 130", value=False)

pair = filtered[[x, y]].dropna()
# The count is based on participants with nonmissing measurements for both variables.
n = len(pair)
r = pair[x].corr(pair[y], method=method) if n >= 2 else float("nan")
st.metric("Correlation (r)", f"{r:.3f}" if pd.notna(r) else "N/A")
st.metric("Participants (n)", f"{n:,}")

if n >= 2:
    plot_data = filtered[[x, y, "systolic_bp"]].dropna(subset=[x, y]).copy()
    if color_by_bp:
        plot_data["BP category"] = plot_data["systolic_bp"].ge(130).map({True: "SBP ≥ 130", False: "SBP < 130"})
    fig, ax = plt.subplots(figsize=(8, 4.5))
    if color_by_bp:
        sns.scatterplot(data=plot_data, x=x, y=y, hue="BP category", alpha=0.55, ax=ax)
    else:
        sns.scatterplot(data=plot_data, x=x, y=y, alpha=0.55, ax=ax)
    # A linear trend line is a visual guide; the correlation method is controlled separately.
    if x != y and pair[x].nunique() > 1:
        sns.regplot(data=pair, x=x, y=y, scatter=False, ci=None, color="black", ax=ax)
    st.pyplot(fig)
    plt.close(fig)
else:
    st.info("Not enough complete pairs to calculate a correlation.")

st.subheader("Correlation heatmap")
selected = st.multiselect("Choose numeric variables", numeric_columns, default=numeric_columns[:6])
if len(selected) >= 2:
    matrix = filtered[selected].corr(method=method)
    # pandas correlation uses pairwise complete observations for each pair.
    pair_counts = filtered[selected].notna().astype(int).T.dot(filtered[selected].notna().astype(int))
    labels = matrix.copy().astype(object)
    for row in selected:
        for column in selected:
            value = matrix.loc[row, column]
            labels.loc[row, column] = f"{value:.2f}\nn={pair_counts.loc[row, column]}" if pd.notna(value) else "N/A"
    fig2, ax2 = plt.subplots(figsize=(max(7, len(selected) * 1.25), max(5, len(selected) * 0.95)))
    sns.heatmap(matrix, annot=labels, fmt="", cmap="coolwarm", vmin=-1, vmax=1, center=0, ax=ax2)
    st.pyplot(fig2)
    plt.close(fig2)
else:
    st.info("Select at least two numeric variables.")

st.caption("Correlations do not establish causation. A correlation near zero may still hide a curved relationship. Missing measurements are excluded pairwise; heatmap colors always span −1 to 1.")
