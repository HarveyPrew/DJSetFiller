import numpy as np
import pandas as pd

np.random.seed(0)


def generate_num_tracks(df_playlists_info):
    num_tracks = df_playlists_info.groupby("num_tracks").pid.apply(np.array)
    return num_tracks


def generate_val_playlist(df_playlists_test_info, num_tracks):
    validation_playlists = {}
    condition = df_playlists_test_info.num_tracks.value_counts().reset_index().values
    for i, j in condition:
        rc = np.random.choice(
            num_tracks.loc[i], 2 * j, replace=False
        )
        validation_playlists[i] = rc
    
    return validation_playlists


def read_hdf_files():
    df_tracks = pd.read_hdf("df_data/df_tracks.hdf")
    df_playlists = pd.read_hdf("df_data/df_playlists.hdf")
    df_playlists_info = pd.read_hdf("df_data/df_playlists_info.hdf")
    df_playlists_test = pd.read_hdf("df_data/df_playlists_test.hdf")
    df_playlists_test_info = pd.read_hdf("df_data/df_playlists_test_info.hdf")

    generate_num_tracks(df_playlists_info)

    return (
        df_tracks,
        df_playlists,
        df_playlists_info,
        df_playlists_test,
        df_playlists_test_info,
    )