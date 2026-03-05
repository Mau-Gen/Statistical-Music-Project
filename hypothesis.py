import mysql.connector
import math
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
from dotenv import load_dotenv
from statistics import variance
from scipy import stats
from scipy.stats import t

"""
Following function is used to see if premium users listens more than free users. 

Two independent sample hypothesis test
Group 1: Free
Group 2: Premium

Using variable duration_per_week
One sided test (Left tail) 

Hypothesis: Mi Free < Mi Premium

"""

def hypothesis_test(conn):
    free_duration = pd.read_sql("""SELECT user_id, 
                                7 * SUM(duration) / (MAX(DATE(ld.listened_at)) - MIN(DATE(ld.listened_at)) + 1)  AS duration_week
                                FROM listening_data ld
                                JOIN users ON ld.user_id = users.id
                                WHERE users.subscription = 'free'
                                GROUP BY user_id""", conn)

    print(free_duration)

    premium_duration = pd.read_sql("""SELECT user_id, 
                                7 * SUM(duration) / (MAX(DATE(ld.listened_at)) - MIN(DATE(ld.listened_at)) + 1) AS duration_week
                                FROM listening_data ld
                                JOIN users ON ld.user_id = users.id
                                WHERE users.subscription = 'premium'
                                GROUP BY user_id""", conn)


    x_mean, y_mean = free_duration.duration_week.mean(), premium_duration.duration_week.mean()
    x_var, y_var = variance(free_duration.duration_week), variance(premium_duration.duration_week)

    x_len, y_len = len(free_duration), len(premium_duration)    

    dom = math.sqrt( (x_var/x_len) + (y_var/y_len) ) 

    t_value = (x_mean - y_mean) / dom

    df = dom**4 / ((((x_var / x_len)**2) / (x_len - 1)) + (((y_var / y_len)**2) / (y_len - 1)))

    t_crit = stats.t.ppf(0.05, df)

    if t_value < t_crit:
        decision = 'Reject H0'
    else:
        decision = 'Failed to reject H0'


    x = np.linspace(-4, 4, 1000)
    y = t.pdf(x, df)

    fig = plt.figure(figsize=(8,5))
    plt.plot(x, y)


    plt.fill_between(x, y, where=(x <= t_crit), alpha=0.3, label="Rejection region")

    plt.axvline(t_value, linestyle="--", label=f"t = {t_value}")
    plt.axvline(t_crit, linestyle=":", label=f"t_crit = {t_crit}")
    plt.axvline(0, linestyle="-", color="Black", alpha=0.3)

    plt.title(f"Hypothesis test with the following statement\n'Do premium users listens more than free users?'")
    
    plt.xlabel(decision, fontsize=12)
    plt.legend()
    
    return fig