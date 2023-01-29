from DJSetFiller.finding_similar_songs import read_data_set


def test_find_db_exists():
    collab_df = read_data_set()
    assert collab_df is not None
