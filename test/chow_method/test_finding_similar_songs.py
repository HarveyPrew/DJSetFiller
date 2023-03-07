from DJSetFiller.finding_similar_songs import (
    read_data_set,
    multiple_song_input_reccomender,
    matrix_size,
    euclidean_distance,
    reduced_similar_songs,
    calculated_eds,
    input_test_songs,
    organise_missing_songs
)


def test_find_db_exists():
    collab_df = read_data_set()
    collab_df_dict = collab_df.to_dict()
    assert len(collab_df_dict) == 10


def test_size_is_found():
    matrixSize, num_songs, sparsity = matrix_size(read_data_set())

    assert matrixSize == 54
    assert num_songs == 26
    assert sparsity > 50


def test_tuple_extration():
    tuples_list = [("id_1", "score_1"), ("id_2", "score_2"), ("id_3", "score_3")]
    songs_inds = [tup[0] for tup in tuples_list]

    assert "id_1" in songs_inds
    assert "id_2" in songs_inds
    assert "score_1" not in songs_inds


def test_multiple_song_list():
    uri_list = ["5vXlU52ohBRZb1uUw4GPqA", "5Zdmkal4CNnC5EY9qCSrMi"]
    results = multiple_song_input_reccomender(uri_list, read_data_set())

    assert len(results) == 14


def test_matrix_returing():
    uri_list = ["5vXlU52ohBRZb1uUw4GPqA", "5Zdmkal4CNnC5EY9qCSrMi"]
    initial_suggestions = multiple_song_input_reccomender(uri_list, read_data_set())
    results = initial_suggestions.to_dict()
    assert results["song"][0] == "Africa"


def test_euclidean_distance():
    uri_list = ["5vXlU52ohBRZb1uUw4GPqA", "5Zdmkal4CNnC5EY9qCSrMi"]
    initial_suggestions = multiple_song_input_reccomender(uri_list, read_data_set())
    ed = euclidean_distance(initial_suggestions)
    assert ed is not None


def test_smallest_ed():
    uri_list = ["5vXlU52ohBRZb1uUw4GPqA", "5Zdmkal4CNnC5EY9qCSrMi"]
    initial_suggestions = multiple_song_input_reccomender(uri_list, read_data_set())
    best_songs = reduced_similar_songs(initial_suggestions)
    song_names = best_songs["song"].values.tolist()
    assert any("State Of Rave (Viers Remix)" in name for name in song_names)


def test_calulate_ed():
    scaled_input_vector = [
        -1.101666184549665,
        -0.6038365812770807,
        -1.386750490563073,
        -0.1786817247259729,
        -0.35355339059327373,
        -0.32126955046767547,
        -0.43658906602088027,
        -0.14817291368239394,
        1.1117217421481622,
        -0.7745848205398156,
        -0.06718260020110874,
        0.3535533905932739,
    ]
    scaled_vectors = {
        0: [
            1.1492156779411027,
            1.2189247758698838,
            -0.9707253433941511,
            0.7467728843880046,
            -0.35355339059327373,
            -0.12800746527394744,
            -0.5920076802169513,
            0.4376730176951285,
            -0.6120343294096077,
            -0.923146748121545,
            -2.103015732020797,
            0.3535533905932739,
        ],
        1: [
            0.1710546710315345,
            -2.116053410910118,
            0.6933752452815365,
            -1.8459092615810726,
            -0.35355339059327373,
            -0.09423350863815007,
            -0.5950628812823313,
            0.4961184550297029,
            -0.38072040045776867,
            1.2009037308095927,
            0.34320558544086094,
            0.3535533905932739,
        ],
    }

    ed_list = calculated_eds(scaled_vectors, scaled_input_vector)

    assert ed_list == [2.4371070571105045, 5.074792132450041]


def test_input_test():
    input = input_test_songs()

    assert input is not None


def test_missing_songs():
    missing_songs = organise_missing_songs()

    assert missing_songs is not None
