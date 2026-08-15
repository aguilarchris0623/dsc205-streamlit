import streamlit as st
import plotly.express as px
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/aguilarchris0623/dsc205-streamlit/refs/heads/main/covid_tests.csv")

df['Last update date'] = pd.to_datetime(df['Last update date'])
df['YearMonth'] = df['Last update date'].dt.to_period('M')
columns_to_sum = [
    'Total cases', 'Confirmed cases', 'Probable cases',
    'Total deaths', 'Confirmed deaths', 'Probable deaths',
    'People tested', 'Number of tests', 'Number of positives',
    'Number of negatives', 'Number of indeterminates']

# Clean column names by stripping whitespace
df.columns = df.columns.str.strip()

# Convert specified columns to numeric, handling non-numeric values by coercing them to NaN
for col in columns_to_sum:
    if col in df.columns:
        df[col] = df[col].astype(str).str.replace(',', '', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Group by 'Town' and 'YearMonth' and sum the relevant columns
monthly_updates = df.groupby(['Town', 'YearMonth'])[columns_to_sum].sum().reset_index()

df2 = pd.read_csv("2020v21CT.csv")
