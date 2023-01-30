from DJSetFiller.finding_similar_songs import (
    read_data_set,
    collab_filter,
    run_function,
    matrix_size,
    simple_collab_filter,
    hard_coded_output,
)


def test_len_of_arrays_same():
    songs_inds = simple_collab_filter()
    assert songs_inds is not None


def test_find_db_exists():
    collab_df = read_data_set()
    assert collab_df is not None


def test_programme_not_working():
    function = run_function("3gCiJLZj4PJfhWXzwnV7FR", read_data_set())
    assert function != "Programme not working"


def test_function_working():
    collabFilter = collab_filter("53jsOPHYPvyKjKW8kWtHVz", read_data_set())

    assert collabFilter is not None


def test_size_is_found():
    matrixSize, num_songs, sparsity = matrix_size(read_data_set())

    assert matrixSize is not None
    assert num_songs is not None
    assert sparsity is not None


def test_hard_code():
    output = hard_coded_output()
    assert output is not None
