
import streamlit as st
from src.utils import load_data, numeric_columns
import pandas as pd
import altair as alt

st.set_page_config(page_title="Starbucks Nutrition — Portfolio App", layout="wide")

st.title("☕ Starbucks Drinks Nutrition — Portfolio App")
st.caption("Data source: Starbucks menu nutrition CSV (bundled). Use the pages on the left to explore.")

@st.cache_data
def get_df():
    return load_data("data/Nutrition_facts_for_Starbucks_Menu_1604_26.csv")

df = get_df()

# KPIs
st.subheader("Dashboard Overview")
k1,k2,k3,k4 = st.columns(4)
with k1: st.metric("Total Drinks", len(df))
with k2: st.metric("Avg Calories", f"{df['calories'].mean():.1f}" if 'calories' in df else "—")
with k3: st.metric("Median Sugar (g)", f"{df['sugar_g'].median():.1f}" if 'sugar_g' in df else "—")
with k4: st.metric("Max Caffeine (mg)", f"{df['caffeine_mg'].max():.0f}" if 'caffeine_mg' in df else "—")

# Quick visual: Sugar vs Calories bubble by category
if {'calories','sugar_g'}.issubset(df.columns):
    chart = (
        alt.Chart(df)
        .mark_circle(opacity=0.6)
        .encode(
            x=alt.X("calories:Q"),
            y=alt.Y("sugar_g:Q"),
            size=alt.Size("caffeine_mg:Q", title="Caffeine (mg)", scale=alt.Scale(range=[10,800])) if 'caffeine_mg' in df else alt.value(60),
            color=alt.Color("category:N") if 'category' in df else alt.value("steelblue"),
            tooltip=[c for c in ['beverage','prep','category','calories','sugar_g','caffeine_mg'] if c in df.columns]
        ).properties(height=380, title="Sugar vs. Calories (size=Caffeine)")
    )
    st.altair_chart(chart, use_container_width=True)

st.info("Explore more in pages: **Distributions & EDA**, **Compare Drinks**, **Recommender**, **Models (Clustering & Prediction)**.")
