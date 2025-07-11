import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv("examscores.csv")
df = df.drop("Unnamed: 0", axis=1)
df["WklyStudyHours"] = df["WklyStudyHours"].str.replace("05-Oct", "5 - 10")

# Sidebar Filters
st.sidebar.title("🎛️ Easy Filters")
st.sidebar.markdown("Use the dropdowns and sliders below to explore the dataset.")

selected_gender = st.sidebar.multiselect("👨‍👩‍👧 Select Gender:", df['Gender'].unique(), default=df['Gender'].unique())
selected_ethnic = st.sidebar.multiselect("🌐 Select Ethnic Group:", df['EthnicGroup'].unique(), default=df['EthnicGroup'].unique())
selected_prep = st.sidebar.multiselect("📚 Test Preparation Status:", df['TestPrep'].unique(), default=df['TestPrep'].unique())

math_range = st.sidebar.slider("🧮 Math Score Range:", 0, 100, (0, 100))
reading_range = st.sidebar.slider("📖 Reading Score Range:", 0, 100, (0, 100))
writing_range = st.sidebar.slider("✍️ Writing Score Range:", 0, 100, (0, 100))

# Filtered DataFrame
filtered_df = df[
    (df['Gender'].isin(selected_gender)) &
    (df['EthnicGroup'].isin(selected_ethnic)) &
    (df['TestPrep'].isin(selected_prep)) &
    (df['MathScore'].between(*math_range)) &
    (df['ReadingScore'].between(*reading_range)) &
    (df['WritingScore'].between(*writing_range))
]

# App Title
st.title("📊 Student Result Analysis Dashboard")
st.markdown("""This interactive dashboard allows you to analyze and compare student scores based on different attributes such as gender, ethnicity, parental education, and more.""")

# Dataset Overview
if st.checkbox("Show Dataset Overview"):
    st.subheader("Dataset Preview")
    st.write(filtered_df.head())

if st.checkbox("Show Summary Statistics"):
    st.subheader("Summary Statistics")
    st.write(filtered_df.describe())

if st.checkbox("Show Missing Values"):
    st.subheader("Missing Values")
    st.write(filtered_df.isnull().sum())

# Gender Distribution
if st.checkbox("Show Gender Distribution"):
    st.subheader("Gender Distribution")
    plt.figure(figsize=(5, 5))
    ax = sns.countplot(data=filtered_df, x="Gender", palette="Set2")
    plt.title("Gender Distribution")
    st.pyplot(plt.gcf())

# Heatmap by Custom Group
st.sidebar.markdown("---")
st.sidebar.subheader("📌 Compare Scores Groupwise")
group_col = st.sidebar.selectbox("Group students by:", ["Gender", "ParentEduc", "ParentMaritalStatus", "WklyStudyHours", "TestPrep", "LunchType", "PracticeSport"])

heatmap_data = filtered_df.groupby(group_col).agg({
    "MathScore": 'mean',
    "ReadingScore": 'mean',
    "WritingScore": 'mean'
})

st.subheader(f"{group_col} vs Scores Heatmap")
st.write(heatmap_data)
plt.figure(figsize=(5, 3.5))
sns.heatmap(heatmap_data, annot=True, cmap="viridis", linewidths=0.5)
plt.title(f"{group_col} vs Mean Scores")
st.pyplot(plt.gcf())

# Score Distributions
if st.checkbox("Show Score Distributions"):
    st.subheader("Score Distributions")
    fig, axs = plt.subplots(3, 1, figsize=(9, 10))
    sns.histplot(filtered_df['MathScore'], bins=20, ax=axs[0], kde=True, color="skyblue")
    axs[0].set_title("Math Score Distribution")
    sns.histplot(filtered_df['ReadingScore'], bins=20, ax=axs[1], kde=True, color="lightgreen")
    axs[1].set_title("Reading Score Distribution")
    sns.histplot(filtered_df['WritingScore'], bins=20, ax=axs[2], kde=True, color="salmon")
    axs[2].set_title("Writing Score Distribution")
    plt.tight_layout()
    st.pyplot(fig)

# Ethnic Group Pie Chart
if st.checkbox("Show Ethnic Group Distribution"):
    st.subheader("Distribution of Ethnic Groups")
    ethnic_counts = filtered_df['EthnicGroup'].value_counts()
    plt.figure(figsize=(4, 4))
    plt.pie(ethnic_counts, labels=ethnic_counts.index, autopct="%1.1f%%", startangle=140, colors=plt.cm.rainbow(np.linspace(0, 1, len(ethnic_counts))))
    plt.title("Ethnic Group Distribution")
    st.pyplot(plt.gcf())

# Correlation Heatmap
if st.checkbox("Show Correlation Heatmap"):
    st.subheader("Correlation Heatmap Between Scores")
    score_corr = filtered_df[["MathScore", "ReadingScore", "WritingScore"]].corr()
    plt.figure(figsize=(5, 4))
    sns.heatmap(score_corr, annot=True, cmap='coolwarm')
    plt.title("Score Correlation")
    st.pyplot(plt.gcf())

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit | Updated Dashboard")
