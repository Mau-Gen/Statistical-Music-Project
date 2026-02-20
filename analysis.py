import mysql.connector
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv("passwords.env")

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

df = pd.read_sql("SELECT * FROM users", conn)
print(df)

listening_data  = pd.read_sql("SELECT duration FROM listening_data", conn)
print(listening_data)

song_duration =  pd.read_sql("SELECT songs.id FROM songs JOIN listening_data ON songs.id = listening_data.song_id WHERE songs.duration = listening_data.duration", conn)
print(song_duration)