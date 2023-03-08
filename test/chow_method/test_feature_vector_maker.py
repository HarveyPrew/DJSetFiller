from DJSetFiller.feature_vector_maker import (
    input_feature_vector,
    feature_vectors_to_dict,
    scaler,
)

from DJSetFiller.inital_suggestions import make_recommendations_for_multiple_songs


def test_input_vector():
    songs = ["5vXlU52ohBRZb1uUw4GPqA", "5Zdmkal4CNnC5EY9qCSrMi"]
    initial_suggestions = make_recommendations_for_multiple_songs(songs, "data/reduced/dataset_reduced.csv")
    output = input_feature_vector(initial_suggestions)

    assert output == [
        0.6145,
        0.705,
        2.5,
        -9.8355,
        0.0,
        0.057800000000000004,
        0.015175000000000001,
        0.5955,
        0.3855,
        0.16165,
        128.481,
        4.0,
    ]


def test_output_vector():
    songs = ["5vXlU52ohBRZb1uUw4GPqA", "5Zdmkal4CNnC5EY9qCSrMi"]
    initial_suggestions = make_recommendations_for_multiple_songs(songs, "data/reduced/dataset_reduced.csv")
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
