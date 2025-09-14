
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.utils import load_data, numeric_columns

st.title("🔁 Compare Two Drinks")

@st.cache_data
def get_df():
    return load_data("data/Nutrition_facts_for_Starbucks_Menu_1604_26.csv")

df = get_df()

# Build pickers
names = df['beverage'].dropna().unique().tolist() if 'beverage' in df else []
col1, col2 = st.columns(2)
with col1:
    d1 = st.selectbox("Drink A", names, index=0 if names else None)
with col2:
    d2 = st.selectbox("Drink B", names, index=1 if len(names)>1 else None)

if not names or d1 is None or d2 is None:
    st.warning("No beverages found.")
    st.stop()

row1 = df[df['beverage'] == d1].iloc[0]
row2 = df[df['beverage'] == d2].iloc[0]

# Side-by-side stats
st.subheader("Side-by-side")
cols = st.columns(2)
show = [c for c in ['category','prep','calories','sugar_g','fat_g','carbs_g','protein_g','caffeine_mg','sodium_mg'] if c in df.columns]
with cols[0]:
    st.markdown(f"**{d1}**")
    st.dataframe(pd.DataFrame(row1[show]).rename(columns={0:'value'}))
with cols[1]:
    st.markdown(f"**{d2}**")
    st.dataframe(pd.DataFrame(row2[show]).rename(columns={0:'value'}))

# Radar chart
st.subheader("Radar comparison")
radar_fields = [c for c in ['calories','sugar_g','fat_g','carbs_g','protein_g','caffeine_mg','sodium_mg'] if c in df.columns]
if radar_fields:
    def to_polar(r):
        return [float(r.get(k, 0) if pd.notna(r.get(k, np.nan)) else 0) for k in radar_fields]
    import numpy as np
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=to_polar(row1), theta=[f.replace('_',' ').title() for f in radar_fields], fill='toself', name=d1))
    fig.add_trace(go.Scatterpolar(r=to_polar(row2), theta=[f.replace('_',' ').title() for f in radar_fields], fill='toself', name=d2))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True, height=500)
    st.plotly_chart(fig, use_container_width=True)

# Delta bars
st.subheader("Difference (A - B)")
diff = pd.DataFrame({
    "metric": [f.replace('_',' ').title() for f in radar_fields],
    "delta": [float(row1[k] if pd.notna(row1.get(k, np.nan)) else 0) - float(row2[k] if pd.notna(row2.get(k, np.nan)) else 0) for k in radar_fields]
})
st.bar_chart(diff.set_index("metric"))
