from DJSetFiller.json_to_dataframe import create_df


def test_read_DJ_set_id():
    djset = create_df()
    assert djset == ["dataset.json"]


def test_doesnt_read_DJ_set_id():
    djset = create_df()
    assert djset != ["datasetz.json"]
