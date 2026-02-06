# Starbucks Drinks Nutrition — Data Science Portfolio App

An end-to-end data science project transforming raw nutritional data into actionable consumer insights. This multi-page Streamlit application features advanced EDA, a beverage comparison engine, a "Smart Swap" recommender, and machine learning models for product segmentation and category prediction.

---

## 🎯 Overview

Starbucks offers hundreds of beverage configurations, but customers often underestimate the nutritional trade-offs—particularly regarding sugar, calories, and caffeine efficiency. One Frappuccino® can exceed the WHO’s daily recommended sugar intake in a single serving.

This project uncovers these insights through an interactive dashboard, framing complex data in terms of customer health and daily choices.

### 📖 Project Story

* **The Problem:** Navigating high-calorie "guilty pleasures" vs. "healthy habits" without losing the Starbucks experience.
* **The Approach:** - **Cleaning:** Normalizing messy column names (e.g., `Sugars..g.`) and handling "Varies" caffeine values.
* **EDA:** Multi-dimensional analysis using Sunburst charts, Radar profiling, and Quadrant Analysis.
* **Engineering:** Building a "Nearest-Healthier-Neighbor" recommender lock-stepped by product category.
* **ML:** Unsupervised Clustering (KMeans) to segment the menu and Supervised Classification (KNN) to predict beverage "DNA".



---

## 🏗️ Repo Structure

```text
starbucks_portfolio_app/
├─ streamlit_app.py           # Dashboard Home + Executive Summary
├─ pages/
│  ├─ 1_EDA.py                # Deep-Dive Portfolio Analysis (Sunburst, Radar, Heatmaps)
│  ├─ 2_Compare.py            # Head-to-Head Comparison (Radar + Delta metrics)
│  ├─ 3_Recommender.py        # "Smart Swap" Engine + Lifestyle Personas
│  └─ 4_Models.py             # K-Means Clustering + KNN Category Prediction
├─ src/
│  └─ utils.py                # Reusable data loading, cleaning & logic helpers
├─ data/
│  └─ Nutrition_facts_for_Starbucks_Menu_1604_26.csv
├─ requirements.txt           # Dependency management
└─ README.md                  # Project documentation

```

---

## ✨ Features & Highlights

### 📊 Strategic EDA (Page 1)

* **Portfolio Architecture:** Sunburst visualization of calorie contribution by category.
* **Nutritional DNA:** Radar charts comparing the "blueprint" of different beverage verticals (e.g., Espresso vs. Frappuccino).
* **Efficiency Lab:** Identifying "Clean Buzz" leaders—high caffeine for low caloric cost.

### 🆚 Head-to-Head Comparison (Page 2)

* **Decision Support:** Side-by-side stats for any two drinks.
* **Smart Swaps:** Visualizes the "trade-off" (e.g., choosing Option A saves 150 calories but loses 20mg of caffeine).
* **Analyst Recommendations:** Automated text summaries based on nutritional deltas.

### 💡 Smart Choice Engine (Page 3)

* **Guilty Pleasure Transformer:** Enter your "usual" order to find a lighter version in the same category.
* **Relatability Metrics:** Translates calorie savings into "Walking Minutes" (e.g., swapping saves 40 mins on the treadmill).
* **Lifestyle Targets:** Quick-filters for Keto, Low Calorie, or High Caffeine personas.

### 🧠 Predictive Analytics (Page 4)

* **Market Segmentation:** K-Means clustering to group drinks into "Light", "Standard", and "Indulgent" families.
* **Category DNA Prediction:** A K-Nearest Neighbors model that predicts the drink category based solely on nutrition.

---

## 🚀 Quick Start

### Local Setup

1. **Clone the Repository**
```bash
git clone <your-repo-url>
cd starbucks_portfolio_app

```


2. **Create and Activate Virtual Environment**
```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate  # Windows

```


3. **Install Dependencies**
```bash
pip install -r requirements.txt

```


4. **Run the App**
```bash
streamlit run streamlit_app.py

```



---

## 📈 Data Schema

The dataset includes 242 Starbucks beverages with the following key attributes:

| Column | Type | Description |
| --- | --- | --- |
| `beverage_category` | String | Product segment (e.g., Classic Espresso) |
| `beverage` | String | Specific drink name |
| `prep` | String | Milk type and size configuration |
| `calories` | Integer | Total caloric energy |
| `sugar_g` | Float | Grams of sugar |
| `caffeine_mg` | Float | Milligrams of caffeine |
| `fat_g` | Float | Total fat content |
| `nutrient_score` | Float | Engineered metric based on DV (Vitamin A/C, Iron, Calcium) |

---

## 💡 Key Insights

* **The Sugar Trap:** Over 40% of the menu exceeds the WHO's recommended daily sugar limit in a single serving.
* **Customization Lever:** Switching from Whole Milk to Nonfat Milk across the portfolio reduces intake by an average of **~40-60 calories** per SKU.
* **Caffeine Leaders:** Brewed coffees and Cold Brews provide the highest "Caffeine Efficiency" (most buzz for the least energy cost).

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📧 Contact

**Emily** - [Your GitHub Profile](https://www.google.com/search?q=https://github.com/emilyxxhy)

Project Link: [https://github.com/emilyxxhy/starbucks_portfolio_app](https://github.com/emilyxxhy/starbucks_portfolio_app)

---

*Disclaimer: This app is for portfolio purposes. Nutritional data is based on publicly available Starbucks US tables.*
