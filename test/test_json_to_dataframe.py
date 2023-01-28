from DJSetFiller.json_to_dataframe import (
    transform_data_to_collections,
    create_playlist_info,
    create_tracks_info,
    create_playlists_df,
    playlist_col,
    playlist_test_col,
)


def test_data_tracks_is_filled():
    (
        data_playlists,
        data_tracks,
        playlists,
        tracks,
        data_playlists_test,
        playlists_test,
    ) = transform_data_to_collections("data/dataset.json")

    assert len(data_playlists) == 3
    assert len(data_tracks) == 6

    assert len(tracks) == 6
    assert "spotify:track:1I7JNe8BDXTzT9Cld4Hzkl" in tracks

    assert len(data_playlists_test) == 1
    assert len(playlists_test) == 2

    assert len(playlists) == 8
    assert playlists[0][0] == 0
    assert playlists[0][1] == "spotify:track:6vXcHqE3bYPirOgKlDbN5s"
    assert playlists[0][2] == 0

    assert playlists[4][0] == 1
    assert playlists[4][1] == "spotify:track:59J7HbzNJbKMYhGe7rywGa"
    assert playlists[4][2] == 0


def test_create_playlist_info():
    (
        data_playlists,
        data_tracks,
        playlists,
        tracks,
        data_playlists_test,
        playlists_test,
    ) = transform_data_to_collections("data/dataset.json")

    playlist_info = create_playlist_info(data_playlists, playlist_col())

    assert playlist_info is not None


def test_create_tracks_is_made():
    (
        data_playlists,
        data_tracks,
        playlists,
        tracks,
        data_playlists_test,
        playlists_test,
    ) = transform_data_to_collections("data/dataset.json")

    playlist_info = create_tracks_info(data_tracks)

    assert playlist_info is not None


def test_create_playlists_is_made():
    (
        data_playlists,
        data_tracks,
        playlists,
        tracks,
        data_playlists_test,
        playlists_test,
    ) = transform_data_to_collections("data/dataset.json")

    df_tracks = create_tracks_info(data_tracks)

    track_uri2tid = df_tracks.set_index("track_uri").tid

    df_playlists = create_playlists_df(playlists, track_uri2tid)

    assert df_playlists is not None


def test_create_playlist_info_test():
    (
        data_playlists,
        data_tracks,
        playlists,
        tracks,
        data_playlists_test,
        playlists_test,
    ) = transform_data_to_collections("data/dataset.json")

    playlist_info_test = create_playlist_info(data_playlists_test, playlist_test_col())

    assert playlist_info_test is not None


def test_create_playlists_test_is_made():
    (
        data_playlists,
        data_tracks,
        playlists,
        tracks,
        data_playlists_test,
        playlists_test,
    ) = transform_data_to_collections("data/dataset.json")

    df_tracks = create_tracks_info(data_tracks)

    track_uri2tid = df_tracks.set_index("track_uri").tid

    df_playlists_test = create_playlists_df(playlists_test, track_uri2tid)

    assert df_playlists_test is not None
