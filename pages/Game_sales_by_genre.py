import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

@st.cache_data
def load_clean_sales2024():
    videogame_sales_2024_df = pd.read_csv("vgchartz-2024.csv", sep=',', decimal='.')
    videogame_sales_2024_df_cleaned = videogame_sales_2024_df.drop_duplicates()
    videogame_sales_2024_df_cleaned["release_date"] = pd.to_datetime(videogame_sales_2024_df_cleaned["release_date"])
    videogame_sales_2024_df_cleaned = videogame_sales_2024_df_cleaned[["title" ,"console", "genre", "total_sales", "na_sales", "jp_sales", "pal_sales","other_sales","release_date", "critic_score"]]
    videogame_sales_2024_df_cleaned["na_sales"] = videogame_sales_2024_df_cleaned["na_sales"].fillna(videogame_sales_2024_df_cleaned["na_sales"].mean())
    videogame_sales_2024_df_cleaned["jp_sales"] = videogame_sales_2024_df_cleaned["jp_sales"].fillna(videogame_sales_2024_df_cleaned["jp_sales"].mean())
    videogame_sales_2024_df_cleaned["pal_sales"] = videogame_sales_2024_df_cleaned["pal_sales"].fillna(videogame_sales_2024_df_cleaned["pal_sales"].mean())
    videogame_sales_2024_df_cleaned["other_sales"] = videogame_sales_2024_df_cleaned["other_sales"].fillna(videogame_sales_2024_df_cleaned["other_sales"].mean())
    videogame_sales_2024_df_cleaned = videogame_sales_2024_df_cleaned[videogame_sales_2024_df_cleaned["genre"] != "Misc"] #Too many Nan data
    return videogame_sales_2024_df_cleaned

def show_sales_per_genre(df_sales2024, regions):
    df_sales2024 = df_sales2024.dropna(subset=['genre'])
    salesPerGenre = df_sales2024[["genre", "jp_sales", "na_sales", "pal_sales", "other_sales"]]
    salesPerGenre = salesPerGenre.groupby(["genre"]).sum().reset_index()

    fig, ax = plt.subplots()
    
    botInitialized = False
    bot = salesPerGenre["pal_sales"]

    if (regions[0]):
        ax.bar(salesPerGenre["genre"], salesPerGenre["pal_sales"], label="eu_sales")
        botInitialized = True
    if (regions[1]):
        if (botInitialized):
            ax.bar(salesPerGenre["genre"], salesPerGenre["jp_sales"], bottom = bot, label="jp_sales")
            bot += salesPerGenre["jp_sales"]
        else:
            ax.bar(salesPerGenre["genre"], salesPerGenre["jp_sales"], label="jp_sales")
            bot = salesPerGenre["jp_sales"]
            botInitialized = True
    if (regions[2]):
        if (botInitialized):
            ax.bar(salesPerGenre["genre"], salesPerGenre["na_sales"], bottom = bot, label="na_sales")
            bot += salesPerGenre["na_sales"]
        else:
            ax.bar(salesPerGenre["genre"], salesPerGenre["na_sales"], label="na_sales")
            bot = salesPerGenre["na_sales"]
            botInitialized = True
    if (regions[3]):
        if (botInitialized):
            ax.bar(salesPerGenre["genre"], salesPerGenre["other_sales"], bottom = bot, label="other_sales")
        else:
            ax.bar(salesPerGenre["genre"], salesPerGenre["other_sales"], label="other_sales")

    plt.xticks(rotation=90)
    ax.legend(loc="upper right")
    plt.title("Video Games Sales per genre released between 1980 and 2024")

    st.pyplot(fig)

# Code

st.set_page_config(page_title="Sales by genre", page_icon="📊")

st.title('Video games sales by genre depending on the region')

st.sidebar.title('Sales by genre')
st.sidebar.subheader('Choose the region')
eu = st.sidebar.checkbox("Europe", True)
jp = st.sidebar.checkbox("Japan", True)
na = st.sidebar.checkbox("North America", True)
other = st.sidebar.checkbox("Other", True)

df_sales2024 = load_clean_sales2024()

st.subheader('Sales per genre')
show_sales_per_genre(df_sales2024, [eu, jp, na, other])