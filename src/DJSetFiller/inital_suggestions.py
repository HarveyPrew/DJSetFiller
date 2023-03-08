import pandas as pd
import os
from scipy.sparse import coo_matrix
from implicit.als import AlternatingLeastSquares
from DJSetFiller.spotify_analysis import track_analysis_from_spotify

pd.options.mode.chained_assignment = None  # default='warn'


def make_recommendations_for_multiple_songs(
    input_song_uris, recommendations_per_song=6
):
    model_data = read_data_set("data/reduced/dataset_reduced.csv")

    input_songs_df = model_data[
        model_data["spotify_id"].isin(input_song_uris)
    ].drop_duplicates(subset=["spotify_id"])

    plays = model_data["size"]
    user_nums = model_data.user_nums
    song_nums = model_data.song_nums

    matrix = coo_matrix((plays, (user_nums, song_nums))).tocsr()
    model = AlternatingLeastSquares(factors=100)
    model.fit(matrix)

    songs_plus_features = find_similar_songs(
        input_songs_df, recommendations_per_song, model, model_data
    )

    return songs_plus_features


def read_data_set(path):
    dataset_df = pd.read_csv(path)

    os.environ["MKL_NUM_THREADS"] = "1"
    return dataset_df


def find_similar_songs(input_songs_df, recommendations_per_song, model, dataset):
    similar_songs = []

    for index, value in enumerate(input_songs_df.index):
        input_song_nums = input_songs_df["song_nums"][value]
        reccomended_song_nums = similar_song_generator(
            input_song_nums, recommendations_per_song, model
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


def similar_song_generator(song_ids, recommendations_per_song, model):
    number_of_similar_items = recommendations_per_song + 1
    songs_inds = model.similar_items(song_ids, N=number_of_similar_items)
    song_id_recs = songs_inds[0]
    return song_id_recs


def matrix_size(user_song_df):
    plays = user_song_df["size"]
    user_nums = user_song_df.user_nums
    song_nums = user_song_df.song_nums
    B = coo_matrix((plays, (song_nums, user_nums))).tocsr()
    modelSize = B.shape[0] * B.shape[1]
    num_songs = len(B.nonzero()[0])
    sparsity = 100 * (1 - (num_songs / modelSize))
    return modelSize, num_songs, sparsity
