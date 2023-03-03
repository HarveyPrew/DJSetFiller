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


def matrix_size(user_song_df):
    plays = user_song_df["size"]
    user_nums = user_song_df.user_nums
    song_nums = user_song_df.song_nums
    B = coo_matrix((plays, (song_nums, user_nums))).tocsr()
    modelSize = B.shape[0] * B.shape[1]
    num_songs = len(B.nonzero()[0])
    sparsity = 100 * (1 - (num_songs / modelSize))
    return modelSize, num_songs, sparsity


def find_similar_songs(input_songs_df, num_songs, model, dataset):
    similar_songs = []

    for index, value in enumerate(input_songs_df.index):
        input_song_nums = input_songs_df['song_nums'][value]
        reccomended_song_nums = similar_song_generator(input_song_nums, num_songs, model)

        similar_songs_df = dataset[dataset.song_nums.isin(reccomended_song_nums)]
        similar_songs_df.drop_duplicates(subset=["spotify_id"], inplace=True)
        similar_songs_df["Type"] = "output"
        similar_songs_df.loc[similar_songs_df['song_nums'] == input_song_nums, ["Type"]] = 'input'
        similar_songs_df["Recommendation Number"] = index
        similar_songs.append(similar_songs_df)

    simlar_songs_list = pd.concat(similar_songs, axis=0).reset_index(drop=True)
    songs_with_features = track_analysis_from_spotify(simlar_songs_list)

    return songs_with_features


def similar_song_generator(song_ids, num_songs, model):
    songs_inds = model.similar_items(song_ids, N=num_songs)
    song_id_recs = songs_inds[0]
    return song_id_recs


def multiple_song_input_reccomender(input_song_uris, dataset, total_songs=7):

    similar_songs_total = total_songs - len(input_song_uris)
    input_songs_df = dataset[dataset['spotify_id'].isin(input_song_uris)].drop_duplicates(subset=['spotify_id'])

    plays = dataset["size"]
    user_nums = dataset.user_nums
    song_nums = dataset.song_nums

    matrix = coo_matrix((plays, (user_nums, song_nums))).tocsr()
    model = AlternatingLeastSquares(factors=100)
    model.fit(matrix)

    songs_plus_features = find_similar_songs(input_songs_df, similar_songs_total, model, dataset)

    return songs_plus_features


def track_analysis_from_spotify(similar_songs_df):
    reccomendedSongs = similar_songs_df

    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)

    analysis = []

    for id in reccomendedSongs.index:
        analysis += sp.audio_features(reccomendedSongs["spotify_id"][id])

    song_features = pd.DataFrame.from_dict(analysis).drop(["id", "analysis_url", "track_href", "uri", "type"], axis=1)

    features_plus_recs = pd.concat([reccomendedSongs, song_features], axis=1)
    return features_plus_recs


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
    input_vector = input_feature_vector(initial_suggestions)
    all_vectors = output_feature_vectors(initial_suggestions)
    all_vectors["input"] = input_vector
    pointOutputs = []

    for i in all_vectors:
        pointOutputs.append(list(all_vectors[i]))

    scaled_vectors = scaler(pointOutputs)
    scaled_input_vector = np.array(scaled_vectors[-1])

    scaled_vectors.pop(-1)

    ed_list = calculated_eds(scaled_vectors, scaled_input_vector)

    ed_dict = all_vectors

    del ed_dict['input']

    z = 0

    for i in ed_dict:
        if (z == len(ed_list)):
            break

        ed_dict[i] = ed_list[z]
        z += 1

    return ed_dict


def reduced_similar_songs(initial_suggestions):
    ed = euclidean_distance(initial_suggestions)
    best_song_num = int(min(ed, key=ed.get))
    initalDf = initial_suggestions
    final_df = initalDf.loc[initalDf["song_nums"] == best_song_num]
    return final_df


def scaler(pointOutputs):
    scaler = StandardScaler().fit(pointOutputs)
    X_scaled = scaler.transform(pointOutputs).tolist()

    return X_scaled


def calculated_eds(scaled_vectors, scaled_input_vector):
    ed_list = []

    for point in scaled_vectors:
        ed_list.append(np.linalg.norm(scaled_input_vector - np.array(point)))

    return ed_list
