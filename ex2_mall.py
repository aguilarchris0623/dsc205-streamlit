import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

url = ('https://raw.githubusercontent.com/iantonios/dsc205/refs/heads/main/diabetes.csv')
df = pd.read_csv(url)

st.title('Mall customers')

st.subheader('Spending score by gender')
st.radio('Outcome', options=['1', '0'])
fig, ax = plt.subplots()
ax.hist(df['outcome'])
ax.set_xlabel('Gender')
ax.set_ylabel('Spending Score')
st.pyplot(fig, clear_figure=True)
