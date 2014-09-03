import deck
import card

#All needed code for the function of the dealer
#Basically keeps hitting until his score is greater than or equal to 17
#Playing on the concept of a hard 17

def init(currentDeck):
  dealerHand = []
  for x in range (0,2):
    dealerHand.append(currentDeck[0])
    currentDeck.remove(currentDeck[0])
  return dealerHand

def endgame(dealerHand, currentDeck):
  while(valOfHand(dealerHand) <=17):
    dealerHand.append(currentDeck[0])
    currentDeck.remove(currentDeck[0])

def showDealerHand(dealerHand):
  dispHand = []
  for card in dealerHand:
    dispHand.append(card)
  return dispHand

def showPartial(dealerHand):
  print "The face up card is the: "
  print dealerHand[0][0], " of ", dealerHand[0][1]
