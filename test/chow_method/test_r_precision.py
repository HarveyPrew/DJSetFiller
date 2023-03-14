from DJSetFiller.DJSet import DJSet
from DJSetFiller.inital_suggestions import make_recommendations_for_dj_set, create_model
from DJSetFiller.euclidean_distance import reduced_similar_songs
from DJSetFiller.r_precision import make_r_precision_calculations_for_evaluation_set


def r_precision():
    djsets = make_r_precision_calculations_for_evaluation_set('data/rprecision_data/reduced/semi_reduced_dataset.csv')

    assert djsets is not None


def test_number_of_known_relevant_tracks():
    expected_number_of_known_relevant_tracks = 1
    djset = DJSet("a")

    djset.add_missing_song(1)
    actual_number_of_known_relevant_tracks = djset.number_of_known_relevant_tracks()

    assert (
        expected_number_of_known_relevant_tracks
        == actual_number_of_known_relevant_tracks
    )


def test_read_songs():

    dj_set_id = " - 747 - Slam Radio 310 - 1"
    djsets = DJSet.read_songs(
        "data/rprecision_data/reduced/input_test_set_reduced.csv",
        "data/rprecision_data/reduced/missing_songs_reduced.csv",
    )
    test_dj_set = djsets[dj_set_id]

    expected_number_of_known_relevant_tracks = 2
    actual_number_of_known_relevant_tracks = (
        test_dj_set.number_of_known_relevant_tracks()
    )

    assert (
        expected_number_of_known_relevant_tracks
        == actual_number_of_known_relevant_tracks
    )

    expected_number_of_known_input_tracks = 3
    actual_number_of_known_input_tracks = test_dj_set.number_of_known_input_tracks()
    assert expected_number_of_known_input_tracks == actual_number_of_known_input_tracks


def test_generate_recommendations():
    dj_set_id = (
        " - 747 - Slam Radio 310 - 1"
    )
    djsets = DJSet.read_songs(
        "data/rprecision_data/reduced/input_test_set_reduced.csv",
        "data/rprecision_data/reduced/missing_songs_reduced.csv",
    )
    dj_set = djsets[dj_set_id]
    model, model_data = create_model("data/rprecision_data/reduced/training_set_test_reduced.csv")

    initial_suggestions = make_recommendations_for_dj_set(
        dj_set, model, model_data
    )
    reduced_suggestions = reduced_similar_songs(initial_suggestions)
    dj_set.read_recommended_songs(reduced_suggestions)

    assert len(dj_set.recommended_songs) == 5


def number_of_relevant_recommended_songs():
    dj_set_id = " - 747 - Slam Radio 310 - 1"
    djsets = DJSet.read_songs(
        "data/rprecision_data/reduced/input_test_set_reduced.csv",
        "data/rprecision_data/reduced/missing_songs_reduced.csv",
    )
    dj_set = djsets[dj_set_id]
    model, model_data = create_model("data/rprecision_data/reduced/semi_reduced_dataset.csv")

    initial_suggestions = make_recommendations_for_dj_set(
        dj_set, model, model_data
    )
    reduced_suggestions = reduced_similar_songs(initial_suggestions)
    dj_set.read_recommended_songs(reduced_suggestions)

    known_relevant_songs = dj_set.number_of_relevant_recommended_songs()
    assert known_relevant_songs > 0
