import os
import json
import pandas as pd


def finding_json_files(path):
    f = open(path)
    js = f.read()
    f.close()
    mpd_slice = json.loads(js)
    return mpd_slice


def json__data_to_list(
    playlist_col, tracks_col, data_playlists, data_tracks, playlists, tracks, mpd_slice
):
    for playlist in mpd_slice["playlists"]:
        json_entry_to_list(data_playlists, playlist_col, playlist)
        for track in playlist["tracks"]:
            playlists.append([playlist["pid"], track["track_uri"], track["pos"]])
            if track["track_uri"] not in tracks:
                json_entry_to_list(data_tracks, tracks_col, track)
                tracks.add(track["track_uri"])

    return data_playlists, data_tracks, playlists, track


def json_entry_to_list(empty_list, collection, entry_in_json):
    empty_list.append([entry_in_json[col] for col in collection])


def playlist_col():
    return [
        "collaborative",
        "duration_ms",
        "modified_at",
        "name",
        "num_albums",
        "num_artists",
        "num_edits",
        "num_followers",
        "num_tracks",
        "pid",
    ]


def tracks_col():
    return [
        "album_name",
        "album_uri",
        "artist_name",
        "artist_uri",
        "duration_ms",
        "track_name",
        "track_uri",
    ]


def playlist_test_col():
    return ["name", "num_holdouts", "num_samples", "num_tracks", "pid"]


def transform_data_to_collections(path):
    data_playlists = []
    data_tracks = []
    playlists = []

    tracks = set()

    mpd_slice = finding_json_files(path)

    json__data_to_list(
        playlist_col(),
        tracks_col(),
        data_playlists,
        data_tracks,
        playlists,
        tracks,
        mpd_slice,
    )

    mpd_slice = finding_json_files("input.json")

    data_playlists_test = []
    playlists_test = []

    json__data_to_list(
        playlist_test_col(),
        tracks_col(),
        data_playlists_test,
        data_tracks,
        playlists_test,
        tracks,
        mpd_slice,
    )

    return (
        data_playlists,
        data_tracks,
        playlists,
        tracks,
        data_playlists_test,
        playlists_test,
    )


def set_collab_as_bool(df_playlists_info):
    df_playlists_info["collaborative"] = df_playlists_info["collaborative"].map(
        {"false": False, "true": True}
    )
    return df_playlists_info


def create_playlist_info(data_playlists, playlist_col):
    df_playlists_info = pd.DataFrame(data_playlists, columns=playlist_col)

    return df_playlists_info


def create_tracks_info(data_tracks):
    df_tracks = pd.DataFrame(data_tracks, columns=tracks_col())
    df_tracks["tid"] = df_tracks.index
    return df_tracks


def create_playlists_df(playlists, track_uri2tid):
    df_playlists = pd.DataFrame(playlists, columns=["pid", "tid", "pos"])
    df_playlists.tid = df_playlists.tid.map(track_uri2tid)
    return df_playlists


def transform_data_to_hdf(path):
    (
        data_playlists,
        data_tracks,
        playlists,
        tracks,
        data_playlists_test,
        playlists_test,
    ) = transform_data_to_collections("data/dataset.json")

    df_playlists_info = create_playlist_info(data_playlists, playlist_col())
    df_playlists_info = set_collab_as_bool(df_playlists_info)

    df_tracks = create_tracks_info(data_tracks)

    track_uri2tid = df_tracks.set_index("track_uri").tid

    df_playlists = create_playlists_df(playlists, track_uri2tid)

    df_playlists_test_info = create_playlist_info(
        data_playlists_test, playlist_test_col()
    )

    df_playlists_test = create_playlists_df(playlists_test, track_uri2tid)

    df_tracks.to_hdf("df_data/df_tracks.hdf", key="abc")
    df_playlists.to_hdf("df_data/df_playlists.hdf", key="abc")
    df_playlists_info.to_hdf("df_data/df_playlists_info.hdf", key="abc")
    df_playlists_test.to_hdf("df_data/df_playlists_test.hdf", key="abc")
    df_playlists_test_info.to_hdf("df_data/df_playlists_test_info.hdf", key="abc")

    return df_playlists_info, df_tracks, df_playlists, df_playlists_test_info, df_playlists_test


