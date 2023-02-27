import beavis
import pandas as pd
from DJSetFiller.finding_similar_songs import (
    read_data_set,
    single_song_input_reccomender,
    multiple_song_input_reccomender,
    matrix_size,
    track_analysis_from_array,
    input_feature_vector
)


def test_find_db_exists():
    collab_df = read_data_set()
    assert collab_df is not None


def test_function_working():
    collabFilter = single_song_input_reccomender(
        "5vXlU52ohBRZb1uUw4GPqA", read_data_set()
    )

    assert collabFilter is not None


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


def test_average_input_vector():
    song_ids = ["5vXlU52ohBRZb1uUw4GPqA", "5Zdmkal4CNnC5EY9qCSrMi"]
    initial_suggestions = multiple_song_input_reccomender(song_ids, read_data_set())
    input_vector = input_feature_vector(initial_suggestions)
    assert input_vector is not None
