import datetime
import mysql.connector
import pandas as pd
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

from mpl_toolkits.mplot3d import Axes3D

#from sklearn import KMeans

""" Features vector = x(user) = [ total_minutes   ] - Sum of duration
                                [  unique_songs   ] - Absolute amount of song_id
                                [ unique_genres   ] - Absolute amount of genre_id
                                [ avg_duration    ] - Sum of duration / plays
                                [sessions_per_week] - Sum of plays / 7

Dim = X -> R^(n*5)

"""     




def behavior_analysis(conn):
    feature1 = pd.read_sql("SELECT user_id, SUM(duration) AS total_listened FROM listening_data GROUP by user_id", conn)
    
    feature2 = pd.read_sql("SELECT user_id, COUNT(DISTINCT song_id) AS unique_songs FROM listening_data GROUP by user_id", conn)
    
    feature3 = pd.read_sql("""SELECT user_id, COUNT(DISTINCT genre_id) AS unique_genre
                            FROM listening_data ld
                            JOIN songs ON songs.id = ld.song_id
                            JOIN artist_genre ag ON ag.artist_id = songs.artist_id
                            JOIN genre ON genre.id = ag.genre_id
                            GROUP by user_id""", conn)

    feature4 = pd.read_sql("""
                            SELECT user_id,
                            SUM(duration) / COUNT(*) AS avg_duration
                            FROM listening_data
                            GROUP BY user_id""", conn)

    feature5 = pd.read_sql("""
                            SELECT user_id,
                            COUNT(*) / ((DATEDIFF(MAX(listened_at), MIN(listened_at)) / 7) + 1) AS sessions_per_week
                            FROM listening_data
                            GROUP BY user_id""", conn)

    for f in (feature1, feature2, feature3, feature4, feature5):
        f.set_index("user_id", inplace=True)

    df = pd.concat([feature1, feature2, feature3, feature4, feature5], axis=1)

    x = df[["total_listened", "unique_songs", "unique_genre", "avg_duration", "sessions_per_week"]]

    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x)
    print(x_scaled)

    amount_cluster = 3

    kmeans = KMeans(n_clusters=amount_cluster, random_state=42)
    labels = kmeans.fit_predict(x_scaled)

    

    df_analysis = x.copy()
    df_analysis["cluster"] = labels

    print(df_analysis.groupby("cluster").mean())

    
    pca = PCA(n_components=2)

    X_pca = pca.fit_transform(x_scaled)

    plt.figure(figsize=(8,6))

    for c in range(amount_cluster):
        plt.scatter(
            X_pca[labels == c, 0],
            X_pca[labels == c, 1],
            label=f"Cluster {c}"
        )

    print(x.corr())

    print('\n')
    print(pca.explained_variance_ratio_)
    print(f'\n Sum\n', pca.explained_variance_ratio_.sum())

    # Only to see what PCA 3 would have done
    print("\nSum with 3 components:")
    print(PCA(n_components=3).fit(x_scaled).explained_variance_ratio_.sum())


    plt.legend()
    plt.title("KMeans (K=3)")
    plt.xlabel("PCA 1")
    plt.ylabel("PCA 2")
    plt.show()



    # -------- 3D PCA --------

    pca3 = PCA(n_components=3)
    X_pca3 = pca3.fit_transform(x_scaled)

    from mpl_toolkits.mplot3d import Axes3D

    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111, projection='3d')

    for c in np.unique(labels):
        ax.scatter(
            X_pca3[labels == c, 0],
            X_pca3[labels == c, 1],
            X_pca3[labels == c, 2],
            label=f"Cluster {c}"
        )

    ax.set_xlabel("PCA 1")
    ax.set_ylabel("PCA 2")
    ax.set_zlabel("PCA 3")
    ax.set_title("KMeans (3D PCA)")
    ax.legend()

    plt.show()











