from DJSetFiller.feature_vector_maker import (
    input_feature_vector,
    feature_vectors_to_dict,
    scaler,
)

from DJSetFiller.inital_suggestions import make_recommendations_for_multiple_songs, create_model


def test_input_vector():
    songs = ["5vXlU52ohBRZb1uUw4GPqA", "5Zdmkal4CNnC5EY9qCSrMi"]
    model, model_data = create_model("data/reduced/dataset_reduced.csv")
    initial_suggestions = make_recommendations_for_multiple_songs(songs, model, model_data)
    output = input_feature_vector(initial_suggestions)

    assert output == [0.806, 0.572, 4.0, -11.081, 0.0, 0.0419, 0.00975, 0.912, 0.286, 123.01, 4.0]


def test_output_vector():
    songs = ["5vXlU52ohBRZb1uUw4GPqA", "5Zdmkal4CNnC5EY9qCSrMi"]
    model, model_data = create_model("data/reduced/dataset_reduced.csv")
    initial_suggestions = make_recommendations_for_multiple_songs(songs, model, model_data)
    output = feature_vectors_to_dict(initial_suggestions)

    assert output[4.0][00] == 0.817


def test_scaler():
    vectors = {
        0: [
            0.817,
            0.975,
            4.0,
            -6.946,
            0.0,
            0.0681,
            0.000677,
            0.806,
            0.0904,
            0.125,
            120.013,
            4.0,
        ],
        1: [
            0.729,
            0.481,
            10.0,
            -15.041,
            0.0,
            0.0699,
            0.000392,
            0.827,
            0.13,
            0.649,
            130.188,
            4.0,
        ],
    }

    output = scaler(vectors)

    assert output[0] == [
        1.0000000000000013,
        1.0,
        -1.0,
        1.0000000000000002,
        0.0,
        -1.0000000000000078,
        0.9999999999999997,
        -1.0,
        -0.9999999999999997,
        -1.0,
        -1.0,
        0.0,
    ]
