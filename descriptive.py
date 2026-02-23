import datetime
import mysql.connector
import pandas as pd
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import numpy as np
import warnings

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

def times_fully_listened(conn):
    amount_songs = pd.read_sql("""
                    SELECT
                        songs.song_name,
                        COUNT(*) AS times
                    FROM songs
                    JOIN listening_data ld ON ld.song_id = songs.id
                    WHERE ld.duration = songs.duration
                    GROUP BY songs.song_name
                    ORDER BY amount DESC""", conn)
    print(amount_songs)


def user_total_listened_time(conn):
    total_time = pd.read_sql("""
                        SELECT
                            users.username,
                            SUM(ld.duration) AS total_time,
                            users.subscription
                        FROM users
                        JOIN listening_data ld ON users.id = ld.user_id
                        GROUP BY users.username, users.subscription
                        ORDER BY total_time""", conn)
    print(total_time)

def userinformation(conn):
    while True:
        try:
            stats = pd.read_sql("""
                            SELECT 
                                COUNT(*) as total, MAX(id) as max_id
                            FROM users
                            """, conn)

            exact_total = stats.iloc[0]['total']
            max_id = stats.iloc[0]['max_id']

            print(f"\n--- USER INFORMATION (Total users: {exact_total}) ---")

            check = input("Would you like to create a new user or view information about a user?\n1) View information\n2) Create a user\n3) Exit\n")

            if check == '1':
                id = int(input(f"Which user id from 1-{max_id} do you want to view? "))
                user = pd.read_sql("""
                                SELECT
                                   *
                                FROM users
                                WHERE users.id = %s
                                    """, conn, params=(id,))
                if user.empty:
                    print(f"No user found with ID {id}")
                else:
                    print(user)

            elif check == '2':
                create_a_user(conn=conn)

            elif check == '3':
                print("Exiting to main menu...")
                break

            else:
                print("Invalid selection, try again.")
        
        except ValueError:
            print("Please enter a valid number.")

        except Exception as e:
            print(f"An error occured: {e}")
            break
    

def create_a_user(conn):
    name = str(input("What username would you like to have? "))
    sub_type = str(input("What subscription would you like to have?\n1) free\n2) premium\n3) family\n"))

    cursor = conn.cursor()

    try:
        args = (name, sub_type)

        cursor.callproc("CreateAUser", args)

        conn.commit()

        print(f"User {name} created successfully!")

    except Exception as e:
        print(f"Something went wrong: {e}")
        conn.rollback()

    finally:
        cursor.close()