import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

url = ('https://raw.githubusercontent.com/iantonios/dsc205/refs/heads/main/mall_customers.csv')
df = pd.read_csv(url)

st.title('Mall customers')

st.subheader('Spending score by gender')
st.radio('Select Gender', options=['Male', 'Female'])
fig, ax = plt.subplots()
ax.hist(df['Gender'], df['Spending Score (1-100)'])
ax.set_xlabel('Gender')
ax.set_ylabel('Spending Score')
st.pyplot(fig, clear_figure=True)
