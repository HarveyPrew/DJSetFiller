class DJSet:
    def __init__(self, path):
        fileContents = ""
        with open(path) as reader:
            fileContents = reader.read()

        if len(fileContents) == 0:
            return

        self.id = fileContents

        self.recomendations = [
            "[0:00:00] Azimuth - The Tunnel",
            "[0:09:11] Conjunto Carcará - A Night In Tunisia",
            "[0:11:26] As Sublimes - Mangueira é Cancáo",
        ]
