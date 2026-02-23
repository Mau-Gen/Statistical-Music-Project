import mysql.connector
import pandas as pd
from dotenv import load_dotenv
import os
from statistics import variance
from scipy import stats
import math

"""
Two independent sample hypothesis test
Group 1: Free
Group 2: Premium

Using variable duration_per_week

One sided test (Left tail)

Hypothesis: Mi Free < Mi Premium

"""

def hypothesis_test(conn):
    free_duration = pd.read_sql("""SELECT user_id, 
                                SUM(duration) / (MAX(DATE(ld.listened_at)) - MIN(DATE(ld.listened_at)) + 1)  AS duration_week
                                FROM listening_data ld
                                JOIN users ON ld.user_id = users.id
                                WHERE users.subscription = 'free'
                                GROUP BY user_id""", conn)

    print(free_duration)

    

    #premium_duration = pd.read_sql("""SELECT user_id, SUM(duration) AS duration_week""", conn)