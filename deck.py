import card
import random

cType = ["Diamond", "Spade", "Heart", "Club"]
cVal = [2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"]
#Creates the final deck that will be used during the game
#This method basically initalizes the deck and makes it suitable for gameplay
#Creates the deck by creating an instance of every possible card combination and adding it to the deck
#The format of the cards added to the deck is (cardValue, cardSuit)
def createDeck():
  currentDeck = []
  for x in cType:
    for y in cVal:
      addToDeck = card.createCard(x,y)
      currentDeck.append(addToDeck)
  return currentDeck

#Suffles the deck after it has been initalized by the createDeck() method
#Picks two random indexes in the deck and swaps the positions of their values
#This method ensures that the most random and realistic shuffle occurs
def shuffle(currentDeck):
  x = 0
  while(x < len(currentDeck)):
    posOne = random.randint(0,len(currentDeck)-1)
    posTwo = random.randint(0,len(currentDeck)-1)
    temp = currentDeck[posOne]
    currentDeck[posOne] = currentDeck[posTwo]
    currentDeck[posTwo] = temp
    x += 1
  return currentDeck

#Displays the deck
def showDeck(currentDeck):
  for card in currentDeck:
    print card
