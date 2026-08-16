import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

df_tests["Last update date"] = pd.to_datetime(df_tests["Last update date"])

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


df["Deaths per 100k"] = (df["Total deaths"] / df["Population"]) * 100_000

selected_metric = st.selectbox(
    "Select Y-Axis Metric:",
    ["Deaths per 100k", "Total deaths", "Positivity Rate (%)"],)

fig1 = fig, ax = plt.subplots(figsize=(12, 7))
sns.scatterplot(
        data=df,
        x="Population",
        y=selected_metric,
        hue="Town_Tier",
        ax.set_xlabel("Town Population", fontsize=12),
        ax.set_ylabel(selected_metric, fontsize=12),
        ax.legend(title='Town Tier'),
        st.pyplot(fig))
