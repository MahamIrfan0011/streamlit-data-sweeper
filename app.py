import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Streamlit App Title
st.title("🧹 Data Sweeper - Clean Your Dataset")

# File Upload
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### 📊 Raw Data Preview")
    st.write(df.head())

    # Handle Missing Values
    if st.checkbox("Remove Missing Values"):
        df.dropna(inplace=True)
        st.success("✅ Missing values removed!")

    # Remove Duplicates
    if st.checkbox("Remove Duplicates"):
        df.drop_duplicates(inplace=True)
        st.success("✅ Duplicates removed!")

    # Handle Outliers
    if st.checkbox("Remove Outliers (Using IQR Method)"):
        def remove_outliers(data):
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            return data[~((data < (Q1 - 1.5 * IQR)) | (data > (Q3 + 1.5 * IQR))).any(axis=1)]
        
        df = remove_outliers(df)
        st.success("✅ Outliers removed!")

    # Show Cleaned Data
    st.write("### ✅ Cleaned Data Preview")
    st.write(df.head())

    # Download Cleaned Data
    cleaned_file = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Cleaned CSV", cleaned_file, "cleaned_data.csv", "text/csv")

    # Data Visualization
    st.write("### 📊 Data Distribution")
    numeric_cols = df.select_dtypes(include=np.number).columns
    if len(numeric_cols) > 0:
        selected_col = st.selectbox("Select a column to visualize", numeric_cols)
        fig, ax = plt.subplots()
        sns.histplot(df[selected_col], bins=30, kde=True, ax=ax)
        st.pyplot(fig)
    else:
        st.warning("No numeric columns found for visualization.")

else:
    st.info("Please upload a CSV file to start cleaning.")

