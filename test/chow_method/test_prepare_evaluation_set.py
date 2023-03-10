def test_dataset_is_imported():
    expected_row_amount = 20
    dataset = import_csv()

    assert len(dataset) == expected_row_amount
