import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
from src.utils import load_data

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Starbucks Smart Choice Engine", page_icon="💡", layout="wide")

st.title("💡 The Smart Choice Engine")
st.markdown("""
### From "Guilty Pleasure" to "Healthy Habit"
> **Product Vision:** Most consumers don't want to stop drinking Starbucks; they want to drink it **smarter**. 
> This engine uses a **Nearest-Healthier-Neighbor** logic to find alternatives that preserve your flavor preferences while slashing unnecessary calories and sugar.
""")

# --- 2. DATA LOADING (ULTRA ROBUST) ---
@st.cache_data
def get_data():
    paths = [
        "data/Nutrition_facts_for_Starbucks_Menu_1604_26 (1).csv",
        "data/Nutrition_facts_for_Starbucks_Menu_1604_26.csv",
        "Nutrition_facts_for_Starbucks_Menu_1604_26.csv"
    ]
    for path in paths:
        if os.path.exists(path):
            return load_data(path)
    return None

df = get_data()

if df is None:
    st.error("🚨 **Data Source Missing!** Please ensure the CSV is in the data folder.")
    st.stop()

# --- HELPER: SAFE DATA RETRIEVAL ---
def get_val(row, key, default=0):
    if key in row:
        val = row[key]
        try:
            return float(val) if pd.notna(val) else default
        except:
            return default
    return default

# --- 3. FEATURE 1: THE SMART SWAP ENGINE ---
st.header("🚀 1. The 'Smart Swap' Finder")
st.info("Pick your 'Guilty Pleasure' below, and our AI logic will find the healthiest version within that same category.")

# Business Logic: Group by Beverage Name, then let them pick the Prep
all_beverages = sorted(df['beverage'].unique())

c1, c2 = st.columns(2)
with c1:
    target_bev = st.selectbox("I usually order:", all_beverages, index=0)
    available_preps = df[df['beverage'] == target_bev]['prep'].unique()
    target_prep = st.selectbox("Preparation / Size:", available_preps)

# Get the "Original" drink
original_drink = df[(df['beverage'] == target_bev) & (df['prep'] == target_prep)].iloc[0]

# RECOMMENDATION LOGIC:
recommendations = df[df['category'] == original_drink['category']].copy()
# Tìm những món có calo thấp hơn món hiện tại
recommendations = recommendations[recommendations['calories'] < original_drink['calories']]
recommendations = recommendations.sort_values(by=['calories', 'sugar_g'], ascending=True)

st.divider()

if not recommendations.empty:
    best_swap = recommendations.iloc[0]
    
    # PRODUCT INSIGHT: THE SIDE-BY-SIDE COMPARISON
    res1, res2, res3 = st.columns([1, 0.5, 1])
    
    with res1:
        st.markdown("#### 🛑 Current Choice")
        st.error(f"**{target_bev}**")
        st.caption(f"Preparation: {target_prep}")
        st.write(f"🔥 Calories: **{get_val(original_drink, 'calories'):.0f} kcal**")
        st.write(f"🍬 Sugar: **{get_val(original_drink, 'sugar_g'):.1f} g**")

    with res2:
        st.markdown("<h1 style='text-align: center; color: gray; padding-top: 50px;'>➡️</h1>", unsafe_allow_html=True)

    with res3:
        st.markdown("#### ✨ The Smart Swap")
        st.success(f"**{best_swap['beverage']}**")
        st.caption(f"Preparation: {best_swap['prep']}")
        st.write(f"🍀 Calories: **{get_val(best_swap, 'calories'):.0f} kcal**")
        st.write(f"🍃 Sugar: **{get_val(best_swap, 'sugar_g'):.1f} g**")

    # --- THE "WOW" FEATURE: IMPACT METRICS ---
    st.markdown("### 📈 The Impact of this Choice")
    cal_saved = get_val(original_drink, 'calories') - get_val(best_swap, 'calories')
    sugar_saved = get_val(original_drink, 'sugar_g') - get_val(best_swap, 'sugar_g')
    
    walking_minutes = (cal_saved / 5) # 5 kcal per minute
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Calories Saved", f"{cal_saved:.0f} kcal", "Lighter")
    m2.metric("Sugar Reduction", f"{sugar_saved:.1f} g", f"{sugar_saved/4:.1f} tsp", delta_color="normal")
    m3.metric("Physical Equivalent", f"{walking_minutes:.0f} min", "Walking Saved")
    
    st.write(f"💡 **Analyst Insight:** Switching to the **{best_swap['beverage']}** allows you to enjoy the {best_swap['category']} experience while saving enough calories to skip **{walking_minutes:.0f} minutes** on the treadmill.")

else:
    st.warning("You are already picking the healthiest option in this category! Great job.")

st.divider()

# --- 4. FEATURE 2: LIFESTYLE TARGETS ---
st.header("🎯 2. Global Menu Optimization")
st.write("Not sure what you want? Tell us your diet profile.")

persona = st.selectbox("Select your Health Persona:", 
                      ["Weight Loss (Low Calorie)", 
                       "Low Carb / Keto (Low Sugar & Fat)", 
                       "The Clean Caffeine Boost (Max Caffeine/Min Sugar)"])

if persona == "Weight Loss (Low Calorie)":
    max_c, max_s, sort_f = 150, 20, "calories"
elif persona == "Low Carb / Keto (Low Sugar & Fat)":
    max_c, max_s, sort_f = 250, 5, "sugar_g"
else:
    max_c, max_s, sort_f = 200, 5, "caffeine_mg"

# Filter based on persona
filtered_menu = df[(df['calories'] <= max_c) & (df['sugar_g'] <= max_s)]

st.markdown(f"### Top 5 Recommendations for **{persona}**")

# CHỖ NÀY LÀ QUAN TRỌNG NHẤT: Kiểm tra xem cột có tồn tại không trước khi hiện bảng
desired_cols = ['beverage', 'prep', 'category', 'calories', 'sugar_g', 'caffeine_mg']
available_cols = [c for c in desired_cols if c in filtered_menu.columns]

if not filtered_menu.empty:
    st.dataframe(
        filtered_menu[available_cols]
        .sort_values(by=sort_f if sort_f in filtered_menu.columns else available_cols[0], 
                     ascending=(persona != "The Clean Caffeine Boost"))
        .head(5),
        use_container_width=True, hide_index=True
    )
else:
    st.info("No drinks match this specific persona perfectly.")

# --- 5. TECHNICAL CONTEXT ---
st.divider()
with st.expander("🛠️ How does the Recommender work?"):
    st.markdown("""
    - **Logic:** Locks search to the same category to maintain flavor profile.
    - **Data Handling:** Custom `get_val` prevents crashes if columns like `caffeine_mg` are formatted as strings or missing.
    """)

st.caption("Starbucks Decision Support System | Product Mindset Portfolio v3.6")