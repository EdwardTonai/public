# Takes the shorthand used to identify a card and translates it into english
def TranslateCard(cardString):
    gem = {
        'D': 'Diamond',
        'S': 'Sapphire',
        'E': 'Emerald',
        'R': 'Ruby',
        'T': 'Topaz'
        }[cardString[0]]
    level = "L:" + cardString[1]
    cardNumber = cardString[2] + "."
    cost = ''
    if int(cardString[3]) > 0:
        cost += "Diamond " + cardString[3] + " "
    if int(cardString[4]) > 0:
        cost += "Sapphire " + cardString[4] + " "
    if int(cardString[5]) > 0:
        cost += "Emerald " + cardString[5] + " "
    if int(cardString[6]) > 0:
        cost += "Ruby " + cardString[6] + " "
    if int(cardString[7]) > 0:
        cost += "Topaz " + cardString[7] + " "
    value = "Value: " + cardString[8]
    translation = gem + " " + level + " " + cardNumber + " " + cost + value
    return translation

def TranslateCardFile(fileName):
    infile = open(fileName)
    for line in infile:
        print TranslateCard(line)


