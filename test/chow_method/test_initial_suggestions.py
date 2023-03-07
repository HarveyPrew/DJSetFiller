from DJSetFiller.inital_suggestions import (
    multiple_song_input_reccomender,
    read_data_set,
    matrix_size
)


def test_multiple_song_list():
    uri_list = ["5vXlU52ohBRZb1uUw4GPqA", "5Zdmkal4CNnC5EY9qCSrMi"]
    results = multiple_song_input_reccomender(uri_list)

    assert len(results) == 14


def test_find_db_exists():
    collab_df = read_data_set()
    collab_df_dict = collab_df.to_dict()
    assert len(collab_df_dict) == 10


def test_size_is_found():
    matrixSize, num_songs, sparsity = matrix_size(read_data_set())

    assert matrixSize == 54
    assert num_songs == 26
    assert sparsity > 50
