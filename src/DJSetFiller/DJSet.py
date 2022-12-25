class DJSet:
    def __init__(self, path):
        fileContents = ""
        with open("DJSetInput.txt", "r") as reader:
            # Read & print the entire file
            fileContents = reader.read()

        if len(fileContents) > 0:
            self.id = fileContents
