import pandas as pd


class DJSet:
    def __init__(self, dj_set_id):
        self.dj_set_id = dj_set_id
        self.missing_songs = set()
        self.input_songs = []
        self.recommended_songs = set()

    def add_missing_song(self, song_id):
        self.missing_songs.add(song_id)

    def add_input_song(self, song_id):
        self.input_songs.append(song_id)
    
    def read_recommended_songs(self, recommended_songs):
        recommended_songs.filter(items=['output'])
        for value in recommended_songs.index:
            self.recommended_songs.add(recommended_songs['spotify_id'][value])

    # R-precision is the number of retrieved relevant tracks divided by
    # the number of known relevant tracks (i.e., the number of withheld tracks)
    def calculate_r_precision(self):
        return 0.5

    # Number of songs we withheld for this DJ set.
    def number_of_known_relevant_tracks(self):
        return len(self.missing_songs)

    def number_of_known_input_tracks(self):
        return len(self.input_songs)

    def read_songs_from_csv(path, input_songs=True):
        dj_sets = {}

        raw_data = pd.read_csv(path)

        for _, row in raw_data.iterrows():

            dj_set_id = row["title + dj"]
            song_id = row["spotify_id"]

            if dj_set_id not in dj_sets:
                dj_sets[dj_set_id] = DJSet(dj_set_id)

            if input_songs:
                dj_sets[dj_set_id].add_input_song(song_id)
            else:
                dj_sets[dj_set_id].add_missing_song(song_id)

        return dj_sets

    def read_withheld_songs(path):
        return DJSet.read_songs_from_csv(path, False)

    def read_input_songs(path):
        return DJSet.read_songs_from_csv(path, True)
