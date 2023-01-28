from DJSetFiller.json_to_dataframe import create_df


def test_data_tracks_is_filled():
    (
        data_playlists,
        data_tracks,
        playlists,
        tracks,
        data_playlists_test,
        playlists_test,
    ) = create_df("data/dataset.json")

    assert len(data_playlists) == 3
    assert len(data_tracks) == 6
    assert len(playlists) == 8
    assert len(tracks) == 6
    assert len(data_playlists_test) == 1
    assert len(playlists_test) == 2

