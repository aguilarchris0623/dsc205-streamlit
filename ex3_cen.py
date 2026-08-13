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

income_range = st.slider(
    'Select Income Range',
    min_value=min_income,
    max_value=max_income,
    value=(min_income, max_income))

income_filtered_df = df[
    (df['Median household income'] >= income_range[0]) &
    (df['Median household income'] <= income_range[1])]

st.dataframe(income_filtered_df[['Place', 'Median household income']], width=800, height=200)

df_sorted = df.sort_values(by='Median household income', ascending=False)
top_5_income = df_sorted.head(5)
bottom_5_income = df_sorted.tail(5)

# Combine for plotting
plot_df = pd.concat([top_5_income, bottom_5_income])

# Create the bar chart using Altair for better Streamlit integration and interactivity
chart = alt.Chart(plot_df).mark_bar().encode(
    x=alt.X('Town:N', sort=alt.EncodingSortField(field='Median household income', op='mean', order='descending'), title='City Name'),
    y=alt.Y('Median household income:Q', title='Median Household Income'),
    color=alt.Color('Median household income:Q', scale=alt.Scale(range='heatmap')) # Color by income level
).properties(
    title='Top 5 Highest and Bottom 5 Lowest Median Household Income Cities'
)

st.altair_chart(chart, use_container_width=True)
