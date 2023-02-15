import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def quickStart(id):
    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)

    analysis = sp.audio_features(id)
    return analysis
