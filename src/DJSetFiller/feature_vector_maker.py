from sklearn.preprocessing import StandardScaler


def input_feature_vector(inital_suggestions):
    new_df = vector_attributes(inital_suggestions, "input")
    column_averages = new_df.drop("song_id", axis=1).mean()
    averages_list = column_averages.tolist()
    return averages_list


def feature_vectors_to_dict(inital_suggestions):
    new_df = vector_attributes(inital_suggestions, "output")
    vector_dict = {
        row["song_id"]: row.drop("song_id").tolist() for _, row in new_df.iterrows()
    }

    input_vector = input_feature_vector(inital_suggestions)
    vector_dict["input"] = input_vector
    return vector_dict


def vector_attributes(inital_suggestions, io):
    df = inital_suggestions.filter(
        items=[
            "song_id",
            "Type",
            "danceability",
            "energy",
            "key",
            "loudness",
            "mode",
            "speechiness",
            "acousticness",
            "instrumentalness",
            "valence",
            "tempo",
            "time_signature",
        ]
    )
    new_df = df[df["Type"] == io].drop(columns=["Type"])
    return new_df


def scaler(all_vectors_dict):
    vectors_list = []

    for i in all_vectors_dict:
        vectors_list.append(list(all_vectors_dict[i]))

    scaler = StandardScaler().fit(vectors_list)
    X_scaled = scaler.transform(vectors_list).tolist()

    return X_scaled
