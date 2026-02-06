
# Starbucks Drinks Nutrition — Data Science Portfolio App

An end-to-end project you can run in VS Code: data cleaning, EDA, interactive Streamlit dashboard, a **Compare Two Drinks** tool, a **Healthier Alternative** recommender, plus **clustering** and a simple **category prediction** model.

## 🚀 Quickstart
[![Open in Streamlit] https://starbucksportfolioapp-67oaqbtqc77lls7gz2fvjy.streamlit.app/
```bash
# 0) (macOS) Install Python 3 if needed
brew install python

# 1) Create & activate a venv
python3 -m venv .venv
source .venv/bin/activate

# 2) Install deps
pip install -r requirements.txt

# 3) Run the multi-page app
streamlit run streamlit_app.py
```

This opens `http://localhost:8501` with pages on the left sidebar.

## 📂 Repo Structure

```
starbucks_portfolio_app/
├─ streamlit_app.py                # Home + overview
├─ pages/
│  ├─ 1_EDA.py                     # Distributions + treemap + top caffeine
│  ├─ 2_Compare.py                 # Compare two drinks (radar + deltas)
│  ├─ 3_Recommender.py             # Goals + Healthier alternative finder
│  └─ 4_Models.py                  # Clustering + category prediction
├─ src/
│  └─ utils.py                     # Shared data loading & helpers
├─ data/
│  └─ Nutrition_facts_for_Starbucks_Menu_1604_26.csv
├─ notebooks/
│  └─ 01_quick_audit.ipynb         # EDA skeleton (optional)
├─ requirements.txt
└─ README.md
```

## ✨ Highlights

- **Compare Two Drinks**: side-by-side stats, radar chart, and delta bars.
- **Healthier Alternative**: suggest a similar, lower-cal/sugar drink within same category/prep when possible.
- **Visuals**: distributions, bubble chart, treemap, top caffeine table.
- **Clustering**: KMeans to group drinks (light/medium/heavy-style).
- **Prediction**: RandomForest to predict `category` from nutrition.
- **Clean code**: shared `src/utils.py`, caching, and tidy page layout.

## 🧪 Tips for Portfolio Polish

- Add screenshots to the README.
- Push to GitHub with a short project story (Goal → Data → Methods → Insights → Next Steps).
- Deploy on Streamlit Community Cloud or Hugging Face Spaces and link it in your resume.

## 🛠️ Common macOS Fix

If you see `zsh: command not found: python`, use `python3` and `pip3` (and Homebrew above).
```
📖 Project Story
❓ Problem

Starbucks offers hundreds of drinks, but customers often underestimate the nutritional trade-offs — especially sugar and calories.
For example, one Frappuccino can exceed the daily recommended sugar intake in a single serving.
I wanted to build an end-to-end data science project that uncovers these insights, makes them interactive, and even recommends healthier alternatives.

🛠️ Approach

Data Cleaning & Understanding

Normalized messy nutrition column names.

Checked for missing values and converted nutrition fields to numeric.

Grouped drinks by categories (Frappuccino, Latte, Tea, Refresher, etc.).

Exploratory Data Analysis (EDA)

Visualized distributions of calories, sugar, and caffeine.

Correlation heatmap between nutrition metrics (sugar, fat, caffeine, etc.).

Identified "sugar bombs" — drinks with highest sugar per serving.

Scatterplot of calories vs caffeine (are high-energy drinks also calorie-heavy?).

Interactive Dashboard (Streamlit)

Sidebar filters (category, prep, calories, sugar, caffeine).

Goal-based filtering (e.g., under 200 calories, under 20g sugar).

KPIs for quick summary stats.

Side-by-side Compare Two Drinks tool with radar + bar charts.

Healthier Alternative Finder — suggests lighter swaps.

Machine Learning Add-ons

Clustering: grouped drinks into "light", "medium", "heavy" categories based on nutrition.

Prediction: trained a RandomForest model to predict drink category from nutrition profile.

Feature importance analysis showed calories and sugar as top predictors.

💡 Key Insights

Hidden Sugar: >40% of drinks exceed WHO’s daily sugar guideline in one serving.

Caffeine Trade-offs: Some high-caffeine drinks are surprisingly low in calories (e.g., cold brews).

Healthier Swaps: Instead of Java Chip Frappuccino (440 cal, 60g sugar),
the app recommends Iced Americano (15 cal, 0g sugar).

🚀 Impact

This project demonstrates:

End-to-end data science workflow: cleaning → EDA → dashboard → ML.

Business storytelling: framing data in terms of customer health and choices.

Engineering skills: building a multi-page Streamlit app with reusable src/utils.py.

🔮 Next Steps

Add drink pricing data to explore “cost per calorie”.

Build a recommendation system for “similar but healthier” drinks.

Deploy on Streamlit Community Cloud so anyone can interact with it.

Export automated PDF insights for non-technical users.

🧪 Tips for Portfolio Polish

Add screenshots to the README.

Push to GitHub with a short project story (Goal → Data → Methods → Insights → Next Steps).

Deploy on Streamlit Community Cloud or Hugging Face Spaces and link it in your resume.
