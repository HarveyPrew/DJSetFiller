def DJSetInput():
    DJSet = "2015-01-02 - Floating Points & Four Tet @ Plastic People Closing Party, London"
    return DJSet

def DJSetCollection():
    DJSetList = ["[0:00:00] Azimuth - The Tunnel", "[0:09:11] Conjunto Carcará - A Night In Tunisia", "[0:11:26] As Sublimes - Mangueira é Cancáo"]
    
    DJSetListString = ""
    for x in range(len(DJSetList)):
        DJSetListString += (f"\n{DJSetList[x]}")

    return DJSetListString

def fileReader():
    with open('DJSetInput.txt', 'w') as writer:
        writer.write(DJSetInput())
        writer.close()
    
    with open('DJSetInput.txt', 'r') as reader:
        # Read & print the entire file
        return(reader.read())



def printReccomendations():
    DJSetList = DJSetCollection()
    if fileReader() == "2015-01-02 - Floating Points & Four Tet @ Plastic People Closing Party, London":
        return DJSetList

print(printReccomendations())