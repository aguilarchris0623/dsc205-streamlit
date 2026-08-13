import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

url = 'https://raw.githubusercontent.com/iantonios/dsc205/refs/heads/main/CT-towns-income-census-2020.csv'
df = pd.read_csv(url)

df['Per capita income'] = df['Per capita income'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(int)
df['Median household income'] = df['Median household income'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(int)
df['Median family income'] = df['Median family income'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(int)

st.header('Towns by County')

counties = df['County'].unique()
selected_county = st.selectbox('Select a County', counties)

county_df = df[df['County'] == selected_county]

st.subheader(f'Cities and Towns in {selected_county} County')
st.dataframe(county_df[['Town', 'Population', 'Median household income']], width=800, height=200)

min_income = int(df['Median household income'].min())
max_income = int(df['Median household income'].max())

income_range = st.slider(
    'Select a Median Household Income Range',
    min_value=min_income,
    max_value=max_income,
    value=(min_income, max_income) # Default to full range
)
