import pandas as pd


def import_csv(path):
    dataset = pd.read_csv(path)
    return dataset


def sets_with_multiple_plays(path):
    dataset = pd.read_csv(path)
    sets_with_multiple_plays = dataset.query('total_play_count > 1')
    return sets_with_multiple_plays
