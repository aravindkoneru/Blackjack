#This is the card class:
#cards make up the deck
#allows for alot of redundant code to be abolished from the deck functions

  #Automatically creates a card when a card object has been initalized
def createCard(suit, val):
  return [val, suit]
