
import pandas as pd
import numpy as np

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.replace(r"[^\w]+", "_", regex=True)
        .str.replace(r"_+", "_", regex=True)
        .str.strip("_")
    )
    rename_map = {
        "Beverage_category": "category",
        "Beverage": "beverage",
        "Beverage_prep": "prep",
        "Calories": "calories",
        "Sugars__g_": "sugar_g",
        "Sugars_g": "sugar_g",
        "Sugars_g_": "sugar_g",
        "Sugars__g": "sugar_g",
        "Total_Carbohydrates__g_": "carbs_g",
        "Total_Fat__g_": "fat_g",
        "Saturated_Fat__g_": "sat_fat_g",
        "Trans_Fat__g_": "trans_fat_g",
        "Protein__g_": "protein_g",
        "Sodium__mg_": "sodium_mg",
        "Cholesterol__mg_": "cholesterol_mg",
        "Dietary_Fibre__g_": "fiber_g",
        "Vitamin_A___DV_": "vitamin_a_dv",
        "Vitamin_C___DV_": "vitamin_c_dv",
        "Calcium___DV_": "calcium_dv",
        "Iron___DV_": "iron_dv",
        "Caffeine__mg_": "caffeine_mg",
        "Unnamed_0": "row_id"
    }
    df = df.rename(columns={k:v for k,v in rename_map.items() if k in df.columns})
    for c in ["calories","sugar_g","carbs_g","fat_g","sat_fat_g","trans_fat_g","protein_g","sodium_mg","cholesterol_mg","fiber_g","caffeine_mg"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return normalize_columns(df)

def goal_filter(df: pd.DataFrame, under_cal=None, under_sugar=None, under_fat=None) -> pd.DataFrame:
    out = df.copy()
    if under_cal is not None and "calories" in out: out = out[out["calories"] <= under_cal]
    if under_sugar is not None and "sugar_g" in out: out = out[out["sugar_g"] <= under_sugar]
    if under_fat is not None and "fat_g" in out: out = out[out["fat_g"] <= under_fat]
    return out

def healthier_alternative(df: pd.DataFrame, row, by=["category","prep"], sort_by=["calories","sugar_g"]):
    """Find a similar but lighter option in same (category, prep) if possible; else same category; else global."""
    df = df.copy()
    subset = df.copy()
    for col in by:
        if col in df.columns and col in row and pd.notna(row[col]):
            subset = subset[subset[col] == row[col]]
    if subset.empty and "category" in df.columns and "category" in row:
        subset = df[df["category"] == row["category"]]
    if subset.empty:
        subset = df
    for sb in sort_by:
        if sb in subset.columns:
            subset = subset.sort_values(sb, ascending=True)
    # Prefer items with lower calories & sugar than original
    if "calories" in subset.columns and "calories" in row and "sugar_g" in subset.columns and "sugar_g" in row:
        subset = subset[(subset["calories"] <= row["calories"]) & (subset["sugar_g"] <= row["sugar_g"])]
    # remove self by beverage name+prep if exists
    if "beverage" in subset.columns and "beverage" in row:
        subset = subset[subset["beverage"] != row["beverage"]]
    return subset.head(1)

def top_k(df: pd.DataFrame, col: str, k: int = 10, asc: bool = False):
    if col not in df.columns: return pd.DataFrame()
    return df.sort_values(col, ascending=asc).head(k)

def numeric_columns(df: pd.DataFrame):
    return [c for c in ["calories","sugar_g","carbs_g","fat_g","sat_fat_g","protein_g","sodium_mg","cholesterol_mg","fiber_g","caffeine_mg"] if c in df.columns]
