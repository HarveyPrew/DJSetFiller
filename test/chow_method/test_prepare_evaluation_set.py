from DJSetFiller.prepare_evaluation_set import (
    import_csv,
    find_sets_with_multiple_plays,
    select_ten_percent_of_sets,
    create_missing_songs,
    create_input_songs,
    create_training_set,
    make_test_data,
)


def small_dataset_is_imported():
    expected_row_amount = 32
    dataset = import_csv("data/rprecision_data/reduced/data_set_test_reduced.csv")

    assert len(dataset) == expected_row_amount


def filter_sets_with_multiple_plays():
    expected_row_amount = 13
    dataset_df = import_csv("data/rprecision_data/reduced/data_set_test_reduced.csv")
    actual_row_amount = len(find_sets_with_multiple_plays(dataset_df))

    assert actual_row_amount == expected_row_amount


def select_ten_percent_of_sets():
    expected_row_amount = 4
    dataset_df = import_csv("data/rprecision_data/reduced/data_set_test_reduced.csv")
    chosen_sets, unique_set = select_ten_percent_of_sets(dataset_df)
    actual_row_amount = len(chosen_sets)
    assert actual_row_amount == expected_row_amount
    assert unique_set is not None


def create_missing_songs():
    expected_row_amount_missing_songs = 1
    dataset_df = import_csv("data/rprecision_data/reduced/data_set_test_reduced.csv")
    chosen_sets, unique_set = select_ten_percent_of_sets(dataset_df)
    missing_songs_df = create_missing_songs(chosen_sets, unique_set)
    actual_row_amount_missing_songs = len(missing_songs_df)
    assert actual_row_amount_missing_songs == expected_row_amount_missing_songs


def create_input_songs():
    expected_row_amount_input_songs = 3
    dataset_df = import_csv("data/rprecision_data/reduced/data_set_test_reduced.csv")
    test_sample, unique_set = select_ten_percent_of_sets(dataset_df)
    missing_songs_df = create_missing_songs(test_sample, unique_set)
    input_songs_df = create_input_songs(missing_songs_df, test_sample)

    actual_row_amount_input_songs = len(input_songs_df)
    assert actual_row_amount_input_songs == expected_row_amount_input_songs


def create_training_set():
    expected_row_amount_training_set = 28

    dataset_df = import_csv("data/rprecision_data/reduced/semi_reduced_dataset.csv")
    test_sample, unique_set = select_ten_percent_of_sets(dataset_df)
    training_set_df = create_training_set(test_sample, dataset_df)
    actual_row_amount_training_set = len(training_set_df)

    assert actual_row_amount_training_set == expected_row_amount_training_set
