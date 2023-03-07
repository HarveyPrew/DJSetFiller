import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd


def track_analysis_from_spotify(similar_songs_df):
    reccomendedSongs = similar_songs_df

    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)

    analysis = []

    for id in reccomendedSongs.index:
        analysis += sp.audio_features(reccomendedSongs["spotify_id"][id])

    song_features = pd.DataFrame.from_dict(analysis).drop(
        ["id", "analysis_url", "track_href", "uri", "type"], axis=1
    )

    features_plus_recs = pd.concat([reccomendedSongs, song_features], axis=1)
    return features_plus_recs
