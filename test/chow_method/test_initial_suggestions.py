from DJSetFiller.inital_suggestions import (
    multiple_song_input_reccomender
)


def test_multiple_song_list():
    uri_list = ["5vXlU52ohBRZb1uUw4GPqA", "5Zdmkal4CNnC5EY9qCSrMi"]
    results = multiple_song_input_reccomender(uri_list)

    assert len(results) == 14


def test_matrix_returing():
    uri_list = ["5vXlU52ohBRZb1uUw4GPqA", "5Zdmkal4CNnC5EY9qCSrMi"]
    initial_suggestions = multiple_song_input_reccomender(uri_list)
    results = initial_suggestions.to_dict()
    assert results is not None

