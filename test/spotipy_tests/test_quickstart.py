from DJSetFiller.QuickStart import (
    quickStart
)


def test_quickstart_occurs():
    quickstart = quickStart()
    assert quickstart is not None
