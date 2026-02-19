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