from DJSetFiller.DJSet import DJSet


def test_r_precision():
    expected_r_precision = 0.5
    djset = DJSet("a")
    actual_r_precision = djset.calculate_r_precision()

    assert actual_r_precision == expected_r_precision


def test_number_of_known_relevant_tracks():
    expected_number_of_known_relevant_tracks = 1
    djset = DJSet("a")

    djset.add_missing_song(1)
    actual_number_of_known_relevant_tracks = djset.number_of_known_relevant_tracks()

    assert (
        expected_number_of_known_relevant_tracks
        == actual_number_of_known_relevant_tracks
    )


def test_read_withheld_songs():
    expected_number_of_known_relevant_tracks = 3
    dj_set_id = ' - ≈Åukasz Tomaszewski, ¬°MASH-UP!, Siriusmo, Lionza, Michael Mayer - COSMO Selektor 1692'
    djsets = DJSet.read_withheld_songs("data/rprecision_data/reduced/missing_songs_reduced.csv")
    test_dj_set = djsets[dj_set_id]

    actual_number_of_known_relevant_tracks = test_dj_set.number_of_known_relevant_tracks()

    assert (
        expected_number_of_known_relevant_tracks
        == actual_number_of_known_relevant_tracks
    )

 