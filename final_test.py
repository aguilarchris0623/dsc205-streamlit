import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


df_tests = pd.read_csv("https://raw.githubusercontent.com/aguilarchris0623/dsc205-streamlit/refs/heads/main/covid19_tests.csv")
df_pop = pd.read_csv('https://raw.githubusercontent.com/aguilarchris0623/dsc205-streamlit/refs/heads/main/2020v21ct.csv')

# 6. Aggregate population per town & clean town names
town_pop = (df_pop.groupby('TOWN NAME')['ALL_RACE-ETHN'].sum().reset_index())
town_pop['Town'] = (town_pop['TOWN NAME'].str.replace(' town', '', case=False).str.strip())
town_pop = town_pop.rename(columns={'ALL_RACE-ETHN': 'Population'})

df_tests["Last update date"] = pd.to_datetime(df_tests["Last update date"])

columns_to_exclude = ['Last update date', 'Town']

for col in df_tests.columns:
    if col not in columns_to_exclude:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.replace(',', '', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce')

def get_tier(pop):
        if pop > 50000:
            return 'Urban Hubs (>50k)'
        elif pop >= 10000:
            return 'Suburban (10k-50k)'
        else:
            return 'Rural (<10k)'

town_pop['Town_Tier'] = town_pop['Population'].apply(get_tier)

df = pd.merge(
df_tests,
town_pop[['Town', 'Population', 'Town_Tier']],
 on='Town',
 how='inner',)

metric_choice = st.selectbox(
        "Metric",
        ["Deaths per 100k", "Total deaths", "Positivity Rate (%)"],)

df["Deaths per 100k"] = (df["Total deaths"] / df["Population"]) * 100_000
df["Positivity Rate (%)"] = (df["Number of positives"] / df["Number of tests"]) * 100

fig1 = px.scatter(
        df,
        x="Population",
        y=metric_choice,
        color="Town_Tier",
        hover_name="Town",
        log_x=True,
        log_y=(metric_choice != "Positivity Rate (%)"),  # a %, so linear y reads better
        title=f"{metric_choice} vs. Town Population",
        labels={"Population": "Town Population"},)

st.plotly_chart(fig1, use_container_width=True)
