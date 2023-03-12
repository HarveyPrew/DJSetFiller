from DJSetFiller.DJSet import DJSet
from DJSetFiller.inital_suggestions import make_recommendations_for_dj_set, create_model
from DJSetFiller.euclidean_distance import reduced_similar_songs
from DJSetFiller.prepare_evaluation_set import make_test_data
import pandas as pd


def make_r_precision_calculations_for_evaluation_set(path):
    make_test_data(path)

    djsets = DJSet.read_songs(
        "data/rprecision_data/reduced/input_songs.csv",
        "data/rprecision_data/reduced/missing_songs.csv",
    )
    print("Number of DJ Sets - " + str(len(djsets)), "\n")
    model, model_data = create_model("data/rprecision_data/reduced/training_set.csv")

    counter = 1
    r_precision_list = []

    for dj_set in djsets.values():

        initial_suggestions = make_recommendations_for_dj_set(
            dj_set, model, model_data
        )
        reduced_suggestions = reduced_similar_songs(initial_suggestions)
        dj_set.read_recommended_songs(reduced_suggestions)

        dj_set.calculate_r_precision()
        print(str(counter), " out of ", str(len(djsets)) + " calculated\n")
        print("Set name - ", dj_set.dj_set_id,
              " Number of Input songs - ", str(len(dj_set.input_songs)),
              " Number of Missing songs - ", str(len(dj_set.missing_songs)),
              " R-precision - ", dj_set.r_precision)
        
        r_precision_list.append([dj_set.dj_set_id, len(dj_set.input_songs), len(dj_set.missing_songs), dj_set.r_precision])
        counter += 1

    r_precision_df = pd.DataFrame(r_precision_list, columns=['set_name', 'input_song_count', "missing_song_cout", "r_value"])
    r_precision_df.to_csv('data/r_precision_values.csv', index=False)
    return r_precision_df


make_r_precision_calculations_for_evaluation_set('data/rprecision_data/reduced/semi_reduced_dataset.csv')
