from DJSetFiller.euclidean_distance import (
    reduced_similar_songs,
    euclidean_distance,
    calculated_eds,
)

from DJSetFiller.inital_suggestions import make_recommendations_for_multiple_songs, create_model


def test_euclidean_distance():
    songs = ["4qmAfMPFE32ZEeLbcx37Bn", "4Xt52noZPI7uBOD9EINnuz", '6jSov5Qazh1WqLqgEw6Q29']
    model, model_data = create_model("data/new_dataset2.csv")
    initial_suggestions = make_recommendations_for_multiple_songs(songs, model, model_data) 
    ed = euclidean_distance(initial_suggestions)
    assert ed is not None


def test_smallest_ed():
    songs = ["0BqSNW0NRmChEjYC95n3E0", "0NHhIQGGHzW3YVDsBNEc4k", '3okR4Eq2CKrUZ50cXI9ejl',
             '5bc5av8GW7hNcVAxTYmPkV', '5n3MM3iuVnGmF3ouFfLlAp', '6O8zWACivE5KC6do6v5kMz',
             '6ZWp11U7wnnoT2vmPOY9SG', '1cc97OaF9JfIB8m5ozj6yU']
    model, model_data = create_model("data/new_dataset2.csv")
    initial_suggestions = make_recommendations_for_multiple_songs(songs, model, model_data)
    best_songs = reduced_similar_songs(initial_suggestions)
    song_names = best_songs["song"].values.tolist()
    assert song_names is not None


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
