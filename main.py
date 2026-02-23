import mysql.connector
import pandas as pd
from dotenv import load_dotenv
import os
from descriptive import *
from clustering import *
from hypothesis import *

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
<<<<<<< Updated upstream
        print("Tool for analysing Spotify-data\n1) Genre popularity\n2) Fully listened songs\n3) Total user listening time\n4) User-specific information\n9) Exit")
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
            behavior_analysis(conn=conn)

        elif user_input == 6:
            hypothesis_test(conn=conn)
        else:
            exit()
        
=======
        print("Tool for analysing Spotify-data\n1) Genre popularity\n2) Behavior analysis\n3) Hypothesis\n9) Exit")
        user_input = int(input())
        if user_input == 1:
            genre_popularity(conn=conn)
        elif user_input == 2:
            behavior_analysis(conn=conn)
        elif user_input == 3:
            hypothess_test(conn=conn)
>>>>>>> Stashed changes
        elif user_input == 9:
            exit()

        else:
            pass
            


if __name__ == "__main__":
    main()