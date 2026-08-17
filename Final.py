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
                
town_pop["Town Tier"] = town_pop['Population'].apply(get_tier)

df = pd.merge(
df_tests,
town_pop[['Town', 'Population', 'Town Tier']],
 on='Town',
 how='inner',)

st.header('Covid-19 Population vs. Infection & Mortality')

latest = (
        df.sort_values("Last update date")
        .groupby("Town", as_index=False)
        .last())

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(latest)

st.markdown('---')

metric_choice = st.selectbox(
        "Metric",
        ["Total deaths", "Deaths per 100k", "Positivity Rate (%)"],)

latest["Deaths per 100k"] = (latest["Total deaths"] / latest["Population"]) * 100_000
latest["Positivity Rate (%)"] = (latest["Number of positives"] / latest["Number of tests"]) * 100

fig1 = px.scatter(
    latest,
    x="Population",
    y=metric_choice,
    color="Town Tier",
    hover_name="Town",
    log_x=True,
    title=f"{metric_choice} vs. Town Population",
    labels={"Population": "Town Population"},)

st.plotly_chart(fig1, width='stretch')

st.markdown('---')

st.subheader("2. New Cases by Town Size Tier")

df.columns = df.columns.str.strip()

# Sort by date for correct difference calculation for each town
df_sorted = df.sort_values(by=['Town', 'Last update date'])

# Calculate daily new cases per town. fillna(0) for the first day of each town.
df_sorted['Daily New Cases'] = df_sorted.groupby('Town')['Total cases'].diff().fillna(0)

# Ensure new cases are not negative (e.g., due to data corrections, though they shouldn't be negative)
df_sorted['Daily New Cases'] = df_sorted['Daily New Cases'].apply(lambda x: max(0, x))

# Aggregate daily new cases by date and town tier for plotting
tier_ts = df_sorted.groupby(['Last update date', 'Town Tier'])['Daily New Cases'].sum().reset_index()

# Plot Visual 2: Daily New Cases
fig2 = px.line(
    tier_ts,
    x="Last update date",
    y="Daily New Cases",
    color="Town Tier",
    title="Daily New Cases Over Time by Town Tier",
    labels={
        "Last update date": "Date",
        "Daily New Cases": "Daily New Cases",},)

date_range = st.slider(
        "Last update date",
        min_value=min_date.to_pydatetime(),
        max_value=max_date.to_pydatetime(),
        value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
        key="chart2_date_range",)

st.plotly_chart(fig2, width='stretch')
