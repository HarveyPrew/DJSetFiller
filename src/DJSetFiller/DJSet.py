import pandas as pd


class DJSet:
    def __init__(self, dj_set_id):
        self.dj_set_id = dj_set_id
        self.missing_songs = set()
        self.input_songs = []
        self.recommended_songs = set()
        self.r_precision = None

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
        number_of_retrieved_relevant_tracks = self.number_of_relevant_recommended_songs()
        number_of_known_relevant_tracks = self.number_of_known_relevant_tracks()

        self.r_precision = number_of_retrieved_relevant_tracks / number_of_known_relevant_tracks

        return self.r_precision

    # Number of songs we withheld for this DJ set.
    def number_of_known_relevant_tracks(self):
        return len(self.missing_songs)

    def number_of_known_input_tracks(self):
        return len(self.input_songs)

    def read_songs_from_csv(dj_sets, path, songs_are_input=True): 
        raw_data = pd.read_csv(path)

        for _, row in raw_data.iterrows():

            dj_set_id = row["set_name_plus_dj_id"]
            song_id = row["spotify_id"]

            if dj_set_id not in dj_sets:
                dj_sets[dj_set_id] = DJSet(dj_set_id)

            if songs_are_input:
                dj_sets[dj_set_id].add_input_song(song_id)
            else:
                dj_sets[dj_set_id].add_missing_song(song_id)

    def read_songs(input_songs_path, witheld_songs_path):
        dj_sets = {}
        DJSet.read_songs_from_csv(dj_sets, input_songs_path, True)
        DJSet.read_songs_from_csv(dj_sets, witheld_songs_path, False)

        return dj_sets
    
    def number_of_relevant_recommended_songs(self):
        return len(self.recommended_songs & self.missing_songs)
