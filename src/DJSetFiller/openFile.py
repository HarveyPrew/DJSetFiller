def DJSetInput():
    DJSet = "2015-01-02 - Floating Points & Four Tet @ Plastic People Closing Party, London"
    return DJSet




def fileReader():
    with open('DJSetInput.txt', 'w') as writer:
        writer.write(DJSetInput())
        writer.close()
    
    with open('DJSetInput.txt', 'r') as reader:
        # Read & print the entire file
        return(reader.read())



def printReccomendations():
    if fileReader() == "2015-01-02 - Floating Points & Four Tet @ Plastic People Closing Party, London":
        return "[0:00:00] Azimuth - The Tunnel\n[0:09:11] Conjunto Carcará - A Night In Tunisia\n[0:11:26] As Sublimes - Mangueira é Cancáo"

print(printReccomendations())