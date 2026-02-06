import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import altair as alt
from src.utils import load_data, get_clean_data_for_ml 

st.set_page_config(page_title="Models", page_icon="🧠")
st.title("🧠 Machine Learning Models")

@st.cache_data
def get_df():
    return load_data("data/Nutrition_facts_for_Starbucks_Menu_1604_26.csv")

df = get_df()

# --- 1. CLUSTERING (K-MEANS) ---
st.header("1. Clustering (Phân nhóm đồ uống)")
st.write("Tự động nhóm các món nước dựa trên thành phần dinh dưỡng.")

# Lấy dữ liệu sạch (không cần target category cho clustering)
X_cluster, _, _ = get_clean_data_for_ml(df, target_col=None)

k = st.slider("Chọn số lượng nhóm (Clusters)", 2, 6, 3)

# Scale dữ liệu (Quan trọng cho KMeans)
scaler_cluster = StandardScaler()
X_cluster_scaled = scaler_cluster.fit_transform(X_cluster)

kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
df["cluster"] = kmeans.fit_predict(X_cluster_scaled)

# Biểu đồ Clustering
if "calories" in df.columns and "sugar_g" in df.columns:
    chart = alt.Chart(df).mark_circle(size=60).encode(
        x=alt.X("calories", title="Calories"),
        y=alt.Y("sugar_g", title="Sugar (g)"),
        color=alt.Color("cluster:N", title="Cluster"),
        tooltip=["beverage", "category", "calories", "sugar_g"]
    ).properties(title="Phân nhóm dựa trên Calo & Đường").interactive()
    st.altair_chart(chart, use_container_width=True)
else:
    st.warning("Thiếu dữ liệu để vẽ biểu đồ.")

st.markdown("---")

# --- 2. CLASSIFICATION (KNN) ---
st.header("2. Predict Category (Dự đoán loại nước)")
st.write("Sử dụng KNN để đoán xem món nước thuộc loại nào (VD: Coffee, Smoothie...) dựa trên dinh dưỡng.")

if 'category' in df.columns:
    # 1. Lấy dữ liệu sạch từ utils (Có target category)
    X, y, features = get_clean_data_for_ml(df, target_col="category")
    
    # 2. Sidebar chỉnh tham số
    n_neighbors = st.slider("Số lượng láng giềng (K-Neighbors)", 1, 15, 5)
    
    # 3. Train/Test Split & Scaling
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 4. Train Model
    knn = KNeighborsClassifier(n_neighbors=n_neighbors)
    knn.fit(X_train_scaled, y_train)
    y_pred = knn.predict(X_test_scaled)
    
    # 5. Hiển thị Metrics
    acc = accuracy_score(y_test, y_pred)
    st.metric("Độ chính xác (Accuracy)", f"{acc*100:.1f}%")
    
    with st.expander("Xem chi tiết báo cáo (Classification Report)"):
        st.text(classification_report(y_test, y_pred))

    # 6. Confusion Matrix (Biểu đồ nhiệt)
    st.subheader("Biểu đồ nhầm lẫn (Confusion Matrix)")
    st.caption("Giúp bạn biết Model đang hay nhầm lẫn giữa các loại nào.")
    
    fig, ax = plt.subplots(figsize=(8, 6))
    cm = confusion_matrix(y_test, y_pred, labels=knn.classes_)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=knn.classes_, yticklabels=knn.classes_, ax=ax)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

    # --- 3. INTERACTIVE PREDICTION (Dùng thử) ---
    st.markdown("---")
    st.subheader("🤖 Dùng thử Model")
    st.write("Nhập thông số dinh dưỡng để xem máy đoán là loại gì:")

    with st.form("predict_form"):
        cols = st.columns(3)
        input_data = {}
        for i, col in enumerate(features):
            # Lấy giá trị trung bình để làm gợi ý mặc định
            default_val = float(X[col].median())
            with cols[i % 3]:
                input_data[col] = st.number_input(f"{col}", value=default_val)
        
        submitted = st.form_submit_button("Dự đoán ngay")

    if submitted:
        # Tạo dataframe từ input
        input_df = pd.DataFrame([input_data])
        # Scale dữ liệu input (Bắt buộc dùng scaler đã fit)
        input_scaled = scaler.transform(input_df)
        
        # Dự đoán
        pred = knn.predict(input_scaled)[0]
        probs = knn.predict_proba(input_scaled)[0]
        max_prob = np.max(probs) * 100

        st.success(f"Dự đoán: **{pred}** (Độ tin cậy: {max_prob:.1f}%)")
        
        # Hiển thị chart xác suất
        prob_df = pd.DataFrame({"Category": knn.classes_, "Probability": probs})
        c = alt.Chart(prob_df).mark_bar().encode(
            x="Probability",
            y=alt.Y("Category", sort="-x"),
            color=alt.condition(
                alt.datum.Category == pred,
                alt.value("green"),
                alt.value("lightgray")
            )
        )
        st.altair_chart(c, use_container_width=True)

else:
    st.error("Không tìm thấy cột 'category' trong dữ liệu.")