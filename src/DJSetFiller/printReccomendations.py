from DJSetFiller.DJSet import DJSet


def printReccomendations(path):
    djset = DJSet(path)
    for r in djset.recomendations:
        print(r)


printReccomendations("DJSetInput.txt")
