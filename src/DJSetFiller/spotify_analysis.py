import pandas as pd


def track_analysis_from_spotify(sp, similar_songs_df):
    recommendedSongs = similar_songs_df.reset_index(drop=True)

    analysis = []

    for id in recommendedSongs.index:
        analysis += sp.audio_features(recommendedSongs["spotify_id"][id])

    song_features = pd.DataFrame.from_dict(analysis).drop(
        ["id", "analysis_url", "track_href", "uri", "type"], axis=1
    )

    features_plus_recs = pd.concat([recommendedSongs, song_features], axis=1)
    return features_plus_recs
