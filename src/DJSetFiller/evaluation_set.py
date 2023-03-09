import pandas as pd


def csv_to_dict(filePath):
    input_df = pd.read_csv(filePath)
    input_dict = {}

    for index, row in input_df.iterrows():

        dj_set = row['set_name_plus_dj_id']
        spotify_id = row['spotify_id']

        if dj_set not in input_dict:
            input_dict[dj_set] = []
    
        # add the DJ ID to the list for the corresponding DJ set
        input_dict[dj_set].append(spotify_id)
    
    return input_dict


def input_test_songs():
    input_dict = csv_to_dict('data/rprecision_data/reduced/input_test_set_reduced.csv')
    return input_dict


def organise_missing_songs():
    missing_songs_dict = csv_to_dict('data/rprecision_data/reduced/missing_songs_reduced.csv')
    return missing_songs_dict
