from DJSetFiller.prepare_evaluation_set import import_csv, sets_with_multiple_plays


def test_dataset_is_imported():
    expected_row_amount = 33
    dataset = import_csv("data/rprecision_data/reduced/data_set_test_reduced.csv")

    assert len(dataset) == expected_row_amount


def test_filter_sets_with_multiple_plays():
    expected_row_amount = 26
    actual_row_amount = len(sets_with_multiple_plays("data/rprecision_data/reduced/data_set_test_reduced.csv"))

    assert actual_row_amount == expected_row_amount

