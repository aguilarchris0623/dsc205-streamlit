import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

df_tests = pd.read_csv("https://raw.githubusercontent.com/aguilarchris0623/dsc205-streamlit/refs/heads/main/covid19_tests(in).csv")
df_pop = pd.read_csv('https://raw.githubusercontent.com/aguilarchris0623/dsc205-streamlit/refs/heads/main/2020v21ct.csv')

#Clean the population data so it matched the same Town names as the Covid data. Add up all age groups and sex to get total town population 
town_pop = (df_pop.groupby('TOWN NAME')['ALL_RACE-ETHN'].sum().reset_index())
town_pop['Town'] = (town_pop['TOWN NAME'].str.replace(' town', '', case=False).str.strip())
town_pop = town_pop.rename(columns={'ALL_RACE-ETHN': 'Population'})

#Convert srting date to datetime format
df_tests["Last update date"] = pd.to_datetime(df_tests["Last update date"])

#Create tiers to divide up different sized towns
def get_tier(pop):
        if pop > 50000:
            return 'Urban (>50k)'
        elif pop >= 10000:
            return 'Suburban (10k-50k)'
        else:
            return 'Rural (<10k)'
                
town_pop["Town Tier"] = town_pop['Population'].apply(get_tier)

#Combine both datasets
df = pd.merge(
df_tests,
town_pop[['Town', 'Population', 'Town Tier']],
 on='Town',
 how='inner',)

st.header('Covid-19 Population vs. Infection & Mortality')

#Pull the last entries recorded on 6/24/2022 for all 169 Towns. Need totals for visuals
latest = (df.sort_values("Last update date").groupby("Town", as_index=False).last())

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(latest)

st.markdown('---')

st.subheader("1. Population & Mortality Benchmark")

#Select between three options for different visuals
metric_choice = st.selectbox(
        "Metric",
        ["Total deaths", "Deaths per 100k", "Positivity Rate (%)"],)

#Equations for mertics
latest["Deaths per 100k"] = (latest["Total deaths"] / latest["Population"]) * 100_000
latest["Positivity Rate (%)"] = (latest["Number of positives"] / latest["Number of tests"]) * 100

#Visual 1: Town population vs...
fig1 = px.scatter(
    latest,
    x="Population",
    y=metric_choice,
    color="Town Tier",
    hover_name="Town",
    log_x=True,
    title=f"{metric_choice} vs. Town Population")

st.plotly_chart(fig1)

st.markdown('---')

st.subheader("2. New Cases by Town Size Tier")

df.columns = df.columns.str.strip()

# Calculate daily new cases per town
df_sorted = df.sort_values(by=['Town', 'Last update date'])
df_sorted['Daily New Cases'] = df_sorted.groupby('Town')['Total cases'].diff().fillna(0)

# Aggregate daily new cases by date and town tier
tier_ts = df_sorted.groupby(['Last update date', 'Town Tier'])['Daily New Cases'].sum().reset_index()

#Find the min and max dates for slider
min_date_dt = tier_ts['Last update date'].min()
max_date_dt = tier_ts['Last update date'].max()
min_date_slider = min_date_dt.date()
max_date_slider = max_date_dt.date()

#Code for interactive slider
selected_date_range = st.slider(
    "Select Date Range:",
    min_value=min_date_slider,
    max_value=max_date_slider,
    value=(min_date_slider, max_date_slider))

start_date, end_date = selected_date_range

filtered_tier_ts = tier_ts[
    (tier_ts['Last update date'] >= pd.to_datetime(start_date)) &
    (tier_ts['Last update date'] <= pd.to_datetime(end_date))]

#Visual 2: Daily New Cases
fig2 = px.line(
    filtered_tier_ts,
    x="Last update date",
    y="Daily New Cases",
    color="Town Tier",
    title="Daily New Cases Over Time by Town Tier",
    labels={
        "Last update date": "Date",
        "Daily New Cases": "Daily New Cases",},)

omnicron = pd.to_datetime('2022-01-10')
fig2.add_vline(
        line_width=2,
        line_dash="dash",
        line_color="yellow",
        annotation_text="Omicron Peak")

st.plotly_chart(fig2, width='stretch')
