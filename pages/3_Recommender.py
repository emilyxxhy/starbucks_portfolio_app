
import streamlit as st
import pandas as pd
import numpy as np
from src.utils import load_data, goal_filter, healthier_alternative

st.title("💡 Recommender & Healthier Alternatives")

@st.cache_data
def get_df():
    return load_data("data/Nutrition_facts_for_Starbucks_Menu_1604_26.csv")

df = get_df()

st.subheader("Your Goals")
u_cal = st.number_input("Max calories", min_value=0, value=200, step=10)
u_sugar = st.number_input("Max sugar (g)", min_value=0, value=20, step=1)
u_fat = st.number_input("Max total fat (g)", min_value=0, value=10, step=1)

df_g = goal_filter(df, u_cal, u_sugar, u_fat)
st.markdown(f"**{len(df_g)}** drinks match your goals.")
show_cols = [c for c in ['beverage','prep','category','calories','sugar_g','fat_g','caffeine_mg','protein_g'] if c in df_g.columns]
st.dataframe(df_g[show_cols].sort_values(['calories','sugar_g'], ascending=[True, True]).head(20))

st.divider()
st.subheader("Healthier Alternative Finder")
if 'beverage' in df:
    pick = st.selectbox("Pick a drink to lighten", sorted(df['beverage'].dropna().unique().tolist()))
    row = df[df['beverage'] == pick].iloc[0]
    alt_df = healthier_alternative(df, row)
    st.markdown("**Original**")
    st.dataframe(pd.DataFrame(row[show_cols]).rename(columns={0:'value'}))
    if alt_df.empty:
        st.info("No lighter alternative found in similar group—try adjusting goals or pick another drink.")
    else:
        st.markdown("**Try this instead:**")
        st.dataframe(alt_df[show_cols])
