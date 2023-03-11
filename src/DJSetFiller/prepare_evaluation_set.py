import pandas as pd


def create_missing_songs(test_sample, unique_dj_sets):
    missing_songs = []
    for dj_set in unique_dj_sets:
        test_sample_dj_set = test_sample.query('set_name_plus_dj_id == @dj_set')
        missing_songs_for_dj_set = test_sample_dj_set.sample(frac=0.2, replace=True, random_state=1)
        missing_songs_for_dj_set.reset_index()
        missing_songs.append(missing_songs_for_dj_set)

    missing_songs_df = pd.concat(missing_songs)
    missing_songs_keys = list(missing_songs_df.columns.values)
    test_sample_index = test_sample.set_index(missing_songs_keys).index
    missing_songs_index = missing_songs_df.set_index(missing_songs_keys).index

    # Removing rows from test sample that are also in missing songs
    input_songs_df = test_sample[~test_sample_index.isin(missing_songs_index)].copy()

    return missing_songs_df, input_songs_df


def select_ten_percent_of_sets(path):
    sets_with_multiple_plays = find_sets_with_multiple_plays(path)
    unique_dj_sets = sets_with_multiple_plays.drop_duplicates(subset='set_name_plus_dj_id').copy()
    percentage_of_sets = unique_dj_sets.sample(frac=0.333, replace=True, random_state=1)
    unique_dj_sets = percentage_of_sets['set_name_plus_dj_id'].tolist()

    test_sample = sets_with_multiple_plays[sets_with_multiple_plays['set_name_plus_dj_id'].isin(unique_dj_sets)].copy()
    return test_sample, unique_dj_sets


def find_sets_with_multiple_plays(path):
    dataset = pd.read_csv(path)
    sets_with_multiple_plays = dataset.query('total_play_count > 1')
    return sets_with_multiple_plays


def import_csv(path):
    dataset = pd.read_csv(path)
    return dataset



