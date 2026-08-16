import pandas as pd
import plotly.express as px
import streamlit as st

df_tests = pd.read_csv("https://raw.githubusercontent.com/aguilarchris0623/dsc205-streamlit/refs/heads/main/covid19_tests.csv")
df_pop = pd.read_csv('https://raw.githubusercontent.com/aguilarchris0623/dsc205-streamlit/refs/heads/main/2020v21ct.csv')

# 6. Aggregate population per town & clean town names
town_pop = (df_pop.groupby('TOWN NAME')['ALL_RACE-ETHN'].sum().reset_index())
town_pop['Town'] = (town_pop['TOWN NAME'].str.replace(' town', '', case=False).str.strip())
town_pop = town_pop.rename(columns={'ALL_RACE-ETHN': 'Population'})

TIER_BINS = [0, 10_000, 50_000, float("inf")]
TIER_LABELS = ["Rural (<10k)", "Suburban (10k-50k)", "Urban Hubs (>50k)"]

pop = (
        df_pop.groupby("TOWN NAME")["ALL_RACE-ETHN"]
        .sum()
        .reset_index()
        .rename(columns={"ALL_RACE-ETHN": "Population"}))
pop["Town"] = pop["TOWN NAME"].str.replace(r"\s+town$", "", regex=True).str.strip()


df["Last update date"] = pd.to_datetime(df["Last update date"])

 df = pd.merge(
  df_tests,
  town_pop[['Town', 'Population', 'Town_Tier']],
  on='Town',
  how='inner',)

latest = (
        filtered.sort_values("Last update date")
        .groupby("Town", as_index=False)
        .last()

latest["Deaths per 100k"] = (latest["Total deaths"] / latest["Population"]) * 100_000

fig1 = px.scatter(
        latest,
        x="Population",
        y="Deaths per 100k",
        color="Town_Tier",
        hover_name="Town",
        log_x=True,
        log_y=True,
        title="Deaths per 100k vs. Town Population (log-log)",
        labels={"Population": "Town Population"},)

st.plotly_chart(fig1, use_container_width=True)
