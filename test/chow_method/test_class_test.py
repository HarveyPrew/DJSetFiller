from DJSetFiller.class_test import dog_speakers


def test_dog_speakers():
    dogs = dog_speakers()
    assert dogs is not None
