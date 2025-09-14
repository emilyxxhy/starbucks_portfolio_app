
# Starbucks Drinks Nutrition — Data Science Portfolio App

An end-to-end project you can run in VS Code: data cleaning, EDA, interactive Streamlit dashboard, a **Compare Two Drinks** tool, a **Healthier Alternative** recommender, plus **clustering** and a simple **category prediction** model.

## 🚀 Quickstart

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

[This opens](https://starbucksportfolioapp-67oaqbtqc77lls7gz2fvjy.streamlit.app/EDA)

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

