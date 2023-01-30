from DJSetFiller.finding_similar_songs import read_data_set, collab_filter, run_function


def test_find_db_exists():
    collab_df = read_data_set()
    assert collab_df is not None



def test_programme_not_working():
    function = run_function("3gCiJLZj4PJfhWXzwnV7FR", read_data_set())
    assert function == "Programme not working"
