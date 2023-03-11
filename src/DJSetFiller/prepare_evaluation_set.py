import pandas as pd


def create_missing_songs(chosen_sets, unique_sets_list):
    missing_songs = []
    for set in unique_sets_list:
        set_df = chosen_sets.query('set_name_plus_dj_id == @set')
        missing_songs_for_set = set_df.sample(frac=0.2, replace=True, random_state=1)
        missing_songs_for_set.reset_index()
        missing_songs.append(missing_songs_for_set)
    
    missing_songs_df = pd.concat(missing_songs)

    return missing_songs_df


def select_ten_percent_of_sets(path):
    sets_with_multiple_plays = find_sets_with_multiple_plays(path)
    unique_sets = sets_with_multiple_plays.drop_duplicates(subset='set_name_plus_dj_id').copy()
    percentage_of_sets = unique_sets.sample(frac=0.333, replace=True, random_state=1)
    unique_sets_list = percentage_of_sets['set_name_plus_dj_id'].tolist()

    chosen_sets = sets_with_multiple_plays[sets_with_multiple_plays['set_name_plus_dj_id'].isin(unique_sets_list)].copy()
    return chosen_sets, unique_sets_list


def find_sets_with_multiple_plays(path):
    dataset = pd.read_csv(path)
    sets_with_multiple_plays = dataset.query('total_play_count > 1')
    return sets_with_multiple_plays


def import_csv(path):
    dataset = pd.read_csv(path)
    return dataset



