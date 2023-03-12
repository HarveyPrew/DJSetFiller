from DJSetFiller.DJSet import DJSet
from DJSetFiller.inital_suggestions import make_recommendations_for_dj_set, create_model
from DJSetFiller.euclidean_distance import reduced_similar_songs
from DJSetFiller.prepare_evaluation_set import make_test_data


def make_r_precision_calculations_for_evaluation_set(path):
    make_test_data(path)

    djsets = DJSet.read_songs(
        "data/rprecision_data/reduced/input_songs.csv",
        "data/rprecision_data/reduced/missing_songs.csv",
    )
    print("Number of DJ Sets - " + str(len(djsets)))
    model, model_data = create_model("data/rprecision_data/reduced/training_set.csv")

    for dj_set in djsets.values():
        initial_suggestions = make_recommendations_for_dj_set(
            dj_set, model, model_data
        )
        reduced_suggestions = reduced_similar_songs(initial_suggestions)
        dj_set.read_recommended_songs(reduced_suggestions)

        dj_set.calculate_r_precision()

    return djsets


make_r_precision_calculations_for_evaluation_set('data/rprecision_data/reduced/data_set_test_reduced.csv')
