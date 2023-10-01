import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def load_data(data_source, uploaded_file):
    if data_source == "CSV":
        d_frame = pd.read_csv(uploaded_file)
    elif data_source == "Excel":
        d_frame = pd.read_excel(uploaded_file)
    
    return d_frame

def preprocess_data(d_frame):
    st.subheader("Data Pre-processing")
    st.title("Data uploaded ")
    st.dataframe(d_frame)
    
    st.write("Column data_types")
    column_types = d_frame.dtypes
    st.write(column_types)
    
    st.write("Missing Values")
    missing_values = d_frame.isnull().sum()
    st.write(missing_values)
    
    categorical_columns = d_frame.select_dtypes(include=["object"]).columns
    st.write("Categorical data")
    st.write(categorical_columns)
    
    numeric_columns = d_frame.select_dtypes(include=["number"]).columns
    st.write("Numeric data ")
    st.write(numeric_columns)
    
    return d_frame

def handle_missing_data(d_frame, numerical_strategy='mean', categorical_strategy='most_frequent', fill_value=None):
    
    numerical_columns = d_frame.select_dtypes(include=['number']).columns
    categorical_columns = d_frame.select_dtypes(include=['object', 'category']).columns

    
    if numerical_strategy == 'mean':
        d_frame[numerical_columns] = d_frame[numerical_columns].fillna(d_frame[numerical_columns].mean())
    elif numerical_strategy == 'median':
        d_frame[numerical_columns] = d_frame[numerical_columns].fillna(d_frame[numerical_columns].median())
    elif numerical_strategy == 'constant':
        d_frame[numerical_columns] = d_frame[numerical_columns].fillna(fill_value)

    
    if categorical_strategy == 'most_frequent':
        d_frame[categorical_columns] = d_frame[categorical_columns].fillna(d_frame[categorical_columns].mode().iloc[0])
    elif categorical_strategy == 'constant':
        d_frame[categorical_columns] = d_frame[categorical_columns].fillna(fill_value)
    
    st.write("data missing handled ")
    missing_values = d_frame.isnull().sum()
    st.write(missing_values)

    return d_frame



def Visualization(d_frame):
    st.subheader("Visualization")

    
    st.write("Histograms ")
    for column in d_frame.select_dtypes(include=["number"]).columns:
        fig, ax = plt.subplots()
        sns.histplot(d_frame[column], kde=True, ax=ax)
        st.pyplot(fig)

    
    st.write("Box Plots ")
    for column in d_frame.select_dtypes(include=["number"]).columns:
        fig, ax = plt.subplots()
        sns.boxplot(x=d_frame[column], ax=ax)
        st.pyplot(fig)

    
    st.write("Scatter Plots")
    for x_column in d_frame.select_dtypes(include=["number"]).columns:
        for y_column in d_frame.select_dtypes(include=["number"]).columns:
            if x_column != y_column:
                fig = px.scatter(d_frame, x=x_column, y=y_column)
                st.plotly_chart(fig)


def main():
    st.title("Automated EDA Tool")

    
    data_source = st.selectbox("the dataset type", ["CSV", "Excel"])
    uploaded_file = st.file_uploader("Upload Data ")

    if uploaded_file:
        d_frame = load_data(data_source, uploaded_file)
        if d_frame is not None:
            st.success("Data loaded ")

            
            preprocess_checkbox = st.checkbox("Data Pre-processing")
            if preprocess_checkbox:
                d_frame = preprocess_data(d_frame)
                d_frame = handle_missing_data(d_frame, numerical_strategy='mean', categorical_strategy='most_frequent')
                st.success(" pre-processing completed")

            
            generate_dashboard_checkbox = st.checkbox( "Visualization Dashboard")
            if generate_dashboard_checkbox:
                Visualization(d_frame)
                st.success("Visualization")

if __name__ == "__main__":
    main()
