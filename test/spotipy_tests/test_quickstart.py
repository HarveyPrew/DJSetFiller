from DJSetFiller.QuickStart import quick_start


def test_quickstart_occurs():
    id = "5vXlU52ohBRZb1uUw4GPqA"
    quickstart = quick_start(id)
    assert quickstart is not None
