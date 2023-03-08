import os
import pandas as pd


def dog_speakers():
    miles = Dog("Miles", 4)
    description = miles.description()
    
    return description


def description_text(self):
    return f"{self.name} is {self.age} years old"


class Dog:
    species = "Canis familiaris"

    def __init__(self, name, age):
        self.name = name
        self.age = age

    # Instance method
    def description(self):
        return description_text(self)

    # Another instance method
    def speak(self, sound):
        return f"{self.name} says {sound}"


class InitalSuggestionMethods:
    def __init__(self, path):
        self.path = path

    def data_set(self):
        return read_data_set(self.path)


def read_data_set(path):
    dataset_df = pd.read_csv(path)

    os.environ["MKL_NUM_THREADS"] = "1"
    return dataset_df