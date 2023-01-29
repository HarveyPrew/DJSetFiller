import pandas as pd


def read_data_set():
    collab_df = pd.read_csv("data/mixesdb_df_for_recs.csv")
    return collab_df
