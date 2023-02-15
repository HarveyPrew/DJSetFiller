from DJSetFiller.QuickStart import (
    quickStart
)


def test_quickstart_occurs():
    id = "5vXlU52ohBRZb1uUw4GPqA"
    quickstart = quickStart(id)
    assert quickstart is not None
