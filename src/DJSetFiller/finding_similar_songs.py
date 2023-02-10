import pandas as pd
import os
from scipy.sparse import coo_matrix
from implicit.als import AlternatingLeastSquares


def read_data_set():
    collab_df = pd.read_csv("data/dateset_reduced.csv")

    os.environ["MKL_NUM_THREADS"] = "1"
    return collab_df


def single_song_input_reccomender(song_id, user_song_df, num_songs=5):

    song_num = user_song_df[user_song_df.spotify_id == song_id].song_nums.values[0]

    user_song_refined = user_song_df

    plays = user_song_refined["size"]
    user_nums = user_song_refined.user_nums
    song_nums = user_song_refined.song_nums

    B = coo_matrix((plays, (user_nums, song_nums))).tocsr()

    model = AlternatingLeastSquares(factors=30)

    model.fit(B)
    songs_inds = model.similar_items(song_num, N=num_songs)
    song_id_recs = songs_inds[0]

    filtered_df = user_song_df[user_song_df.song_nums.isin(song_id_recs)]
    filtered_df.drop_duplicates(subset=["spotify_id"], inplace=True)

    return filtered_df


def run_function(song_id, user_song_df, num_songs=5):
    try:
        single_song_input_reccomender(song_id, user_song_df, num_songs=5)
    except IndexError:
        return "Programme not working"


def matrix_size(user_song_df):
    plays = user_song_df["size"]
    user_nums = user_song_df.user_nums
    song_nums = user_song_df.song_nums
    B = coo_matrix((plays, (song_nums, user_nums))).tocsr()
    modelSize = B.shape[0] * B.shape[1]
    num_songs = len(B.nonzero()[0])
    sparsity = 100 * (1 - (num_songs / modelSize))
    return modelSize, num_songs, sparsity


def multiple_song_input_reccomender(input_songs, user_song_df, num_songs=5):

    song_ids = []
    for id in input_songs:
        song_ids.append(user_song_df[user_song_df.spotify_id == id].song_nums.values[0])

    user_song_refined = user_song_df

    plays = user_song_refined["size"]
    user_nums = user_song_refined.user_nums
    song_nums = user_song_refined.song_nums

    B = coo_matrix((plays, (user_nums, song_nums))).tocsr()

    model = AlternatingLeastSquares(factors=30)

    model.fit(B)
    
    songs_inds_1 = model.similar_items(song_ids[0], N=num_songs)
    song_id_recs_1 = songs_inds_1[0]

    filtered_df_1 = user_song_df[user_song_df.song_nums.isin(song_id_recs_1)]
    filtered_df_1.drop_duplicates(subset=["spotify_id"], inplace=True)

    songs_inds_2 = model.similar_items(song_ids[1], N=num_songs)
    song_id_recs_2 = songs_inds_2[0]

    filtered_df_2 = user_song_df[user_song_df.song_nums.isin(song_id_recs_2)]
    filtered_df_2.drop_duplicates(subset=["spotify_id"], inplace=True)

    return filtered_df_1, filtered_df_2
