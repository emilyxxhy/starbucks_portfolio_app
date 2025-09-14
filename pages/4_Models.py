
import streamlit as st
import pandas as pd
import numpy as np
from src.utils import load_data, numeric_columns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import altair as alt

st.title("🧠 Models — Clustering & Category Prediction")

@st.cache_data
def get_df():
    return load_data("data/Nutrition_facts_for_Starbucks_Menu_1604_26.csv")

df = get_df()

num_cols = numeric_columns(df)
if len(num_cols) < 2:
    st.warning("Not enough numeric columns to model.")
    st.stop()

# Clustering
st.subheader("Clustering drinks into Light / Medium / Heavy")
k = st.slider("Number of clusters (k)", 3, 6, value=3)
X = df[num_cols].fillna(df[num_cols].median())
scaler = StandardScaler()
Xs = scaler.fit_transform(X)
kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
labels = kmeans.fit_predict(Xs)
dfc = df.copy()
dfc["cluster"] = labels

cmap = {i: f"Cluster {i}" for i in range(k)}
dfc["cluster_name"] = dfc["cluster"].map(cmap)

if {'calories','sugar_g'}.issubset(dfc.columns):
    chart = (
        alt.Chart(dfc)
        .mark_circle(size=70, opacity=0.7)
        .encode(
            x="calories:Q", y="sugar_g:Q",
            color="cluster_name:N",
            tooltip=[c for c in ['beverage','prep','category','calories','sugar_g','caffeine_mg','cluster_name'] if c in dfc.columns]
        ).properties(height=400, title="Clusters on Calories vs Sugar")
    )
    st.altair_chart(chart, use_container_width=True)

st.caption("Heuristic: lower calories/sugar → 'light'; higher → 'heavy'.")

# Category prediction
st.subheader("Predicting drink category from nutrition")
if 'category' in df:
    dfm = df.dropna(subset=['category']).copy()
    y = dfm['category']
    X = dfm[num_cols].fillna(dfm[num_cols].median())
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    clf = RandomForestClassifier(n_estimators=300, random_state=42)
    clf.fit(Xtr, ytr)
    yp = clf.predict(Xte)
    acc = accuracy_score(yte, yp)
    st.metric("Test Accuracy", f"{acc*100:.1f}%")
    st.text("Classification Report")
    st.code(classification_report(yte, yp))
    # Feature importances
    imp = pd.Series(clf.feature_importances_, index=X.columns).sort_values(ascending=False).head(10)
    imp_chart = alt.Chart(imp.reset_index().rename(columns={'index':'feature',0:'importance'})).mark_bar().encode(x='importance:Q', y=alt.Y('feature:N', sort='-x'))
    st.altair_chart(imp_chart, use_container_width=True)
else:
    st.info("Category column not found, skipping classifier.")
