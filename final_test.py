import folium
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from streamlit_folium import st_folium


df_tests = pd.read_csv("https://raw.githubusercontent.com/aguilarchris0623/dsc205-streamlit/refs/heads/main/covid19_tests.csv")
df_pop = pd.read_csv('https://raw.githubusercontent.com/aguilarchris0623/dsc205-streamlit/refs/heads/main/2020v21ct.csv')


df_tests.columns = df_tests.columns.str.strip()
df_pop.columns = df_pop.columns.str.strip()

# 3. Explicitly clean and convert ALL test metrics to numeric (float/int)
test_numeric_cols = [
    'Total cases',
    'Total deaths',
    'Number of tests',
    'Number of positives',
    'Number of negatives',
    'Case rate',
    'Rate tested per 100k',]

for col in test_numeric_cols:
    if col in df_tests.columns:
# Remove commas and convert to numeric
df_tests[col] = pd.to_numeric(
df_tests[col].astype(str).str.replace(',', '').str.strip(),
errors='coerce',)

    # 4. Clean and convert Population column in Census dataset
df_pop['ALL_RACE-ETHN'] = pd.to_numeric(
df_pop['ALL_RACE-ETHN'].astype(str).str.replace(',', '').str.strip(),
errors='coerce',)

# 5. Parse update date
df_tests['Last update date'] = pd.to_datetime(df_tests['Last update date'])

# 6. Aggregate population per town & clean town names
town_pop = (df_pop.groupby('TOWN NAME')['ALL_RACE-ETHN'].sum().reset_index())
town_pop['Town'] = (town_pop['TOWN NAME'].str.replace(' town', '', case=False).str.strip())
town_pop = town_pop.rename(columns={'ALL_RACE-ETHN': 'Population'})

    # Ensure Population is explicitly numeric
town_pop['Population'] = pd.to_numeric(town_pop['Population'], errors='coerce')

# 7. Classify Population Tiers
def get_tier(pop):
  if pop > 50000:
    return 'Urban Hubs (>50k)'
  elif pop >= 10000:
    return 'Suburban (10k-50k)'
  else:
    return 'Rural (<10k)'

town_pop['Town_Tier'] = town_pop['Population'].apply(get_tier)

    # 8. Merge COVID and Population datasets
df = pd.merge(
    df_tests,
    town_pop[['Town', 'Population', 'Town_Tier']],
    on='Town',
    how='inner',)

    return df
