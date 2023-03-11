from DJSetFiller.prepare_evaluation_set import (
    import_csv, 
    find_sets_with_multiple_plays, 
    select_ten_percent_of_sets,
    create_missing_songs)


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
    actual_row_amount = len(select_ten_percent_of_sets("data/rprecision_data/reduced/data_set_test_reduced.csv"))
    assert actual_row_amount == expected_row_amount


def test_create_missing_songs():
    expected_row_amount = 4
    chosen_sets = select_ten_percent_of_sets("data/rprecision_data/reduced/data_set_test_reduced.csv")
    actual_row_amount = len(create_missing_songs(chosen_sets))
    assert actual_row_amount == expected_row_amount
