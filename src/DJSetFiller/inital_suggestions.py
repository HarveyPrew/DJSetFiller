import pandas as pd
import os
from scipy.sparse import coo_matrix
from implicit.als import AlternatingLeastSquares
import DJSetFiller.spotify_analysis as spotify

pd.options.mode.chained_assignment = None  # default='warn'


def make_recommendations_for_dj_set(dj_set, model, model_data):
    return make_recommendations_for_multiple_songs(
        dj_set.input_songs, model, model_data
    )


def make_recommendations_for_multiple_songs(
    input_song_ids, model, model_data, recommendations_per_song=200
):

    input_songs_df = model_data[
        model_data["spotify_id"].isin(input_song_ids)
    ].drop_duplicates(subset=["spotify_id"])

    songs_plus_features = find_similar_songs_for_input_set(
        input_songs_df, recommendations_per_song, model, model_data
    )

    return songs_plus_features


def create_model(model_path):
    model_data = read_data_set(model_path)

    plays = model_data["dj_play_count"]
    dj_id = model_data.dj_id
    song_id = model_data.song_id

    matrix = coo_matrix((plays, (dj_id, song_id))).tocsr()
    model = AlternatingLeastSquares(factors=100)
    model.fit(matrix)
    return model, model_data


def read_data_set(path):
    dataset_df = pd.read_csv(path)

    os.environ["MKL_NUM_THREADS"] = "1"
    return dataset_df


def find_similar_songs_for_input_set(
    input_songs_df, recommendations_per_song, model, dataset
):
    similar_songs = []

    for index, value in enumerate(input_songs_df.index):
        input_song_id = input_songs_df["song_id"][value]
        recommended_song_ids = find_similar_songs_for_single_input(
            input_song_id, recommendations_per_song, model
        )

        similar_songs_df = dataset[dataset.song_id.isin(recommended_song_ids)]
        similar_songs_df.drop_duplicates(subset=["spotify_id"], inplace=True)
        similar_songs_df["Type"] = "output"
        similar_songs_df.loc[
            similar_songs_df["song_id"] == input_song_id, ["Type"]
        ] = "input"
        similar_songs.append(similar_songs_df)

    similar_songs_list = pd.concat(similar_songs, axis=0).reset_index(drop=True)
    similar_songs_list.drop_duplicates(subset=["spotify_id", "Type"], inplace=True)
    similar_songs_list.drop_duplicates(subset=["spotify_id"], inplace=True)

    songs_with_features = spotify.api_client.get_spotify_features(similar_songs_list)

    return songs_with_features


def find_similar_songs_for_single_input(song_ids, recommendations_per_song, model):
    number_of_similar_items = recommendations_per_song + 1
    songs_inds = model.similar_items(song_ids, N=number_of_similar_items)
    song_id_recs = songs_inds[0]
    return song_id_recs


def matrix_size(user_song_df):
    plays = user_song_df["dj_play_count"]
    dj_id = user_song_df.dj_id
    song_id = user_song_df.song_id
    B = coo_matrix((plays, (song_id, dj_id))).tocsr()
    modelSize = B.shape[0] * B.shape[1]
    num_songs = len(B.nonzero()[0])
    sparsity = 100 * (1 - (num_songs / modelSize))
    return modelSize, num_songs, sparsity
