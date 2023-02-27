import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import os
from scipy.sparse import coo_matrix
from implicit.als import AlternatingLeastSquares
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'


def read_data_set():
    collab_df = pd.read_csv("data/dataset_reduced.csv")

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

    whole_df = track_analysis_from_pandas(filtered_df)
    
    return whole_df


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

    song_id_recs = similar_song_generator(song_ids, num_songs, model)
    df_with_type = type_implementation(user_song_df, song_id_recs, rec_number, input_songs, type)
    results = track_analysis_from_pandas(df_with_type)

    return results


def similar_song_generator(song_ids, num_songs, model):
    songs_inds = model.similar_items(song_ids, N=num_songs)
    song_id_recs = songs_inds[0]
    return song_id_recs


def type_implementation(user_song_df, song_id_recs, rec_number, input_songs, type):
    filtered_df = user_song_df[user_song_df.song_nums.isin(song_id_recs)]
    filtered_df.drop_duplicates(subset=["spotify_id"], inplace=True)
    filtered_df["Reccomendation Number"] = rec_number

    filtered_df["Type"] = type
    filtered_df.loc[filtered_df["spotify_id"] == input_songs, "Type"] = "input"
    filtered_df.sort_values("Type")
    return filtered_df


def multiple_song_input_reccomender(input_songs, user_song_df, num_songs=5):

    song_ids = []
    for id in input_songs:
        song_ids.append(user_song_df[user_song_df.spotify_id == id].song_nums.values[0])

    user_song_refined = user_song_df

    plays = user_song_refined["size"]
    user_nums = user_song_refined.user_nums
    song_nums = user_song_refined.song_nums

    matrix = coo_matrix((plays, (user_nums, song_nums))).tocsr()
    model = AlternatingLeastSquares(factors=100)
    model.fit(matrix)
    filtered_dfs = []

    i = 0

    for id in song_ids:
        filtered_dfs.append(
            find_similar_songs(id, num_songs, model, user_song_df, i, input_songs[i])
        )
        i += 1

    results = pd.concat(filtered_dfs)
    return results


def track_analysis_from_pandas(filtered_df):
    reccomendedSongs = filtered_df.reset_index()
    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)

    analysis = []

    for id in reccomendedSongs.index:
        analysis += sp.audio_features(reccomendedSongs["spotify_id"][id])

    song_features = pd.DataFrame.from_dict(analysis).drop(["id", "analysis_url", "track_href", "uri", "type"], axis=1)

    features_plus_recs = pd.concat([reccomendedSongs, song_features], axis=1)
    return features_plus_recs


def track_analysis_from_array(song_id):
    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)

    analysis = sp.audio_features(song_id)

    return analysis


def song_features_matrix(inital_suggestions):

    song_nums = inital_suggestions.song_nums
    B = coo_matrix((plays, (song_nums, user_nums))).tocsr()


def input_feature_vector(inital_suggestions):
    df = inital_suggestions.filter(items=['song_nums', 'Type', 'danceability', 'energy', 'key', 'loudness',
                                          'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness',
                                          'valence', 'tempo', 'duration', 'time_signature'])
    new_df = df[df["Type"] == "input"].drop(columns=['Type'])
    column_averages = new_df.drop('song_nums', axis=1).mean()
    averages_list = column_averages.tolist()
    return averages_list


def output_feature_vectors(inital_suggestions):
    df = inital_suggestions.filter(items=['song_nums', 'Type', 'danceability', 'energy', 'key', 'loudness',
                                          'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness',
                                          'valence', 'tempo', 'duration', 'time_signature'])
    new_df = df[df["Type"] == "output"].drop(columns=['Type'])
    result = {row['song_nums']: row.drop('song_nums').tolist() for _, row in new_df.iterrows()}
    return result


def euclidean_distance(input_feature_vector, output_feature_vectors):
    pointInput = np.array(input_feature_vector)
    pointOutputs = []

    for i in output_feature_vectors:
        pointOutputs.append(np.array(list(output_feature_vectors[i])))
 
    distanceList = []

    for point in pointOutputs:
        distanceList.append(np.linalg.norm(pointInput - point))

    return distanceList
