def hitMe(currentDeck, playerHand):
  playerHand.append(currentDeck[0])
  currentDeck.remove(currentDeck[0])

def valOfHand(hand):
  val = 0
  for x in hand:
    if(type(x[0]) == int):
      val += x[0]
    elif(type(x[0]) == str and not x[0] == "Ace"):
      val += 10
    elif(x[0] == "Ace"):
      if(val < 11):
        val += 10
      else:
        val += 1
  return val

def readCards(playerHand):
  print "Your hand:"
  for card in playerHand:
    print card[0], " of ", card[1]
  print "The Value of your hand: ", valOfHand(playerHand)
