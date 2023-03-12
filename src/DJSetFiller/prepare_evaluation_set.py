import pandas as pd


def make_test_data(dataset_path):
    dataset_df = import_csv(dataset_path)
    test_sample, unique_dj_sets = select_ten_percent_of_sets(dataset_df)
    missing_songs_df = create_missing_songs(test_sample, unique_dj_sets)
    create_input_songs(missing_songs_df, test_sample)
    create_training_set(test_sample, dataset_df)
    return 0


def create_training_set(test_sample, dataset):
    training_set_df = remove_rows_in_x_from_y(test_sample, dataset)
    training_set_df.to_csv('data/rprecision_data/reduced/training_set.csv', index=False)
    return training_set_df


def create_input_songs(missing_songs_df, test_sample):
    input_songs_df = remove_rows_in_x_from_y(missing_songs_df, test_sample)
    input_songs_df.to_csv('data/rprecision_data/reduced/input_songs.csv', index=False)
    return input_songs_df


def remove_rows_in_x_from_y(x, y):
    small_df_keys = list(x.columns.values)
    big_df_index = y.set_index(small_df_keys).index
    small_df_index = x.set_index(small_df_keys).index

    # Removing rows from x that are also in y
    reduced_df = y[~big_df_index.isin(small_df_index)].copy()
    return reduced_df


def create_missing_songs(test_sample, unique_dj_sets):
    missing_songs = []
    for dj_set in unique_dj_sets:
        test_sample_dj_set = test_sample.query('set_name_plus_dj_id == @dj_set')
        missing_songs_for_dj_set = test_sample_dj_set.sample(frac=0.2, replace=True, random_state=1)
        missing_songs_for_dj_set.reset_index()
        missing_songs.append(missing_songs_for_dj_set)

    missing_songs_df = pd.concat(missing_songs)
    missing_songs_df.to_csv('data/rprecision_data/reduced/missing_songs.csv', index=False)

    return missing_songs_df


def select_ten_percent_of_sets(dataset_df):
    sets_with_multiple_plays = find_sets_with_multiple_plays(dataset_df)
    unique_dj_sets = sets_with_multiple_plays.drop_duplicates(subset='set_name_plus_dj_id').copy()
    percentage_of_sets = unique_dj_sets.sample(frac=0.333, replace=True, random_state=1)
    unique_dj_sets = percentage_of_sets['set_name_plus_dj_id'].tolist()

    test_sample = sets_with_multiple_plays[sets_with_multiple_plays['set_name_plus_dj_id'].isin(unique_dj_sets)].copy()

    return test_sample, unique_dj_sets


def find_sets_with_multiple_plays(dataset_df):

    sets_with_multiple_plays = dataset_df.query('total_play_count > 2')
    grouped = sets_with_multiple_plays.groupby('set_name_plus_dj_id').size()
    result = grouped[grouped > 3]
    result_df = sets_with_multiple_plays[sets_with_multiple_plays['set_name_plus_dj_id'].isin(result.index)]
    return result_df


def import_csv(path):
    dataset_df = pd.read_csv(path)
    return dataset_df
