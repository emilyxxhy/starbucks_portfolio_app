import streamlit as st
import pandas as pd
import altair as alt
from src.utils import load_data

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Starbucks Nutrition Analytics",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. DATA LOADING & PREPARATION ---
@st.cache_data
def get_data():
    return load_data("data/Nutrition_facts_for_Starbucks_Menu_1604_26.csv")

try:
    df = get_data()
except Exception as e:
    st.error(f"⚠️ System Error: Unable to load data. Details: {e}")
    st.stop()

# --- 3. SIDEBAR: CONTROL PANEL ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/d/d3/Starbucks_Corporation_Logo_2011.svg/1200px-Starbucks_Corporation_Logo_2011.svg.png", width=80)
    
    st.header("🎛️ Analysis Controls")
    
    # Filter Logic
    if 'category' in df.columns:
        all_categories = df['category'].unique().tolist()
        st.caption("Select product categories to analyze:")
        selected_cats = st.multiselect(
            "Category Filter", 
            all_categories, 
            default=all_categories[:2] if len(all_categories) > 2 else all_categories,
            label_visibility="collapsed"
        )
    else:
        selected_cats = []
        st.warning("Category column missing.")

    st.markdown("---")
    
    # Data Dictionary (Context for HR/Users)
    with st.expander("📖 Data Dictionary"):
        st.markdown("""
        - **Calories:** Energy content (kcal).
        - **Sugar (g):** Total sugar content per serving.
        - **Caffeine (mg):** Stimulant content.
        - **Prep:** Type of milk or preparation method.
        """)
    
    st.info("💡 **Pro Tip:** Use the tabs on the main page to switch between Insights and Rankings.")
    st.caption("v2.2 | Portfolio Project")

# Apply Filter
if selected_cats and 'category' in df.columns:
    df_filtered = df[df['category'].isin(selected_cats)]
else:
    df_filtered = df

# --- 4. MAIN DASHBOARD ---

# Header: Value Proposition
st.title("☕ Starbucks Nutrition Insights")
st.markdown("""
> **Executive Summary:** This dashboard empowers customers to make informed health decisions by analyzing the nutritional trade-offs in Starbucks beverages. 
> We focus on the correlation between **Sugar**, **Calories**, and **Caffeine**.
""")

st.divider()

# --- SECTION A: REAL-WORLD CONTEXT (BENCHMARKS) ---
st.subheader("1. Health Impact Overview")

if not df_filtered.empty:
    cols = st.columns(4)
    
    # Calculate Metrics safely
    avg_sugar = df_filtered['sugar_g'].mean() if 'sugar_g' in df_filtered.columns else 0
    avg_cal = df_filtered['calories'].mean() if 'calories' in df_filtered.columns else 0
    max_caffeine = df_filtered['caffeine_mg'].max() if 'caffeine_mg' in df_filtered.columns else 0
    total_items = len(df_filtered)

    # FDA Daily Limit Context (Assuming ~50g sugar/day for reference)
    sugar_delta = f"{avg_sugar/50*100:.0f}% of Daily Limit"

    with cols[0]:
        st.metric("Total Items Analyzed", total_items, help="Number of drinks in current selection")
    with cols[1]:
        st.metric("Avg. Calories", f"{avg_cal:.0f} kcal", delta="Energy", delta_color="off")
    with cols[2]:
        st.metric("Avg. Sugar", f"{avg_sugar:.1f} g", delta=sugar_delta, delta_color="inverse")
    with cols[3]:
        st.metric("Max Caffeine Kick", f"{max_caffeine:.0f} mg", help="Highest caffeine content found")

    # Narrative Insight
    if avg_sugar > 30:
        st.warning(f"⚠️ **Health Alert:** The selected categories average **{avg_sugar:.1f}g of sugar**, which is significant. The FDA recommends limiting added sugar to ~50g per day.")
    else:
        st.success(f"✅ **Health Check:** These categories average **{avg_sugar:.1f}g of sugar**, which is within a reasonable range for a treat.")

else:
    st.warning("Please select a category from the sidebar to begin analysis.")

st.divider()

# --- SECTION B: VISUAL ANALYSIS (WITH EXPLANATION) ---
st.subheader("2. The 'Sugar-Energy' Trap")
st.markdown("Analyze whether higher sugar content necessarily leads to higher calories.")

col_viz, col_explain = st.columns([3, 1.2])

with col_viz:
    if not df_filtered.empty and 'calories' in df_filtered.columns and 'sugar_g' in df_filtered.columns:
        # Dynamic Tooltips
        tooltips = ['beverage', 'calories', 'sugar_g', 'category']
        if 'caffeine_mg' in df_filtered.columns: tooltips.append('caffeine_mg')

        # Chart
        chart = (
            alt.Chart(df_filtered)
            .mark_circle(size=80, opacity=0.6, stroke='white', strokeWidth=1)
            .encode(
                x=alt.X("calories:Q", title="Calories (kcal)"),
                y=alt.Y("sugar_g:Q", title="Sugar Content (g)"),
                color=alt.Color("category:N", title="Category", legend=alt.Legend(orient="bottom")),
                tooltip=tooltips
            )
            .properties(
                height=400,
                title="Correlation Analysis: Calories vs. Sugar"
            )
            .interactive()
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Insufficient data to generate chart.")

with col_explain:
    st.markdown("#### 🧐 How to read this?")
    st.info("""
    - **X-Axis:** How much energy (Calories) the drink provides.
    - **Y-Axis:** How much Sugar is in the drink.
    - **Dots:** Each dot is a unique drink.
    """)
    
    st.markdown("#### 💡 Key Takeaway")
    st.markdown("""
    Most drinks follow a **linear trend**: as sugar increases, calories increase.
    
    *Look for dots in the **bottom-left** corner for healthier options.*
    """)

# --- SECTION C: ACTIONABLE LISTS (RANKINGS) ---
st.divider()
st.subheader("3. Top Contenders")
st.markdown("Identifies the outliers: The heaviest treats vs. the lightest options.")

# Tabs for better UI organization
tab_heavy, tab_light = st.tabs(["🔴 The 'Heavyweights'", "🟢 The 'Lightweights'"])

# --- HÀM ĐƯỢC SỬA ĐỂ CHỐNG LỖI MATPLOTLIB ---
def show_top_table(data, sort_col, asc, color_highlight):
    if sort_col in data.columns:
        cols = ['beverage', sort_col, 'category']
        # Add Prep if exists
        if 'prep' in data.columns: cols.insert(1, 'prep')
        
        display_df = data.sort_values(sort_col, ascending=asc).head(5)[cols]
        
        # Thử tô màu, nếu lỗi (do thiếu matplotlib) thì hiện bảng thường
        try:
            st.dataframe(
                display_df.style.background_gradient(subset=[sort_col], cmap=color_highlight),
                use_container_width=True,
                hide_index=True
            )
        except ImportError:
            # Fallback an toàn: Hiện bảng không màu nếu chưa cài matplotlib
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )
        except Exception as e:
            st.dataframe(display_df, use_container_width=True, hide_index=True)

with tab_heavy:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Highest Calorie Options**")
        st.caption("Drinks that might replace a full meal.")
        show_top_table(df_filtered, 'calories', False, 'Reds')
    with c2:
        st.markdown("**Highest Sugar Options**")
        st.caption("Drinks exceeding daily sugar recommendations.")
        show_top_table(df_filtered, 'sugar_g', False, 'Oranges')

with tab_light:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Lowest Calorie Options**")
        st.caption("Best for weight management.")
        show_top_table(df_filtered, 'calories', True, 'Greens')
    with c2:
        st.markdown("**Lowest Sugar Options**")
        st.caption("Best for blood sugar control.")
        show_top_table(df_filtered, 'sugar_g', True, 'Teals')

# --- 4. CALL TO ACTION (NAVIGATION) ---
st.divider()
st.markdown("### 🚀 Ready to explore further?")
col_nav1, col_nav2, col_nav3 = st.columns(3)

with col_nav1:
    st.info("**🔎 Want details?**\n\nGo to the **EDA Page** to see histograms and boxplots.")
with col_nav2:
    st.info("**⚖️ Can't decide?**\n\nUse the **Compare Page** to fight two drinks head-to-head.")
with col_nav3:
    st.info("**🤖 Need AI help?**\n\nAsk our **Recommender System** to pick a drink for you.")