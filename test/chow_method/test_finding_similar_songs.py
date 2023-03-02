import beavis
from io import StringIO
import pandas as pd
from DJSetFiller.finding_similar_songs import (
    read_data_set,
    multiple_song_input_reccomender,
    matrix_size,
    input_feature_vector,
    output_feature_vectors,
    euclidean_distance,
    reduced_similar_songs,
    filtered_df,
    track_analysis_from_spotify,
    scaler,
    calculated_eds
)


def test_find_db_exists():
    collab_df = read_data_set()
    collab_df_dict = collab_df.to_dict()
    assert len(collab_df_dict) == 10


def test_size_is_found():
    matrixSize, num_songs, sparsity = matrix_size(read_data_set())

    assert matrixSize == 54
    assert num_songs == 26
    assert sparsity > 50


def test_tuple_extration():
    tuples_list = [("id_1", "score_1"), ("id_2", "score_2"), ("id_3", "score_3")]
    songs_inds = [tup[0] for tup in tuples_list]

    assert "id_1" in songs_inds
    assert "id_2" in songs_inds
    assert "score_1" not in songs_inds


def test_multiple_song_list():
    song_ids = ["5vXlU52ohBRZb1uUw4GPqA", "5Zdmkal4CNnC5EY9qCSrMi"]
    results = multiple_song_input_reccomender(song_ids, read_data_set())

    assert len(results) == 10


def test_song_attribute():
    dataset = {'artist': {0: '11:11'}, 'song': {0: 'West Side'}, 'spotify_song_name': {0: 'West Side'}, 'spotify_id': {0: '15Hy4NsbvkcSygqXC2vZdL'},
               'preview': {0: '15Hy4NsbvkcSygqXC2vZdL'}, 'songs': {0: 'West Side'}, 'set_title_split': {0: 'West Side'},
               'user_nums': {0: 0}, 'song_nums': {0: 17}, 'size': {0: 1}}
    test = pd.DataFrame.from_dict(dataset)
    results = track_analysis_from_spotify(test).to_dict()

    assert results['tempo'] == {0: 178.345}


def test_matrix_returing():
    song_ids = ["5vXlU52ohBRZb1uUw4GPqA", "5Zdmkal4CNnC5EY9qCSrMi"]
    initial_suggestions = multiple_song_input_reccomender(song_ids, read_data_set())
    results = initial_suggestions.to_dict()
    assert results['song'][0] == 'Lifted'


def test_euclidean_distance():
    song_ids = ["5vXlU52ohBRZb1uUw4GPqA", "5Zdmkal4CNnC5EY9qCSrMi"]
    initial_suggestions = multiple_song_input_reccomender(song_ids, read_data_set())
    ed = euclidean_distance(initial_suggestions)
    assert ed[4.0] == 4.11614363824532


def test_smallest_ed():
    song_ids = ["5vXlU52ohBRZb1uUw4GPqA", "5Zdmkal4CNnC5EY9qCSrMi"]
    initial_suggestions = multiple_song_input_reccomender(song_ids, read_data_set())
    best_song_num = reduced_similar_songs(initial_suggestions).to_dict()
    assert best_song_num["song"] == {4: 'State Of Rave (Viers Remix)'}


def test_scaler():
    vectors = [[0.817, 0.975, 4.0, -6.946, 0.0, 0.0681, 0.000677, 0.806, 0.0904, 0.125, 120.013, 4.0],
               [0.729, 0.481, 10.0, -15.041, 0.0, 0.0699, 0.000392, 0.827, 0.13, 0.649, 130.188, 4.0]]
    
    output = scaler(vectors)

    assert output[0] == [1.0000000000000013, 1.0, -1.0, 1.0000000000000002, 0.0,
                         -1.0000000000000078, 0.9999999999999997, -1.0,
                         -0.9999999999999997, -1.0, -1.0, 0.0]


def test_input_vector():
    song_ids = ["5vXlU52ohBRZb1uUw4GPqA", "5Zdmkal4CNnC5EY9qCSrMi"]
    initial_suggestions = multiple_song_input_reccomender(song_ids, read_data_set())
    output = input_feature_vector(initial_suggestions)

    assert output == [0.6145, 0.705, 2.5, -9.8355, 0.0, 0.057800000000000004,
                      0.015175000000000001, 0.5955, 0.3855, 0.16165, 128.481, 4.0]
    

def test_output_vector():
    song_ids = ["5vXlU52ohBRZb1uUw4GPqA", "5Zdmkal4CNnC5EY9qCSrMi"]
    initial_suggestions = multiple_song_input_reccomender(song_ids, read_data_set())
    output = output_feature_vectors(initial_suggestions)

    assert output[4.0][00] == 0.817


def test_calulate_ed():
    scaled_input_vector = [-1.101666184549665, -0.6038365812770807, -1.386750490563073,
                           -0.1786817247259729, -0.35355339059327373, -0.32126955046767547,
                           -0.43658906602088027, -0.14817291368239394, 1.1117217421481622,
                           -0.7745848205398156, -0.06718260020110874, 0.3535533905932739]
    scaled_vectors = {0: [1.1492156779411027, 1.2189247758698838, -0.9707253433941511,
                          0.7467728843880046, -0.35355339059327373, -0.12800746527394744,
                          -0.5920076802169513, 0.4376730176951285, -0.6120343294096077,
                          -0.923146748121545, -2.103015732020797, 0.3535533905932739],
                      1: [0.1710546710315345, -2.116053410910118, 0.6933752452815365,
                          -1.8459092615810726, -0.35355339059327373, -0.09423350863815007,
                          -0.5950628812823313, 0.4961184550297029, -0.38072040045776867,
                          1.2009037308095927, 0.34320558544086094, 0.3535533905932739]}
    
    ed_list = calculated_eds(scaled_vectors, scaled_input_vector)

    assert ed_list == [2.4371070571105045, 5.074792132450041]
