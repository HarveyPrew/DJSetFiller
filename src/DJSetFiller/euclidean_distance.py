import numpy as np
from DJSetFiller.feature_vector_maker import feature_vectors_to_dict, scaler


def reduced_similar_songs(initial_suggestions):
    ed = euclidean_distance(initial_suggestions)
    best_song_ids = sorted(ed, key=ed.get)[:100]
    initial_df = initial_suggestions
    final_df = initial_df.loc[initial_df["song_id"].isin(best_song_ids)]
    return final_df


def euclidean_distance(initial_suggestions):
    all_vectors_dict = feature_vectors_to_dict(initial_suggestions)
    scaled_vectors = scaler(all_vectors_dict)
    scaled_input_vector = np.array(scaled_vectors.pop(-1))

    ed_list = calculated_eds(scaled_vectors, scaled_input_vector)

    ed_dict = {key: value for key, value in all_vectors_dict.items() if key != "input"}
    ed_dict.update(zip(ed_dict.keys(), ed_list))

    return ed_dict


def calculated_eds(scaled_vectors, scaled_input_vector):
    ed_list = []

    for point in scaled_vectors:
        ed_list.append(np.linalg.norm(scaled_input_vector - np.array(point)))

    return ed_list
