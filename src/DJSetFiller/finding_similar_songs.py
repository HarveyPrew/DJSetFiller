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
        collab_filter(song_id, user_song_df, num_songs=5)
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


def simple_collab_filter():
    user_nums = [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        2,
        2,
        2,
        2,
        2,
    ]
    song_nums = [
        17,
        1,
        2,
        3,
        4,
        5,
        6,
        17,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        4,
        2,
        9,
        15,
        16,
    ]
    size = [
        2,
        2,
        3,
        2,
        3,
        2,
        2,
        2,
        2,
        3,
        2,
        3,
        2,
        2,
        1,
        1,
        2,
        1,
        1,
        1,
        1,
        3,
        3,
        2,
        1,
        1,
    ]

    B = coo_matrix((size, (user_nums, song_nums))).tocsr()

    model = AlternatingLeastSquares(factors=100)

    model.fit(B)
    songs_inds = model.similar_items(2, N=6)
    return songs_inds[0]


def hard_coded_output():
    songs_inds = [232, 16278, 2127, 1106, 5197]
    user_song_df = read_data_set()
    filtered_df = user_song_df[user_song_df.song_nums.isin(songs_inds)]

    filtered_df.drop_duplicates(subset=["spotify_id"], inplace=True)

    return filtered_df
