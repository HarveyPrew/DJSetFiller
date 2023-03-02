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
    track_analysis_from_spotify
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
    assert ed is not None


def test_smallest_ed():
    song_ids = ["5vXlU52ohBRZb1uUw4GPqA", "5Zdmkal4CNnC5EY9qCSrMi"]
    initial_suggestions = multiple_song_input_reccomender(song_ids, read_data_set())
    best_song_num = reduced_similar_songs(initial_suggestions).to_dict()
    assert best_song_num["song"] == {4: 'State Of Rave (Viers Remix)'}
