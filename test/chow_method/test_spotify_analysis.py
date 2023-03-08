from DJSetFiller.spotify_analysis import (
    track_analysis_from_spotify
)
import pandas as pd


def test_track_analysis_from_spotify():

    dataset = {
        "artist": {0: "11:11"},
        "song": {0: "West Side"},
        "spotify_song_name": {0: "West Side"},
        "spotify_id": {0: "15Hy4NsbvkcSygqXC2vZdL"},
        "preview": {0: "15Hy4NsbvkcSygqXC2vZdL"},
        "songs": {0: "West Side"},
        "set_title_split": {0: "West Side"},
        "dj_id": {0: 0},
        "song_id": {0: 17},
        "size": {0: 1},
    }
    test = pd.DataFrame.from_dict(dataset)
    results = track_analysis_from_spotify(test).to_dict()

    assert results["tempo"] == {0: 178.345}


