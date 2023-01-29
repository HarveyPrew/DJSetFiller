import pandas as pd
import os


def read_data_set():
    collab_df = pd.read_csv("data/mixesdb_df_for_recs.csv")
    # needed to make the training not take ages
    os.environ["MKL_NUM_THREADS"] = "1"
    return collab_df


def collab_filter(song_id, user_song_df, num_songs=5):
    """
    song_id = spotify id for individual song
    user_song_df= dataframe with users, songs, playcounts etc
    for the time being i am not going to enable filtering by key/tempo as not enough songs
    but in future will do
    """

    song_num = user_song_df[user_song_df.spotify_id == song_id].song_nums.values[0]

    return song_num
