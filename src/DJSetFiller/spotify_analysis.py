import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyAPI(object):
    def __init__(self):
        self.auth_manager = SpotifyClientCredentials()
        self.spotify_client = spotipy.Spotify(auth_manager=self.auth_manager)

    def get_spotify_features(self, similar_songs):
        recommendedSongs = similar_songs.reset_index(drop=True)
        analysis = []

        for id in recommendedSongs.index:
            analysis += self.spotify_client.audio_features(
                recommendedSongs["spotify_id"][id]
            )

        song_features = pd.DataFrame.from_dict(analysis).drop(
            ["id", "analysis_url", "track_href", "uri", "type"], axis=1
        )

        features_plus_recs = pd.concat([recommendedSongs, song_features], axis=1)
        return features_plus_recs


api_client = SpotifyAPI()
