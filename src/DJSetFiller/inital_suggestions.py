import pandas as pd
import os
from scipy.sparse import coo_matrix
from implicit.als import AlternatingLeastSquares
from DJSetFiller.spotify_analysis import track_analysis_from_spotify

pd.options.mode.chained_assignment = None  # default='warn'


def multiple_song_input_reccomender(input_song_uris, total_songs=7):

    dataset = read_data_set()

    input_songs_df = dataset[
        dataset["spotify_id"].isin(input_song_uris)
    ].drop_duplicates(subset=["spotify_id"])

    plays = dataset["size"]
    user_nums = dataset.user_nums
    song_nums = dataset.song_nums

    matrix = coo_matrix((plays, (user_nums, song_nums))).tocsr()
    model = AlternatingLeastSquares(factors=100)
    model.fit(matrix)

    songs_plus_features = find_similar_songs(
        input_songs_df, total_songs, model, dataset
    )

    return songs_plus_features


def read_data_set():
    collab_df = pd.read_csv("data/reduced/dataset_reduced.csv")

    os.environ["MKL_NUM_THREADS"] = "1"
    return collab_df


def find_similar_songs(input_songs_df, similar_songs_total, model, dataset):
    similar_songs = []

    for index, value in enumerate(input_songs_df.index):
        input_song_nums = input_songs_df["song_nums"][value]
        reccomended_song_nums = similar_song_generator(
            input_song_nums, similar_songs_total, model
        )

        similar_songs_df = dataset[dataset.song_nums.isin(reccomended_song_nums)]
        similar_songs_df.drop_duplicates(subset=["spotify_id"], inplace=True)
        similar_songs_df["Type"] = "output"
        similar_songs_df.loc[
            similar_songs_df["song_nums"] == input_song_nums, ["Type"]
        ] = "input"
        similar_songs_df["Recommendation Number"] = index
        similar_songs.append(similar_songs_df)

    simlar_songs_list = pd.concat(similar_songs, axis=0).reset_index(drop=True)
    songs_with_features = track_analysis_from_spotify(simlar_songs_list)

    return songs_with_features


def similar_song_generator(song_ids, num_songs, model):
    songs_inds = model.similar_items(song_ids, N=num_songs)
    song_id_recs = songs_inds[0]
    return song_id_recs

