import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

@st.cache_data
def load_csv(url):
    df = pd.read_csv(url)
    return df

df = load_csv("temperatures.csv")

st.write('hello :D')
name = st.text_input("What is your name ?")
if (name != ""):
    st.write('hello ' + name)

fig, ax = plt.subplots()
ax.scatter(df, df)

st.pyplot(fig)