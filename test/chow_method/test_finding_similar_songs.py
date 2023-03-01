import beavis
from io import StringIO
import pandas as pd
from DJSetFiller.finding_similar_songs import (
    read_data_set,
    multiple_song_input_reccomender,
    matrix_size,
    track_analysis_from_array,
    input_feature_vector,
    output_feature_vectors,
    euclidean_distance,
    reduced_similar_songs,
    filtered_df
)


def test_find_db_exists():
    collab_df = read_data_set()
    assert collab_df is not None


def test_size_is_found():
    matrixSize, num_songs, sparsity = matrix_size(read_data_set())

    assert matrixSize is not None
    assert num_songs is not None
    assert sparsity is not None


def test_tuple_extration():
    tuples_list = [("id_1", "score_1"), ("id_2", "score_2"), ("id_3", "score_3")]
    songs_inds = [tup[0] for tup in tuples_list]

    assert "id_1" in songs_inds
    assert "id_2" in songs_inds
    assert "score_1" not in songs_inds


def test_multiple_song_list():
    song_ids = ["5vXlU52ohBRZb1uUw4GPqA", "5Zdmkal4CNnC5EY9qCSrMi"]
    results = multiple_song_input_reccomender(song_ids, read_data_set())

    assert results is not None


def test_song_attribute():
    song_id = ["6Q3ozAXkxLpKQy6sc8L0TY"]
    results = track_analysis_from_array(song_id)

    assert results is not None


def test_matrix_returing():
    song_ids = ["5vXlU52ohBRZb1uUw4GPqA", "5Zdmkal4CNnC5EY9qCSrMi"]
    initial_suggestions = multiple_song_input_reccomender(song_ids, read_data_set())  
    assert initial_suggestions is not None


def test_euclidean_distance():
    song_ids = ["5vXlU52ohBRZb1uUw4GPqA", "5Zdmkal4CNnC5EY9qCSrMi"]
    initial_suggestions = multiple_song_input_reccomender(song_ids, read_data_set())
    ed = euclidean_distance(initial_suggestions)
    assert ed is not None


def test_smallest_ed():
    song_ids = ["5vXlU52ohBRZb1uUw4GPqA", "5Zdmkal4CNnC5EY9qCSrMi"]
    initial_suggestions = multiple_song_input_reccomender(song_ids, read_data_set())
    best_song_num = reduced_similar_songs(initial_suggestions).to_dict()
    assert best_song_num["song"] == {4: 'State Of Rave (Viers Remix)'}
