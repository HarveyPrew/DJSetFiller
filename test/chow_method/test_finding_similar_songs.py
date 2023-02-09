from DJSetFiller.finding_similar_songs import (
    read_data_set,
    single_song_input_reccomender,
    multiple_song_input_reccomender,
    matrix_size,
)


def test_find_db_exists():
    collab_df = read_data_set()
    assert collab_df is not None


def test_function_working():
    collabFilter = single_song_input_reccomender(
        "6aYP1tSk7xBppdAuEjC4tC", read_data_set()
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
    song_ids = ["6aYP1tSk7xBppdAuEjC4tC", "5vXlU52ohBRZb1uUw4GPqA"]
    collabFilter = multiple_song_input_reccomender(song_ids, read_data_set())

    assert collabFilter is not None
