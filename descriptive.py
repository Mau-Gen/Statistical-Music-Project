import datetime
import mysql.connector
import pandas as pd
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import numpy as np
import warnings
from matplotlib import ticker

warnings.filterwarnings('ignore', category=UserWarning, module='pandas')

#from sklearn import KMeans ?



# Bar chart for popularity of genres by listening time (Descending order)
def genre_popularity(conn):

    popular_genres = pd.read_sql("""
                            SELECT 
                                genre.genre_name,
                                COUNT(*) AS total_listens
                            FROM listening_data ld
                            JOIN songs ON songs.id = ld.song_id
                            JOIN artist_genre ag ON ag.artist_id = songs.artist_id
                            JOIN genre ON genre.id = ag.genre_id
                            GROUP BY genre.genre_name
                            ORDER BY total_listens DESC""", conn)


    print(popular_genres)
    genres_label = popular_genres["genre_name"]
    listening_time = popular_genres["total_listens"]

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.barh(genres_label, listening_time)
    ax.set_title("Genre popularity")
    ax.set_xlabel("Amount of listening time")
    ax.set_ylabel("Genres")

    return fig



#print(popular_genres)

#user_sub = pd.read_sql("SELECT username FROM users WHERE subscription = 'premium'", conn)
#print(user_sub)

# Songs listened with premium account

#amount_pre = pd.read_sql("SELECT COUNT(*) FROM users INNER JOIN listening_data WHERE users.id = listening_data.user_id AND users.subscription = 'family'", conn)
#print(amount_pre)

#df = pd.read_sql("SELECT listened_at FROM listening_data WHERE user_id = 68", conn)
#print(df)
#duration = df["listened_at"]

#print(f"Average listening time", ((duration.mean()) / 60))

def top_10_songs_this_month(conn):
    amount_songs = pd.read_sql("""
                    SELECT
                        songs.song_name,
                        monthly_listeners AS times
                    FROM songs
                    ORDER BY times DESC LIMIT 10""", conn)
    
    print(amount_songs)

    fig, ax = plt.subplots(figsize=(8, 6), tight_layout=True)
    bars = ax.bar(amount_songs["song_name"], amount_songs["times"], color="green")
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.yaxis.get_major_formatter().set_scientific(False)

    min_val = amount_songs["times"].min()
    max_val = amount_songs["times"].max()

    diff = max_val - min_val

    padding = diff * 0.15 if diff > 0 else min_val * 0.001

    ax.set_ylim(bottom= min_val - padding, top = max_val + padding)
    ax.bar_label(bars, fmt="{:,.0f}", padding=3)

    ax.set_title("Top 10 Songs With Most Monthly Listeners")
    plt.xticks(rotation=45, ha="right")
    return fig


def user_total_listened_time(conn):
    total_time = pd.read_sql("""
                        SELECT
                            users.username,
                            SUM(ld.duration) AS total_time,
                            users.subscription
                        FROM users
                        JOIN listening_data ld ON users.id = ld.user_id
                        GROUP BY users.username, users.subscription
                        ORDER BY total_time DESC LIMIT 15""", conn)
    
    fig, ax = plt.subplots(figsize=(8, 6), tight_layout=True)
    ax.pie(total_time["total_time"], labels=total_time["username"], autopct="%1.1f%%")
    ax.set_title("Top 15 Users In Total Listening Time")
    return fig

def get_users_stats(conn):
    stats = pd.read_sql("""
                            SELECT 
                                COUNT(*) as total, MAX(id) as max_id
                            FROM users
                            """, conn)

    exact_total = stats.iloc[0]['total']
    max_id = stats.iloc[0]['max_id']
    return exact_total, max_id

def get_user_info(conn, user_id):
    user = pd.read_sql("""
                    SELECT
                       *
                    FROM users
                    WHERE users.id = %s
                    """, conn, params=(user_id,))
    return user

def create_a_user_gui(conn, name, sub_type):

    cursor = conn.cursor()

    try:
        args = (name, sub_type)

        cursor.callproc("CreateAUser", args)

        conn.commit()

        print(f"User {name} created successfully!")
        return True, f"User {name} created!"

    except Exception as e:
        conn.rollback()
        return False, str(e)

    finally:
        cursor.close()