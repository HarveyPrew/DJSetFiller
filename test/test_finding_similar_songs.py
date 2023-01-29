from DJSetFiller.finding_similar_songs import read_data_set, collab_filter


def test_find_db_exists():
    collab_df = read_data_set()
    assert collab_df is not None


def test_find_song_num():
    song_num = collab_filter("6vXcHqE3bYPirOgKlDbN5s", read_data_set())
    assert song_num == 43414
