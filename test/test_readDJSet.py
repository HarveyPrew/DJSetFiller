from DJSetFiller.DJSet import DJSet


def test_read_DJ_set_id():
    djset = DJSet("DJSetInput.txt")
    assert (
        djset.id
        == "2015-01-02 - Floating Points & Four Tet @ Plastic People Closing Party, London"
    )


def test_DJ_set_reccomendation_contains_songs():
    djset = DJSet("DJSetInput.txt")
    assert len(djset.recomendations) > 0

