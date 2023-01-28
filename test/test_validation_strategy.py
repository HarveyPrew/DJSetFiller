from DJSetFiller.validation_strategy import read_hdf_files


def test_hdf_files_are_read():
    (
        df_tracks,
        df_playlists,
        df_playlists_info,
        df_playlists_test,
        df_playlists_test_info,
    ) = read_hdf_files()

    assert df_tracks is not None
    assert df_playlists is not None
    assert df_playlists_info is not None
    assert df_playlists_test is not None
    assert df_playlists_test_info is not None
