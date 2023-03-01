import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import os
from sklearn.preprocessing import StandardScaler
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


def filtered_df(inital_suggestions, io):
    df = inital_suggestions.filter(items=['song_nums', 'Type', 'danceability', 'energy', 'key', 'loudness',
                                          'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness',
                                          'valence', 'tempo', 'time_signature'])
    new_df = df[df["Type"] == io].drop(columns=['Type'])
    return new_df


def input_feature_vector(inital_suggestions):
    new_df = filtered_df(inital_suggestions, 'input')
    column_averages = new_df.drop('song_nums', axis=1).mean()
    averages_list = column_averages.tolist()
    return averages_list


def output_feature_vectors(inital_suggestions):
    new_df = filtered_df(inital_suggestions, 'output')
    result = {row['song_nums']: row.drop('song_nums').tolist() for _, row in new_df.iterrows()}
    return result


def euclidean_distance(initial_suggestions):
    input = input_feature_vector(initial_suggestions)
    output = output_feature_vectors(initial_suggestions)
    output["input"] = input
    pointOutputs = []

    for i in output:
        pointOutputs.append(list(output[i]))

    scaler = StandardScaler().fit(pointOutputs)
    X_scaled = scaler.transform(pointOutputs).tolist()

    pointInput = np.array(X_scaled[-1])

    X_scaled.pop(-1)

    distanceList = []

    for point in X_scaled:
        distanceList.append(np.linalg.norm(pointInput - np.array(point)))

    ed_dict = output

    del ed_dict['input']

    z = 0

    for i in ed_dict:
        if (z == len(distanceList)):
            break

        ed_dict[i] = distanceList[z]
        z += 1

    return ed_dict


def reduced_similar_songs(initial_suggestions):
    ed = euclidean_distance(initial_suggestions)
    best_song_num = int(min(ed, key=ed.get))
    initalDf = initial_suggestions
    final_df = initalDf.loc[initalDf["song_nums"] == best_song_num]
    return final_df
