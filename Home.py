import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import random

# Common functions

def mean(val):
    numbers = val.split('-')                
    return (float(numbers[0].strip()) + float(numbers[1].strip())) / 2     


# Cached functions

@st.cache_data
def load_clean_sales2024():
    videogame_sales_2024_df = pd.read_csv("Dataset/vgchartz-2024.csv", sep=',', decimal='.')
    videogame_sales_2024_df_cleaned = videogame_sales_2024_df.drop_duplicates()

    #Clean release date and only keep dates < 2017 as games above 2017 don't have enough data
    videogame_sales_2024_df_cleaned["release_date"] = pd.to_datetime(videogame_sales_2024_df_cleaned["release_date"])
    videogame_sales_2024_df_cleaned = videogame_sales_2024_df_cleaned[videogame_sales_2024_df_cleaned["release_date"] < pd.to_datetime("2017-01-01")]

    #Replace nan values with mean values for sales
    videogame_sales_2024_df_cleaned["na_sales"] = videogame_sales_2024_df_cleaned["na_sales"].fillna(videogame_sales_2024_df_cleaned["na_sales"].mean())
    videogame_sales_2024_df_cleaned["jp_sales"] = videogame_sales_2024_df_cleaned["jp_sales"].fillna(videogame_sales_2024_df_cleaned["jp_sales"].mean())
    videogame_sales_2024_df_cleaned["pal_sales"] = videogame_sales_2024_df_cleaned["pal_sales"].fillna(videogame_sales_2024_df_cleaned["pal_sales"].mean())
    videogame_sales_2024_df_cleaned["other_sales"] = videogame_sales_2024_df_cleaned["other_sales"].fillna(videogame_sales_2024_df_cleaned["other_sales"].mean())

    #Clean genre collumn
    videogame_sales_2024_df_cleaned = videogame_sales_2024_df_cleaned.dropna(subset=['genre'])
    videogame_sales_2024_df_cleaned = videogame_sales_2024_df_cleaned[videogame_sales_2024_df_cleaned["genre"] != "Misc"] #Too many Nan data

    #Create year collumn
    videogame_sales_2024_df_cleaned['year'] = videogame_sales_2024_df_cleaned['release_date'].dt.year
    videogame_sales_2024_df_cleaned['year'].dropna()
    return videogame_sales_2024_df_cleaned

@st.cache_data
def load_clean_steamsales_march2025():
    steam_games_beforemarch2025 = pd.read_csv("../Dataset/games_march2025_full.csv", sep=',', decimal='.')
    steam_games_beforemarch2025_cleaned = steam_games_beforemarch2025.drop_duplicates()
    steam_games_beforemarch2025_cleaned = steam_games_beforemarch2025_cleaned.dropna(subset=['user_score', 'genres', 'estimated_owners'])

    #Clean estimated owners collumns (From "1000 - 2000" to "1500" using mean function)
    steam_games_beforemarch2025_cleaned["estimated_owners"] = steam_games_beforemarch2025_cleaned["estimated_owners"].apply(mean)

    #clean genres collumns
    steam_games_beforemarch2025_cleaned["genres"] = steam_games_beforemarch2025_cleaned["genres"].astype(str).str.strip("[]").str.replace("'", "", regex=False).str.replace('"', "", regex=False)
    steam_games_beforemarch2025_cleaned["genres"] = steam_games_beforemarch2025_cleaned["genres"].str.split(",")
    steam_games_beforemarch2025_cleaned = steam_games_beforemarch2025_cleaned.explode("genres")
    return steam_games_beforemarch2025_cleaned

# Schemas

def show_genre_market_part_by_continent(df_sales2024):
    df_sales2024 = df_sales2024.dropna(subset=['genre'])
    salesPerGenre = df_sales2024[["genre", "jp_sales", "na_sales", "pal_sales"]]
    salesPerGenre = salesPerGenre.groupby(["genre"]).sum().reset_index()
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))  # 1 ligne, 2 colonnes
    salesPerGenre = salesPerGenre.sort_values(by = "na_sales")
    axes[0].pie(salesPerGenre["na_sales"].tail(7), labels = salesPerGenre["genre"].tail(7))
    axes[0].set_title('North America')

    salesPerGenre = salesPerGenre.sort_values(by = "pal_sales")
    axes[1].pie(salesPerGenre["pal_sales"].tail(7), labels = salesPerGenre["genre"].tail(7))
    axes[1].set_title('Europe')

    salesPerGenre = salesPerGenre.sort_values(by = "jp_sales")
    axes[2].pie(salesPerGenre["jp_sales"].tail(7), labels = salesPerGenre["genre"].tail(7))
    axes[2].set_title('Japan')

    st.pyplot(fig)

def show_critics_per_genre(df_sales2024):
    criticScorePerGenre = df_sales2024.dropna(subset=['critic_score', 'genre'])
    criticScorePerGenre = criticScorePerGenre[["genre", "critic_score"]]
    criticScorePerGenre = criticScorePerGenre.groupby(["genre"]).mean().reset_index()
    colors = [(random.random(), random.random(), random.random()) for genre in criticScorePerGenre["genre"].unique()]
    fig = plt.figure()
    plt.bar(criticScorePerGenre["genre"], criticScorePerGenre["critic_score"], label="critic_score", color = colors)
    plt.xticks(rotation=90)
    plt.yticks(range(0,11,1))
    plt.xlabel("Genre")
    plt.ylabel("Mean Critic Score")
    plt.title("Mean Critic Score per genre released between 2000 and 2024")

    st.pyplot(fig)

def show_genre_by_owners_steam(df_steamsales_2025):
    # split en listes et explode
    df_steamsales_2025["genres"] = df_steamsales_2025["genres"].str.split(",")
    df_steamsales_2025_exploded = df_steamsales_2025.explode("genres")
    df_steamsales_2025_exploded["genres"] = df_steamsales_2025_exploded["genres"].str.strip()

    # groupby et tri
    salesPerGenre = df_steamsales_2025_exploded.groupby("genres")["estimated_owners"].sum().sort_values(ascending=False).head(10)

    # plot
    fig = plt.figure(figsize=(10,6))
    plt.barh(salesPerGenre.index[::-1], salesPerGenre.values[::-1])
    plt.xlabel("Estimated owners")
    plt.title("Top 10 genres by estimated owners")
    plt.tight_layout()
    
    st.pyplot(fig)


# Main

st.set_page_config(
    page_title="Home",
    page_icon="👋",
)

st.balloons()

st.title('Welcome to our Data Science TP')
st.markdown('by Matéo Erbisti, Lenny Rabinne & Antoine Mordant')

st.sidebar.success('Check our interactive panels !')
st.sidebar.write('Hi, newcomer !')
name = st.sidebar.text_input("Tell us your name !")
if (name != ""):
    st.balloons()
    st.sidebar.write('Oh hi ' + name + ' ! Feel free to explore our site !')

df_sales2024 = load_clean_sales2024()

st.subheader('Sales per continent')
show_genre_market_part_by_continent(df_sales2024)

df_steamsales_2025 = load_clean_steamsales_march2025()

st.subheader('Genre by owner (Steam 2025)')
show_genre_by_owners_steam(df_steamsales_2025)

st.subheader('Critics by genre')
show_critics_per_genre(df_sales2024)