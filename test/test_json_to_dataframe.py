from DJSetFiller.json_to_dataframe import create_df


def test_data_tracks_is_filled():
    djset = create_df("data/dataset.json")

    assert len(djset) == 6
