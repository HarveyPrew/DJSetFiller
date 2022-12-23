def fileReader():
    with open('dog_breeds.txt', 'r') as reader:
        # Read & print the entire file
        return(reader.read())


print(fileReader())