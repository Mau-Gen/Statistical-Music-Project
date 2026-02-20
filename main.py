import mysql.connector
import pandas as pd
from dotenv import load_dotenv
import os
from descriptive import *


def connect():
    load_dotenv("passwords.env")

    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    return conn

def main():
    conn = connect() # Connect to database
    user_input = 0
    while True:
        print("Tool for analysing Spotify-data\n1) Genre popularity\n2) Fully listened songs\n3) Total user listening time\n4) User-specific information\n5) Create a new user\n9) Exit")
        user_input = int(input())
        if user_input == 1:
            genre_popularity(conn=conn)

        elif user_input == 2:
            times_fully_listened(conn=conn)
        
        elif user_input == 3:
            user_total_listened_time(conn=conn)

        elif user_input == 4:
            userinformation(conn=conn)

        elif user_input == 5:
            create_user(conn=conn)
        
        elif user_input == 9:
            exit()

        else:
            pass
            


if __name__ == "__main__":
    main()