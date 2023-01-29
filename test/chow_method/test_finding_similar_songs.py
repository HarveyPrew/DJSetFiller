from DJSetFiller.finding_similar_songs import read_data_set, collab_filter


def test_find_db_exists():
    collab_df = read_data_set()
    assert collab_df is not None


def test_find_song_attributes():
    song_nums, user_nums, plays, B, model, songs_inds = collab_filter(
        "53TFvcQoCYaGytR1HezNlL", read_data_set()
    )
    assert song_nums is not None
    assert user_nums is not None
    assert plays is not None
    assert B is not None
    assert model is not None
    assert songs_inds is not None
