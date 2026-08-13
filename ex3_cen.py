import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

url = 'https://raw.githubusercontent.com/iantonios/dsc205/refs/heads/main/CT-towns-income-census-2020.csv'
df = pd.read_csv(url)

df['Per capita income'] = df['Per capita income'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(int)
df['Median household income'] = df['Median household income'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(int)
df['Median family income'] = df['Median family income'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(int)

counties = df['County'].unique()
selected_county = st.selectbox('Select a County', counties)
county_df = df[df['County'] == selected_county]
st.dataframe(county_df[['Place']], width=800, height=200)

min_income = int(df['Median household income'].min())
max_income = int(df['Median household income'].max())

