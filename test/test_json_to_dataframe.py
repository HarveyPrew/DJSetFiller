from DJSetFiller.json_to_dataframe import create_df


def test_data_playlists_is_filled():
    djset = create_df()
    assert len(djset) == 3
