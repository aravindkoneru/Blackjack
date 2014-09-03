import deck
from Tkinter import *
import tkSimpleDialog
from tkFileDialog import *
import tkMessageBox
import os
import pickle

#Inputs a hand as a list and returns the value of the hand
def valOfHand(hand):
  #shift the ace to the end of the hand
  handLen = len(hand)
  for x in range(handLen-1):
    if(hand[x][0] == "Ace"):
      ace = hand[x]
      replace = hand[handLen-1]
      hand[x] = replace
      hand[handLen-1] = ace
  #calculate value of hand
  val = 0
  for x in hand:
    if(type(x[0]) == int):
      val += x[0]
    elif(type(x[0]) == str and not x[0] == "Ace"):
      val += 10
    elif(x[0] == "Ace"):
      if(val < 11):
        val += 11
      else:
        val += 1
  return val

#Draws the score of the player's hand in the bottom right of the screen
#Draws busted if the player busts
def drawValueOfPlayerHand():
  if(canvas.data.playerHandVal <= 21):
    canvas.create_text(70, 425, text="Value of Player Hand: "+str(canvas.data.playerHandVal), \
                       font=("Helvetica", 12, "bold"), anchor="center")
  else:
    canvas.create_text(70, 425, text = "BUSTED!", font = ("Helvetica", 12, "bold"), anchor = "center")

#Draws the score of the dealer's hand in the top right of the screen
#Draws busted if the dealer busts
def drawValueOfDealerHand():
  if(canvas.data.dealerHandVal <= 21):
    canvas.create_text(70, 25, text="Value of Dealer Hand: "+str(canvas.data.dealerHandVal), \
                       font=("Helvetica", 12, "bold"), anchor="center")
  else:
    canvas.create_text(70, 25, text = "BUSTED!", font = ("Helvetica", 12, "bold"), anchor = "center")

#Adds a card and a photoImage to the dealer's hand
#Redraws the board
def hitDealer():
  if(canvas.data.dealerHandVal > 21):
    canvas.data.dealerBusted = True
  if(canvas.data.dealerHandVal < 17):
    playingDeck = canvas.data.playingDeck
    currentCard = playingDeck[0]
    dealerCardImages = canvas.data.dealerCardImages
    dealerHand = canvas.data.dealerHand
    fileName = "%s%s.gif" % (currentCard[0], currentCard[1])
    dealerCardImages.append(PhotoImage(file = fileName))
    dealerHand = canvas.data.dealerHand.append(currentCard)
    playingDeck = playingDeck.remove(playingDeck[0])
    canvas.data.dealerHandVal = valOfHand(canvas.data.dealerHand)
  else:
    canvas.data.dealerDone = True
  redrawAllPlayer()
  redrawAllDealer()

#Redraw's all of the dealer's cards and his score
def redrawAllDealer():
  dealerHand = canvas.data.dealerHand
  offset = 50
  countX = 0
  countY = 0
  count = 0
  dealerCardImages = canvas.data.dealerCardImages
  drawValueOfDealerHand()

  while(count < len(dealerCardImages)):
    yCord = 100 + offset*countY
    xCord = 50 + offset * countX
    if(xCord > 450):
      countY += 1
      countX = 0
      yCord = 100 + offset*countY
      xCord = 50 + offset*countX
      drawCard(count, xCord, yCord, dealerCardImages)
    else:
      drawCard(count, xCord, yCord, dealerCardImages)
    countX += 1
    count += 1

#Changes the status of the playerDone to true and simulates the dealer's turn
def stay():
  canvas.data.playerDone = True
  dealerTurn()

#Called after stay, this method tells the dealer to keep hitting until he hits 17 or bigger
#then calls the determine winner method
def dealerTurn():
  while(canvas.data.dealerDone == False):
    hitDealer()
  determineWinner()

#Determines who the winner of the game is
def determineWinner():
  playerHand = canvas.data.playerHandVal
  dealerHand = canvas.data.dealerHandVal

  if(playerHand > dealerHand and canvas.data.playerBusted == False):
    canvas.create_text(400, 225, text = "You won this hand!\nKeep playing and win more!", font = ("Helvetica", 12, "bold"), anchor = "center")
    canvas.data.totalAmount += canvas.data.bet*(3/2)
  elif(canvas.data.dealerBusted == True):
    canvas.create_text(400, 225, text = "You won this hand!\nKeep playing and win more!", font = ("Helvetica", 12, "bold"), anchor = "center")
    canvas.data.totalAmount += canvas.data.bet*(3/2)
  else:
    canvas.create_text(400, 225, text = "You lost this hand...\nYou'll do better next time!", font = ("Helvetica", 12, "bold"), anchor = "center")
    canvas.data.totalAmount -= canvas.data.bet

#Adds a card and a photoImage to the player's hand
#Redraws the whole game afterwards
def hit():
  if(canvas.data.playerHandVal < 22 and canvas.data.playerDone == False):
    playingDeck = canvas.data.playingDeck
    currentCard = playingDeck[0]
    playerCardImages = canvas.data.playerCardImages
    fileName = "%s%s.gif" % (currentCard[0], currentCard[1])
    playerCardImages.append(PhotoImage(file = fileName))
    playerHand = canvas.data.playerHand.append(currentCard)
    playingDeck = playingDeck.remove(playingDeck[0])
    canvas.data.playerHandVal = valOfHand(canvas.data.playerHand)
    redrawAllPlayer()
    redrawAllDealer()
    if(canvas.data.playerHandVal > 21):
      canvas.data.playerBusted = True
      stay()

#Redraw's the player's cards and the player's score
def redrawAllPlayer():
  playerHand = canvas.data.playerHand
  offset = 50
  countX = 0
  countY = 0
  count = 0
  playerCardImages = canvas.data.playerCardImages
  canvas.delete(ALL)
  drawTable()
  drawValueOfPlayerHand()
  drawValueOfDealerHand()

  while(count < len(playerCardImages)):
    yCord = 350 + offset*countY
    xCord = 50 + offset * countX
    if(xCord > 450):
      countY += 1
      countX = 0
      yCord = 350 + offset*countY
      xCord = 50 + offset*countX
      drawCard(count, xCord, yCord, playerCardImages)
    else:
      drawCard(count, xCord, yCord, playerCardImages)
    countX += 1
    count += 1

#Draws the card given the x,y position, cardNum, and the name of the hand
def drawCard(counter, xC, yC, typeList):
  canvas.create_image(xC, yC, anchor = "center", image = typeList[counter])

#Draws the table and also the card in the center of the board
def drawTable():
  canvas.create_rectangle(0,0,500,500, fill = "#348017")
  canvas.create_image(250,225, anchor = "center", image = canvas.data.topCard)
  canvas.create_text(75, 225, text = "Bank: $%d" % canvas.data.totalAmount, font = ("Helvetica", 12, "bold"), anchor = "center")
  canvas.create_text(75, 250, text = "Current Bet: $%d" % canvas.data.bet, font = ("Helvetica", 12, "bold"), anchor = "center")

#Initializes all of the needed variables and other aspects of the game
def init():
  playingDeck = deck.createDeck()
  playingDeck = deck.shuffle(playingDeck)
  canvas.data.playingDeck = playingDeck #stores list of cards in deck
  canvas.data.playerHand = []#stores list of cards in player's hand
  canvas.data.dealerHand = []#stores list of cards in dealer's hand
  canvas.data.playerCardImages = []#stores list of images in player's hand
  canvas.data.playerHandVal = 0#stores value of player's hand
  canvas.data.totalAmount = 1000#stores value of money in the bank
  canvas.data.bet = 0#stores the value of the bet
  canvas.data.dealerHandVal = 0#stores value of dealer hand
  canvas.data.dealerCardImages = []#stores list of images in dealer's hand
  canvas.data.topCard = PhotoImage(file = "155.gif")#stores the image of the top of the card
  canvas.data.dealerDone = False#stores the boolean value to determine if the dealer is done playing
  canvas.data.playerDone = False#stores the boolean value to determine if the player is done playing
  canvas.data.playerBusted = False#stores the boolean value to determine if the player busted
  canvas.data.dealerBusted = False#stores the boolean value to the determine if the dealer busted
  promptForBet()#gets and stores the bet
  drawTable()#draws the green table and also the bank amount and bet amount
  setUpBoard()#hits the player twice, hits the dealer once
  drawValueOfPlayerHand()#draws the value of the player's hand
  drawValueOfDealerHand()#draws the value of teh dealer's hand

#resets all values except bank
def resetGame():
  if(canvas.data.totalAmount > 0 and canvas.data.playerDone and canvas.data.dealerDone):
    playingDeck = deck.createDeck()
    playingDeck = deck.shuffle(playingDeck)
    canvas.data.playingDeck = playingDeck #stores list of cards in deck
    canvas.data.playerHand = []#stores list of cards in player's hand
    canvas.data.dealerHand = []#stores list of cards in dealer's hand
    canvas.data.playerCardImages = []#stores list of images in player's hand
    canvas.data.playerHandVal = 0#stores value of player's hand
    canvas.data.bet = 0#stores the value of the bet
    canvas.data.dealerHandVal = 0#stores value of dealer hand
    canvas.data.dealerCardImages = []#stores list of images in dealer's hand
    canvas.data.dealerDone = False
    canvas.data.playerDone = False
    canvas.data.playerBusted = False
    canvas.data.dealerBusted = False
    promptForBet()
    drawTable()
    setUpBoard()
    drawValueOfPlayerHand()
    drawValueOfDealerHand()
  elif(canvas.data.totalAmount <= 0 and canvas.data.playerDone and canvas.data.dealerDone):
    tkMessageBox.showinfo(title = "You Lost", message = "Congratulations! You are bad at gambling!\nThis game will now exit.")
    root.destroy()

#sets up the board by dealing two cards (player) and showing one card (dealer)
def setUpBoard():
  hit()
  hit()
  hitDealer()

#Takes key input and converts to actions
def keyPressed(event):
  if(event.keysym == "Tab"):
    splashScreen()

#Shows a splash screen with help at the beginning of video.
#is callable by pressing tab
def splashScreen():
  labelText = "Welcome to Blackjack. These are the house rules:\n\
              1. The dealer must stay at 17\n\
              2. If the dealer busts, then the player wins\n\
              3. If the player and the dealer bust, then the player wins\n\
              4. If both the player and the dealer tie, the dealer wins\n\
              Press the tab button to see this splash screen again"
  splash = Tk()
  splash.overrideredirect(True)
  splashCanvas = Canvas(splash, height=500, width=500, bg="#348017")
  splashCanvas.pack()
  splashLabel =   Label(splash, text = labelText, bg = "#348017", fg = "white", anchor = "center")
  splashLabel.place(x = 50, y = 200)
  closeButton = Button(splash, text = "Continue", width = 10, command = splash.destroy)
  closeButton.place(x = 225, y = 450)
  splash.mainloop()

#prompts the user for the bet
def promptForBet():
  canvas.data.bet = tkSimpleDialog.askinteger(title = "Bet Entry", prompt = "Enter your bet:", minvalue = 10, maxvalue = canvas.data.totalAmount)

def createDict():
	gameData = {"playingDeck":canvas.data.playingDeck,
				"playerHand":canvas.data.playerHand,
				"dealerHand": canvas.data.dealerHand,
				#"playerCardImages": canvas.data.playerCardImages,
				"playerHandVal": canvas.data.playerHandVal,
				"totalAmount":canvas.data.totalAmount,
				"bet":canvas.data.bet,
				"dealerHandVal": canvas.data.dealerHandVal,
				#"dealerCardImages": canvas.data.dealerCardImages,
				"dealerDone": canvas.data.dealerDone,
				"playerDone":canvas.data.playerDone,
				"playerBusted": canvas.data.playerBusted,
				"dealerBusted": canvas.data.dealerBusted}
	return gameData


def getFileName(directory):
	slashPos = directory.rfind("/")
	return directory[slashPos+1:]

def getDirectoryName(directory):
	slashPos = directory.rfind("/")
	canvas.data.currentDir = directory[:slashPos]
	return directory[:slashPos]

def openFile():
	fileDirectory = askopenfilename() # show an "Open" dialog box and return the path to the selected file
	oldDirectory = os.getcwd()
	os.chdir(getDirectoryName(fileDirectory))
	fileName = getFileName(fileDirectory)
	gameData = pickle.load(open(fileName, "rb"))
	os.chdir(oldDirectory)
	loadGame(gameData)

def saveFile():
	fileDirectory = askdirectory() # show an "Open" dialog box and return the path to the selected file
	oldDirectory = os.getcwd()
	os.chdir(fileDirectory)
	fileName = tkSimpleDialog.askstring(title = "Save Game", prompt = "Enter name of file")
	fileName = fileName + ".p"
	gameData = createDict()
	pickle.dump(gameData, open(fileName, "w+"))
	os.chdir(oldDirectory)

def loadGame(gameData):
	canvas.data.playingDeck = gameData["playingDeck"]
	canvas.data.playerHand = gameData["playerHand"]
	canvas.data.dealerHand = gameData["dealerHand"]
	canvas.data.playerHandVal = gameData["playerHandVal"]
	canvas.data.totalAmount = gameData["totalAmount"]
	canvas.data.bet = gameData["bet"]
	canvas.data.dealerHandVal = gameData["dealerHandVal"]
	canvas.data.playerDone = gameData["playerDone"]
	canvas.data.dealerDone = gameData["dealerDone"]
	canvas.data.playerBusted = gameData["playerBusted"]
	canvas.data.dealerBusted = gameData["dealerBusted"]
	canvas.data.playerCardImages = []
	canvas.data.dealerCardImages = []
	for card in canvas.data.playerHand:
		fileName = "%s%s.gif" % (card[0], card[1])
		canvas.data.playerCardImages.append(PhotoImage(file = fileName))
	for card in canvas.data.dealerHand:
		fileName = "%s%s.gif" % (card[0], card[1])
		canvas.data.dealerCardImages.append(PhotoImage(file = fileName))
	drawTable()
	redrawAllPlayer()
	redrawAllDealer()
	drawValueOfPlayerHand()
	drawValueOfDealerHand()

#Main method used to run the game
def run():
  splashScreen()
  global canvas
  global root
  root = Tk()
  menubar = Menu(root)
  canvas = Canvas(root, width = 500, height = 500)
  root.resizable(width=0, height=0)
  canvas.pack()
  img = PhotoImage(file = "blackjack_icon.gif")
  canvas.tk.call('wm', 'iconphoto', root._w, img)
  root.title("Blackjack")
  class Struct: pass
  canvas.data = Struct()
  init()
  canvas.data.windowWidth = 500
  canvas.data.windowHeight = 500
  hitButton = Button(root, text = "Hit", width = 10, command = hit)
  hitButton.place(x = 200, y = 450)
  stayButton = Button(root, text = "Stand", width = 10, command = stay)
  stayButton.place(x = 50, y = 450)
  resetButton = Button(root, text = "Deal Again", width = 10, command = resetGame)
  resetButton.place(x = 350, y = 450)
  root.bind("<Key>", keyPressed)
  filemenu = Menu(menubar, tearoff=0)
  filemenu.add_command(label="Load", command=openFile)
  filemenu.add_command(label="Save", command=saveFile)
  filemenu.add_separator()
  filemenu.add_command(label="Exit", command=root.quit)
  menubar.add_cascade(label="File", menu=filemenu)
  root.config(menu=menubar)
  root.mainloop()

run()
