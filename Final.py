import folium
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from streamlit_folium import st_folium


df_tests = pd.read_csv("https://raw.githubusercontent.com/aguilarchris0623/dsc205-streamlit/refs/heads/main/covid19_tests.csv")
df_pop = pd.read_csv('https://raw.githubusercontent.com/aguilarchris0623/dsc205-streamlit/refs/heads/main/2020v21ct.csv')


# Aggregate total population per town & assign tiers
town_pop = (df_pop.groupby('TOWN NAME')['ALL_RACE-ETHN'].sum().reset_index())
town_pop['Town'] = (town_pop['TOWN NAME'].str.replace(' town', '', case=False).str.strip())
town_pop = town_pop.rename(columns={'ALL_RACE-ETHN': 'Population'})

def get_tier(pop):
    if pop > 50000:
        return 'Urban Hubs (>50k)'
    elif pop >= 10000:
        return 'Suburban (10k-50k)'
    else:
        return 'Rural (<10k)'

town_pop['Town_Tier'] = town_pop['Population'].apply(get_tier)

# Merge population demographics into Covid dataset
df = pd.merge(
df_tests,
town_pop[['Town', 'Population', 'Town_Tier']],
on='Town',
how='inner',)




# Filter dataset for the latest date slice
latest_df = df['Last update date'].max()

# Calculate per-capita metrics
latest_df["Deaths per 100k"] = (latest_df["Total deaths"] / latest_df["Population"]) * 100_000
latest_df["Positivity Rate (%)"] = (latest_df["Number of positives"] / latest_df["Number of tests"]) * 100


# Widget: Metric Selection Dropdown
selected_metric = st.selectbox(
    "Select Y-Axis Metric:",
    ["Deaths per 100k", "Total deaths", "Positivity Rate (%)"],)


latest = (
        filtered.sort_values("Last update date")
        .groupby("Town", as_index=False)
        .last())
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
