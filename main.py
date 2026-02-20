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
        print("Tool for analysing Spotify-data\n1) Genre popularity\n9) Exit")
        user_input = int(input())
        if user_input == 1:
            genre_popularity(conn=conn)
        
        elif user_input == 9:
            exit()

        else:
            pass
            


if __name__ == "__main__":
    main()