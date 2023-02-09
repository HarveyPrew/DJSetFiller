from DJSetFiller.finding_similar_songs import (
    read_data_set,
    collab_filter,
    run_function,
    matrix_size
)


def test_find_db_exists():
    collab_df = read_data_set()
    assert collab_df is not None


def test_function_working():
    collabFilter = collab_filter("53TFvcQoCYaGytR1HezNlL", read_data_set())

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
