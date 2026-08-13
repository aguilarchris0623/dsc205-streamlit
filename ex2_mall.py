import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('Diabetic vs. non-diabetic')
df = pd.read_csv('https://raw.githubusercontent.com/iantonios/dsc205/refs/heads/main/diabetes.csv')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(df)

st.markdown('---')
st.subheader('Gas consumption by country of origin')

Outcome = st.radio('Select if diabetic or non-diabetic', ('Diabetic', 'Non-diabetic'))

if Outcome == 'Diabetic':
    df = df.loc[df['Outcome']=='1']
elif Outcome == 'Europe':
    df = df.loc[df['Outcome']=='0']
else:
    df = df.loc[df['Outcome']=='2']

fig = plt.figure()
ax = fig.add_subplot()
ax.set_xlabel('mpg')
ax.hist(df['Outcome'])
st.pyplot(fig)
