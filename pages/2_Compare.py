import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import altair as alt
import os
from src.utils import load_data

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Compare Drinks - Decision Support", page_icon="🆚", layout="wide")

# Starbucks Green Styling
st.markdown("""
    <style>
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; border-left: 5px solid #00704A; }
    </style>
    """, unsafe_allow_html=True)

st.title("🆚 Beverage Head-to-Head Comparison")
st.markdown("""
> **Business Insight:** Decisions are rarely about absolute numbers; they are about **trade-offs**. 
> This tool identifies "Smart Swaps" to help customers optimize their daily intake.
""")

# --- 2. DATA LOADING (ROBUST) ---
@st.cache_data
def get_data():
    paths = ["data/Nutrition_facts_for_Starbucks_Menu_1604_26.csv", "Nutrition_facts_for_Starbucks_Menu_1604_26.csv"]
    for path in paths:
        if os.path.exists(path):
            return load_data(path)
    return None

df = get_data()

if df is None:
    st.error("🚨 **File CSV không tìm thấy!** Hãy kiểm tra lại thư mục data.")
    st.stop()

# --- HELPER FUNCTION: LẤY DỮ LIỆU AN TOÀN (CHỐNG BUG) ---
def get_val(row, key):
    """Lấy giá trị từ row, thử cả chữ thường và chữ hoa, nếu không có trả về 0"""
    # Thử các biến thể của key
    for k in [key, key.lower(), key.capitalize(), key.replace('_', ' ')]:
        if k in row:
            val = row[k]
            try:
                return float(val) if pd.notna(val) else 0.0
            except:
                return 0.0
    return 0.0

# --- 3. SELECTION LOGIC ---
# Ghép Beverage + Prep để tạo option duy nhất
df['full_name'] = df['beverage'].astype(str) + " (" + df['prep'].astype(str) + ")"
options = sorted(df['full_name'].unique().tolist())

st.subheader("1. Select Beverages to Compare")
col_sel1, col_sel2 = st.columns(2)

with col_sel1:
    st.markdown("### 🥤 Option A (Baseline)")
    choice_a = st.selectbox("Search and select drink", options, key="a_choice")
    row_a = df[df['full_name'] == choice_a].iloc[0]

with col_sel2:
    st.markdown("### 🍹 Option B (Alternative)")
    choice_b = st.selectbox("Compare with", options, index=min(1, len(options)-1), key="b_choice")
    row_b = df[df['full_name'] == choice_b].iloc[0]

st.divider()

# --- 4. KEY METRIC COMPARISON ---
st.subheader("2. Executive Summary: The Trade-off")

m1, m2, m3, m4 = st.columns(4)

# Lấy các chỉ số quan trọng một cách an toàn
cal_a, cal_b = get_val(row_a, 'calories'), get_val(row_b, 'calories')
sug_a, sug_b = get_val(row_a, 'sugar_g'), get_val(row_b, 'sugar_g')
caf_a, caf_b = get_val(row_a, 'caffeine_mg'), get_val(row_b, 'caffeine_mg')

with m1:
    d_cal = cal_a - cal_b
    st.metric("Calories", f"{cal_a:.0f} kcal", delta=f"{-d_cal:.0f} vs B", delta_color="normal" if d_cal < 0 else "inverse")

with m2:
    d_sugar = sug_a - sug_b
    st.metric("Sugar", f"{sug_a:.1f} g", delta=f"{-d_sugar:.1f} vs B", delta_color="normal" if d_sugar < 0 else "inverse")

with m3:
    d_caff = caf_a - caf_b
    st.metric("Caffeine", f"{caf_a:.0f} mg", delta=f"{d_caff:.0f} vs B")

with m4:
    if cal_a < cal_b - 50:
        st.success("✅ Option A is a 'Light' choice")
    elif cal_a > cal_b + 50:
        st.warning("⚠️ Option A is an 'Indulgent' choice")
    else:
        st.info("⚖️ Similar Energy Profile")

# --- 5. VISUAL ANALYSIS ---
st.divider()
col_radar, col_bar = st.columns([1.5, 1])

# Danh sách metrics để vẽ chart (Chỉ lấy những gì tồn tại)
potential_metrics = ['calories', 'sugar_g', 'fat_g', 'protein_g', 'carbs_g']
existing_metrics = [m for m in potential_metrics if any(k in df.columns for k in [m, m.capitalize()])]

with col_radar:
    st.markdown("**Nutritional Footprint**")
    fig = go.Figure()
    
    def get_radar_values(row):
        vals = [get_val(row, m) for m in existing_metrics]
        # Scale calories để chart đẹp
        if 'calories' in existing_metrics:
            idx = existing_metrics.index('calories')
            vals[idx] = vals[idx] / 5 
        return vals

    for row, name, color in [(row_a, choice_a, '#00704A'), (row_b, choice_b, '#ef553b')]:
        v = get_radar_values(row)
        v.append(v[0]) # Đóng vòng radar
        l = [m.replace('_', ' ').title() for m in existing_metrics]
        if 'Calories' in l: l[l.index('Calories')] = 'Calories (1/5)'
        l.append(l[0])
        
        fig.add_trace(go.Scatterpolar(r=v, theta=l, fill='toself', name=name[:20], line_color=color))

    fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True, height=450)
    st.plotly_chart(fig, use_container_width=True)

with col_bar:
    st.markdown("**Comparison Delta (A vs B)**")
    
    diff_values = [get_val(row_a, m) - get_val(row_b, m) for m in existing_metrics]
    diff_df = pd.DataFrame({"Metric": [m.replace('_', ' ').title() for m in existing_metrics], "Diff": diff_values})
    
    bar = alt.Chart(diff_df).mark_bar().encode(
        x=alt.X("Diff:Q", title="Value Difference (Positive = A is higher)"),
        y=alt.Y("Metric:N", sort="-x"),
        color=alt.condition(alt.datum.Diff > 0, alt.value("#ef553b"), alt.value("#636efa")),
        tooltip=["Metric", "Diff"]
    ).properties(height=350)
    st.altair_chart(bar, use_container_width=True)

# --- 6. SMART SWAP SUMMARY ---
st.divider()
st.subheader("📝 Smart Swap Summary")

s_diff = sug_a - sug_b
c_diff = cal_a - cal_b

recs = []
if s_diff > 10: recs.append(f"❌ **Sugar Alert:** '{choice_a}' has much more sugar (+{s_diff:.1f}g).")
if c_diff < -80: recs.append(f"🟢 **Calorie Saver:** Switching to '{choice_a}' saves you {abs(c_diff):.0f} kcal.")
if caf_a > caf_b + 40: recs.append(f"⚡ **Buzz Factor:** '{choice_a}' is more caffeinated.")

if not recs:
    st.write("These drinks are nutritionally similar. Choose based on your taste preference!")
for r in recs:
    st.write(r)

st.caption("Starbucks Portfolio v3.3 | Data Science Project")