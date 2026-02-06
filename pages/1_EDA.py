import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import re

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Executive Portfolio Audit | Starbucks", page_icon="📊", layout="wide")

# Starbucks Brand Identity CSS (High-End Corporate Look)
st.markdown("""
    <style>
    .report-box { padding: 25px; border-radius: 15px; background-color: #f0f4f2; border-left: 8px solid #00704A; margin-bottom: 25px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); }
    .insight-header { color: #00704A; font-weight: bold; font-size: 1.3em; margin-bottom: 10px; display: block; }
    .stMetric { border: 1px solid #e0e0e0; padding: 15px; border-radius: 12px; background-color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Strategic Portfolio Intelligence Dashboard")
st.markdown("### 🧭 Data-Driven Menu Optimization & Health Audit")

# --- 2. THE BULLETPROOF DATA ENGINE ---
@st.cache_data
def get_ultimate_data():
    # Tìm file đúng nghĩa đen
    paths = ["Nutrition_facts_for_Starbucks_Menu_1604_26 (1).csv", 
             "data/Nutrition_facts_for_Starbucks_Menu_1604_26 (1).csv",
             "data/Nutrition_facts_for_Starbucks_Menu_1604_26.csv"]
    
    df = None
    for path in paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            break
    
    if df is None: return None

    # --- CHỐNG BUG TÊN CỘT (THE CLEANER) ---
    def clean_col(name):
        c = str(name).lower().strip()
        c = re.sub(r'[^a-z0-9]+', '_', c).strip('_')
        # Mapping các lỗi đặt tên đặc thù của Starbucks CSV
        if 'sugar' in c: return 'sugar_g'
        if 'caff' in c: return 'caffeine_mg'
        if 'fat' in c and 'total' in c: return 'fat_g'
        if 'calor' in c: return 'calories'
        if 'bev' in c and 'cat' in c: return 'category'
        if 'prep' in c: return 'prep'
        if 'protein' in c: return 'protein_g'
        if 'sod' in c: return 'sodium_mg'
        return c

    df.columns = [clean_col(c) for c in df.columns]

    # --- CHỐNG BUG DỮ LIỆU (THE CONVERTER) ---
    essential_cols = ['calories', 'sugar_g', 'fat_g', 'protein_g', 'caffeine_mg', 'sodium_mg']
    for col in essential_cols:
        if col in df.columns:
            # Xử lý các ô như "Varies" hoặc "N/A"
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        else:
            df[col] = 0.0 # Tạo cột giả nếu thiếu để không sập app

    # --- STRATEGIC FEATURES ---
    # 1. Health Tiers
    df['health_tier'] = df.apply(lambda r: '🔴 Indulgent' if r['calories'] > 350 or r['sugar_g'] > 45 
                                 else ('🟡 Moderate' if r['calories'] > 180 or r['sugar_g'] > 20 else '🟢 Optimized'), axis=1)
    
    # 2. Functional Efficiency
    df['efficiency_index'] = df['caffeine_mg'] / (df['calories'] + 1)
    
    # 3. Nutrient Density (Vitamins/Minerals)
    dv_cols = [c for c in df.columns if 'dv' in c]
    if dv_cols:
        for c in dv_cols: df[c] = pd.to_numeric(df[c].astype(str).str.replace('%',''), errors='coerce').fillna(0)
        df['nutrient_score'] = df[dv_cols].sum(axis=1)
    else: df['nutrient_score'] = 0

    return df

df = get_ultimate_data()

if df is None:
    st.error("🚨 Critical Error: Master Dataset not found. Please ensure the CSV is in the root or /data folder.")
    st.stop()

# --- 3. SIDEBAR CONTROLS ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/d/d3/Starbucks_Corporation_Logo_2011.svg", width=80)
    st.header("🎛️ Analysis Controls")
    
    all_cats = sorted(df['category'].unique())
    selected_cats = st.multiselect("Select Market Segments:", all_cats, default=all_cats[:5])
    
    tier_filter = st.multiselect("Health Tier Filter:", df['health_tier'].unique(), default=df['health_tier'].unique())

df_f = df[(df['category'].isin(selected_cats)) & (df['health_tier'].isin(tier_filter))]

# --- 4. EXECUTIVE KPIs ---
st.header("🎯 1. Portfolio Executive Panorama")
if not df_f.empty:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("SKU Count", len(df_f))
    c2.metric("Avg. Calories", f"{df_f['calories'].mean():.0f} kcal")
    c3.metric("Sugar Liabilities", len(df_f[df_f['sugar_g'] > 40]), delta="High Risk", delta_color="inverse")
    
    cat_scores = df_f.groupby('category')['nutrient_score'].mean()
    leader = cat_scores.idxmax().split(' ')[0] if not cat_scores.empty else "N/A"
    c4.metric("Nutrient Dense Lead", leader)
else:
    st.warning("No data matches the selected filters. Please adjust the sidebar.")
    st.stop()

st.divider()

# --- 5. THE "DEEP DIVE" TABS ---
t1, t2, t3, t4, t5 = st.tabs([
    "📂 Portfolio Structure", "🧬 Nutritional DNA", "⚖️ Efficiency Lab", "🥛 Customization Impact", "🚨 Risk Audit"
])

# === TAB 1: STRUCTURE ===
with t1:
    st.subheader("Market Composition by Health Impact")
    col1, col2 = st.columns([2, 1])
    with col1:
        fig_sun = px.sunburst(df_f, path=['category', 'health_tier'], values='calories', color='health_tier',
                             color_discrete_map={'🔴 Indulgent': '#e74c3c', '🟡 Moderate': '#f1c40f', '🟢 Optimized': '#27ae60'},
                             title="Caloric Contribution by Segment")
        st.plotly_chart(fig_sun, use_container_width=True)
    with col2:
        st.markdown("<div class='report-box'><span class='insight-header'>💡 Business Insight</span>"
                    "The largest segments in red represent <b>Revenue vs. Health</b> trade-offs. "
                    "Optimizing the 'Moderate' (yellow) middle-ground is the key to market expansion.</div>", unsafe_allow_html=True)
        st.write("**Inventory by Tier:**")
        st.bar_chart(df_f['health_tier'].value_counts())

# === TAB 2: DNA ===
with t2:
    st.subheader("Nutritional Profile Comparison (Radar)")
    radar_cats = st.multiselect("Compare Nutritional DNA of Categories:", all_cats, default=all_cats[:2], key="r_eda")
    if radar_cats:
        m_list = ['calories', 'sugar_g', 'fat_g', 'protein_g', 'sodium_mg']
        m_list = [m for m in m_list if m in df.columns]
        rdf = df[df['category'].isin(radar_cats)].groupby('category')[m_list].mean()
        max_v = df[m_list].max().replace(0, 1)
        
        fig_r = go.Figure()
        for cat in radar_cats:
            v = (rdf.loc[cat] / max_v).values.tolist()
            v.append(v[0])
            fig_r.add_trace(go.Scatterpolar(r=v, theta=[i.title() for i in m_list] + [m_list[0].title()], fill='toself', name=cat))
        
        fig_r.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), height=500)
        st.plotly_chart(fig_r, use_container_width=True)
        st.info("💡 Radar values are normalized to show relative intensity of nutrients.")

# === TAB 3: EFFICIENCY ===
with t3:
    st.subheader("Functional Efficiency: Caffeine vs. Calories")
    fig_q = px.scatter(df_f, x="calories", y="caffeine_mg", color="category", size="sugar_g", 
                       hover_name="beverage", title="The 'Clean Buzz' Quadrant Analysis")
    fig_q.add_vline(x=200, line_dash="dot", annotation_text="Low Calorie Cap")
    fig_q.add_hline(y=150, line_dash="dot", annotation_text="High Function Zone")
    st.plotly_chart(fig_q, use_container_width=True)
    st.success("✅ **Top Performer:** Drinks in the Top-Left are 'Efficiency Leaders' (High energy, low caloric cost).")

# === TAB 4: CUSTOMIZATION ===
with t4:
    st.subheader("The 'Milk' Lever: Customization Impact")
    if 'prep' in df_f.columns:
        fig_box = px.box(df_f, x="prep", y="calories", color="prep", title="Caloric Variance by Milk/Preparation")
        st.plotly_chart(fig_box, use_container_width=True)
        
        # Calculate impact
        try:
            whole_avg = df_f[df_f['prep'].str.contains('Whole', case=False, na=False)]['calories'].mean()
            nonfat_avg = df_f[df_f['prep'].str.contains('Nonfat', case=False, na=False)]['calories'].mean()
            st.markdown(f"📈 **Strategic Impact:** Switching to Nonfat saves an average of **{whole_avg-nonfat_avg:.0f} calories** per SKU.")
        except: pass

# === TAB 5: AUDIT ===
with t5:
    st.subheader("High-Liability Product Audit")
    st.error("**🚨 Top 10 Heaviest Indulgences (Sort by Calories)**")
    st.dataframe(df_f.nlargest(10, 'calories')[['beverage', 'prep', 'calories', 'sugar_g', 'fat_g']], use_container_width=True)
    
    st.divider()
    st.subheader("Nutrient Correlation Heatmap")
    num_df = df_f.select_dtypes(include=[np.number])
    if not num_df.empty:
        fig_heat = px.imshow(num_df.corr(), text_auto=".2f", color_continuous_scale='RdBu_r')
        st.plotly_chart(fig_heat, use_container_width=True)

# --- 6. CONCLUSION ---
st.divider()
st.subheader("📝 Analyst Conclusion")
col_c1, col_c2 = st.columns(2)
with col_c1:
    st.success("**Strategic Strength:** The menu offers excellent functional efficiency in the Espresso segment.")
with col_c2:
    st.error("**Risk Exposure:** High sugar dependency in Blended categories poses a brand health risk.")

st.caption(f"Starbucks Strategic Analytics v7.0 | {pd.Timestamp.now().strftime('%Y-%m-%d')} | English Standard")