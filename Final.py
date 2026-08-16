import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


df_tests = pd.read_csv("https://raw.githubusercontent.com/aguilarchris0623/dsc205-streamlit/refs/heads/main/covid19_tests(in).csv")
df_pop = pd.read_csv('https://raw.githubusercontent.com/aguilarchris0623/dsc205-streamlit/refs/heads/main/2020v21ct.csv')

# 6. Aggregate population per town & clean town names
town_pop = (df_pop.groupby('TOWN NAME')['ALL_RACE-ETHN'].sum().reset_index())
town_pop['Town'] = (town_pop['TOWN NAME'].str.replace(' town', '', case=False).str.strip())
town_pop = town_pop.rename(columns={'ALL_RACE-ETHN': 'Population'})

df_tests["Last update date"] = pd.to_datetime(df_tests["Last update date"])

def get_tier(pop):
        if pop > 50000:
            return 'Urban (>50k)'
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
        ["Total deaths", "Deaths per 100k", "Positivity Rate (%)"],)

latest = (
        df.sort_values("Last update date")
        .groupby("Town", as_index=False)
        .last())

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(latest)

# Define metric_choice before using it
latest["Deaths per 100k"] = (latest["Total deaths"] / latest["Population"]) * 100_000
latest["Positivity Rate (%)"] = (latest["Number of positives"] / latest["Number of tests"]) * 100

fig1 = px.scatter(
    latest,
    x="Population",
    y=metric_choice,
    color="Town_Tier",
    hover_name="Town",
    log_x=True,

    title=f"{metric_choice} vs. Town Population",
    labels={"Population": "Town Population"},)

st.plotly_chart(fig1, width='stretch')
