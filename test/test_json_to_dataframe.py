from DJSetFiller.json_to_dataframe import get_data_files, create_df


def test_get_data_files():
    data_files = get_data_files("data")

    assert data_files[0] == "dataset.json"


def test_data_tracks_is_filled():
    djset = create_df("data")

    assert len(djset) == 6
