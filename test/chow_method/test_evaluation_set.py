from DJSetFiller.evaluation_set import (
    input_test_songs,
    organise_missing_songs
)


def test_input_test():
    input = input_test_songs()

    assert input is not None


def test_missing_songs():
    missing_songs = organise_missing_songs()

    assert missing_songs is not None
