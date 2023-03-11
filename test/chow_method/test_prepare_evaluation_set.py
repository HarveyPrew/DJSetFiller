from DJSetFiller.prepare_evaluation_set import (
    import_csv, 
    find_sets_with_multiple_plays,
    select_ten_percent_of_sets,
    create_missing_songs,
    create_input_songs)


def test_dataset_is_imported():
    expected_row_amount = 33
    dataset = import_csv("data/rprecision_data/reduced/data_set_test_reduced.csv")

    assert len(dataset) == expected_row_amount


def test_filter_sets_with_multiple_plays():
    expected_row_amount = 26
    actual_row_amount = len(find_sets_with_multiple_plays("data/rprecision_data/reduced/data_set_test_reduced.csv"))

    assert actual_row_amount == expected_row_amount


def test_select_ten_percent_of_sets():
    expected_row_amount = 8
    chosen_sets, unique_set = select_ten_percent_of_sets("data/rprecision_data/reduced/data_set_test_reduced.csv")
    actual_row_amount = len(chosen_sets)
    assert actual_row_amount == expected_row_amount
    assert unique_set is not None


def test_create_missingsongs():
    expected_row_amount_missing_songs = 2
    chosen_sets, unique_set = select_ten_percent_of_sets("data/rprecision_data/reduced/data_set_test_reduced.csv")
    missing_songs = create_missing_songs(chosen_sets, unique_set)
    actual_row_amount_missing_songs = len(missing_songs)
    assert actual_row_amount_missing_songs == expected_row_amount_missing_songs


def test_create_input_songs():
    expected_row_amount_input_songs = 6
    test_sample, unique_set = select_ten_percent_of_sets("data/rprecision_data/reduced/data_set_test_reduced.csv")
    missing_songs_df = create_missing_songs(test_sample, unique_set)
    input_songs = create_input_songs(missing_songs_df, test_sample)

    actual_row_amount_input_songs = len(input_songs)
    assert actual_row_amount_input_songs == expected_row_amount_input_songs
