from DJSetFiller.DJSet import DJSet


def test_r_precision():
    expected_r_precision = 0.5
    djset = DJSet()
    actual_r_precision = djset.calculate_r_precision()

    assert actual_r_precision == expected_r_precision
