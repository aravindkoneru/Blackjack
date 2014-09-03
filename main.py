import dealer
import deck
import bank
import playerCommands

playingDeck = []

dealerHand = []
playerHand = []

totalAmount = 0
bet = 0
numDecks = 0

print "Welcome to blackjack. The ratio is 3:2"

#Allows the user to choose the number of decks that they will play with
while(numDecks == 0):
  print "How many decks would you like to play with? (enter a number): ",
  try:
    numDecks = int(raw_input())
  except:
    numDecks = 0
    continue

#Allows the user to set up the bank for bets in the future
while(totalAmount == 0):
  print "How much would you like to have in the bank? (enter a number): ",
  try:
    totalAmount = int(raw_input())
  except:
    totalAmount = 0
    continue

print "You are playing with %d decks and have $%d to bet." % (numDecks, totalAmount)

#Creates by playingDeck by adding and shuffling x number of decks as specified by the user
for x in range(0, numDecks):
  playingDeck += deck.createDeck()
  playingDeck = deck.shuffle(playingDeck)

#Makes the user place their bet
while(bet == 0):
  print "How much would you like to bet? (enter a number): ",
  try:
    bet = int(raw_input())
  except:
    bet == 0
    continue

dealerHand = dealer.init(playingDeck)

playerCommands.hitMe(playingDeck, playerHand)
playerCommands.hitMe(playingDeck, playerHand)

dealer.showPartial(dealerHand)
print "Value of Dealer Hand: ", playerCommands.valOfHand(dealerHand)
playerCommands.readCards(playerHand)

dealerVal = playerCommands.valOfHand(dealerHand)
playerVal = playerCommands.valOfHand(playerHand)

if(playerVal == 21):
  print "Black Jack! You win $%d!" % bet
  totalAmount += bet
else:
  hit = True
  while(hit and playerVal < 22):
    print "Do you want to hit? (Y or N): ",
    try:
      answer = raw_input().upper()
      if not(answer == "Y" or answer == "N"):
        raise InvalidInputError()
    except:
      print "Invalid answer. Enter Y or N"
      continue
    if(answer == "Y"):
      playerCommands.hitMe(playingDeck, playerHand)
      playerVal = playerCommands.valOfHand(playerHand)
      playerCommands.readCards(playerHand)
    elif(answer == "N"):
      hit = False
      break

if(playerVal > 21):
  print "BUSTED BITCH!"
  totalAmount -= bet
