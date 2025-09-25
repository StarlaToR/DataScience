import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

@st.cache_data
def load_clean_sales2024():
    videogame_sales_2024_df = pd.read_csv("../Dataset/vgchartz-2024.csv", sep=',', decimal='.')
    videogame_sales_2024_df_cleaned = videogame_sales_2024_df.drop_duplicates()
    videogame_sales_2024_df_cleaned["release_date"] = pd.to_datetime(videogame_sales_2024_df_cleaned["release_date"])
    videogame_sales_2024_df_cleaned = videogame_sales_2024_df_cleaned[videogame_sales_2024_df_cleaned["release_date"] < pd.to_datetime("2017-01-01")]
    videogame_sales_2024_df_cleaned = videogame_sales_2024_df_cleaned[["title" ,"console", "genre", "total_sales", "na_sales", "jp_sales", "pal_sales","other_sales","release_date", "critic_score"]]
    videogame_sales_2024_df_cleaned["na_sales"] = videogame_sales_2024_df_cleaned["na_sales"].fillna(videogame_sales_2024_df_cleaned["na_sales"].mean())
    videogame_sales_2024_df_cleaned["jp_sales"] = videogame_sales_2024_df_cleaned["jp_sales"].fillna(videogame_sales_2024_df_cleaned["jp_sales"].mean())
    videogame_sales_2024_df_cleaned["pal_sales"] = videogame_sales_2024_df_cleaned["pal_sales"].fillna(videogame_sales_2024_df_cleaned["pal_sales"].mean())
    videogame_sales_2024_df_cleaned["other_sales"] = videogame_sales_2024_df_cleaned["other_sales"].fillna(videogame_sales_2024_df_cleaned["other_sales"].mean())
    videogame_sales_2024_df_cleaned = videogame_sales_2024_df_cleaned[videogame_sales_2024_df_cleaned["genre"] != "Misc"] #Too many Nan data
    videogame_sales_2024_df_cleaned['year'] = videogame_sales_2024_df_cleaned['release_date'].dt.year
    videogame_sales_2024_df_cleaned['year'].dropna()
    return videogame_sales_2024_df_cleaned

def show_sales_per_year(df_sales2024, genreOnGraph, start, end):
    fig = plt.figure()

    for genre in df_sales2024["genre"].unique():
        if genre in genreOnGraph:
            salesPerYear = df_sales2024[df_sales2024["genre"] == genre]
            salesPerYear = salesPerYear[(salesPerYear['year'] >= start) & (salesPerYear['year'] <= end)]
            salesPerYear = salesPerYear.groupby("year")["total_sales"].sum()
            plt.plot(salesPerYear.index, salesPerYear.values, label=genre)


    plt.legend(title = "Genre",loc='center left', bbox_to_anchor=(1, 0.5))
    plt.title("Sales per year")
    plt.xlabel('Year')
    plt.ylabel('Total Sales (in millions)')

    st.pyplot(fig)

st.set_page_config(page_title="Sales by year", page_icon="📊")

st.title('Video games genres sales by year')

st.sidebar.title('Sales by year')
st.sidebar.subheader('Genres')

genreOnGraph = np.array(("Action", "Action-Adventure", "Adventure", "Fighting", "Platform", "Role-Playing", "Shooter", "Sports"))

action = st.sidebar.checkbox("Action", True)
act_adv = st.sidebar.checkbox("Action-Adventure", True)
advent = st.sidebar.checkbox("Adventure", True)
fight = st.sidebar.checkbox("Fighting", True)
plat = st.sidebar.checkbox("Platform", True)
rpg = st.sidebar.checkbox("Role-Playing", True)
shoot = st.sidebar.checkbox("Shooter", True)
sport = st.sidebar.checkbox("Sports", True)
boolean = np.array((action, act_adv, advent, fight, plat, rpg, shoot, sport))

st.sidebar.subheader('Period')
start = st.sidebar.number_input("Start", 1976, 2016, 1976)
end = st.sidebar.number_input("End", start, 2016, 2016)

if (start > end):
    start = np.clip(end - 1, 1976, end)
if (start == end):
    end += 1

df_sales2024 = load_clean_sales2024()

st.subheader('Sales per year')
show_sales_per_year(df_sales2024, genreOnGraph[boolean], start, end)