
import streamlit as st
import altair as alt
import pandas as pd
from src.utils import load_data, numeric_columns

st.title("📊 Distributions & EDA")

@st.cache_data
def get_df():
    return load_data("data/Nutrition_facts_for_Starbucks_Menu_1604_26.csv")

df = get_df()

st.subheader("Filters")
cat = st.multiselect("Category", sorted(df['category'].dropna().unique()) if 'category' in df else [])
prep = st.multiselect("Preparation", sorted(df['prep'].dropna().unique()) if 'prep' in df else [])
df_f = df.copy()
if cat and 'category' in df_f: df_f = df_f[df_f['category'].isin(cat)]
if prep and 'prep' in df_f: df_f = df_f[df_f['prep'].isin(prep)]

# Distributions
st.markdown("### Distributions")
cols = st.columns(3)
num_cols = [c for c in ['calories','sugar_g','caffeine_mg'] if c in df_f.columns]
for i, c in enumerate(num_cols):
    with cols[i % 3]:
        chart = (
            alt.Chart(df_f.dropna(subset=[c]))
            .mark_bar()
            .encode(x=alt.X(c, bin=alt.Bin(maxbins=30)), y='count()', tooltip=[c,'count()'])
            .properties(height=250, title=c.replace('_',' ').title())
        )
        st.altair_chart(chart, use_container_width=True)

# Top caffeinated
st.markdown("### Top 10 Most Caffeinated Drinks")
if 'caffeine_mg' in df_f:
    topc = df_f.sort_values('caffeine_mg', ascending=False).head(10)
    st.dataframe(topc[[c for c in ['beverage','prep','category','caffeine_mg','calories','sugar_g'] if c in topc.columns]])

# Treemap of categories
st.markdown("### Treemap of Menu Categories")
import plotly.express as px
if 'category' in df_f and 'calories' in df_f:
    treemap = px.treemap(df_f, path=['category','prep'] if 'prep' in df_f else ['category'], values='calories', hover_data=['beverage'] if 'beverage' in df_f else None)
    st.plotly_chart(treemap, use_container_width=True)
