import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('Diabetic vs. Non-diabetic')
df = pd.read_csv('https://raw.githubusercontent.com/iantonios/dsc205/refs/heads/main/diabetes.csv')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(df)

st.markdown('---')
st.subheader('Distribution of glucose')

Select = st.radio('Select if Diabetic or Non-diabetic', ('Diabetic', 'Non-diabetic'))

if Select == 'Diabetic':
    df = df.loc[df['Outcome'] == 1]
else:
    df = df.loc[df['Outcome'] == 0]

fig = plt.figure()
ax = fig.add_subplot()
ax.set_xlabel('Glucose Level')
ax.hist(df['Glucose'], bins=20)
st.pyplot(fig)
