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


def find_similar_songs(song_ids, num_songs, model, user_song_df, i, input_songs):
    z = 0
    rec_number = []
    type = []

    while z < num_songs:
        rec_number.append(i)
        type.append("output")
        z += 1

    songs_inds = model.similar_items(song_ids, N=num_songs)
    song_id_recs = songs_inds[0]

    filtered_df = user_song_df[user_song_df.song_nums.isin(song_id_recs)]
    filtered_df.drop_duplicates(subset=["spotify_id"], inplace=True)
    filtered_df['Reccomendation Number'] = rec_number

    filtered_df["Type"] = type

    filtered_df.loc[filtered_df['spotify_id'] == input_songs, "Type"] = "input"

    return filtered_df


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
    filtered_dfs = []

    i = 0

    for id in song_ids:
        filtered_dfs.append(find_similar_songs(id, num_songs, model, user_song_df, i, input_songs[i]))
        i += 1

    results = pd.concat(filtered_dfs)  
    return results
