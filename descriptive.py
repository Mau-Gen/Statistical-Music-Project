import datetime
import mysql.connector
import pandas as pd
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import numpy as np

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

    plt.barh(genres_label, listening_time)
    plt.title('Genre popularity')
    plt.xlabel('Amount of listening time')
    plt.ylabel('Genres')
    plt.show()



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