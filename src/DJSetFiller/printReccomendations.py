from DJSetFiller.DJSet import DJSet


def print_reccomendations(path):
    djset = DJSet(path)
    for r in djset.recomendations:
        print(r)


print_reccomendations("DJSetInput.txt")
