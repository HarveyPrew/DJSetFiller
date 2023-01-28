from DJSetFiller.validation_strategy import read_hdf_files, generate_num_tracks
import pandas as pd


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


def test_num_tracks_working():

    df_playlists_info = pd.read_hdf("df_data/df_playlists_info.hdf")
    num_tracks = generate_num_tracks(df_playlists_info)

    assert num_tracks is not None
