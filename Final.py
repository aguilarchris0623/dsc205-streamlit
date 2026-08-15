import streamlit as st
import plotly.express as px
import pandas as pd

df_tests = pd.read_csv("https://raw.githubusercontent.com/aguilarchris0623/dsc205-streamlit/refs/heads/main/covid_tests.csv")
df_pop = pd.read_csv('2020v21CT.csv')

# Aggregate total population per town & assign tiers
    town_pop = (
        df_pop.groupby('TOWN NAME')['ALL_RACE-ETHN'].sum().reset_index()
    )
    town_pop['Town'] = (
        town_pop['TOWN NAME'].str.replace(' town', '', case=False).str.strip()
    )
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
        how='inner',
    )
    return df
