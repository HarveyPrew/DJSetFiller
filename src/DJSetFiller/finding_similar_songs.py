import pandas as pd
import os
from scipy.sparse import coo_matrix
from implicit.als import AlternatingLeastSquares


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

    user_song_refined = user_song_df

    # count_series = user_song_df.groupby(["user_nums", "song_nums"]).size()
    # user_plays = count_series.to_frame(name="plays").reset_index()
    # plays = user_plays["plays"]

    plays = user_song_refined["size"]
    user_nums = user_song_refined.user_nums
    song_nums = user_song_refined.song_nums

    B = coo_matrix((plays, (song_nums, user_nums))).tocsr()

    model = AlternatingLeastSquares(factors=30)

    model.fit(B)
    songs_inds = model.similar_items(song_num, N=num_songs)
    songs_inds = [tup[0] for tup in songs_inds]

    filtered_df = user_song_df[user_song_df.song_nums.isin(songs_inds)]
    filtered_df.drop_duplicates(subset=["spotify_id"], inplace=True)

    return song_nums, user_nums, plays, B, model, songs_inds, filtered_df
