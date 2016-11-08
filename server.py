from flask import Flask, request
import json
from slackclient import SlackClient
from firebase import firebase

app = Flask(__name__)

class tictactoe:
	'Base class from Tic Tac Toe Game'
	boardValues = ['-','-','-','-','-','-','-','-','-']
	gameOn = False
	firstPlayerSymbol = 'X'
	secondPlayerSymbol = 'O'

	def __init__(self, firstPlayer=None, secondPlayer=None,gameStatus=True):
		self.firstPlayer = firstPlayer
		self.secondPlayer = secondPlayer
		self.gameOn = gameStatus
		self.nextTurn = self.firstPlayer
		self.clearBoard()

	def peekBoardValue(self, position):
		idx = self.getBoardIndex(position) 
		if idx != -1:
			return self.boardValues[idx]
		return -1

	def changeBoardValue(self, position, newValue):
		i = self.getBoardIndex(position)
		if i != -1:
			self.boardValues[i] = newValue
		return self.boardValues

	def clearBoard(self):
		self.boardValues = ['-','-','-','-','-','-','-','-','-']

	def getGameStatus(self):
		return self.gameOn

	def changeGameStatus(self, newValue):
		self.gameOn = newValue

	def getBoardIndex(self, position):
		return {
			'a1':0,
			'a2':1,
			'a3':2,
			'b1':3,
			'b2':4,
			'b3':5,
			'c1':6,
			'c2':7,
			'c3':8,
		}.get(position,-1)

	def currentGameStatus(self):
		return self.gameOn

	def changeGameStatus(self, newValue):
		self.gameOn = newValue

	def currentBoardString(self):
		header = '*1 2 3  \n'
		topLine = 'a '+self.boardValues[0]+' '+self.boardValues[1]+' '+self.boardValues[2]+'\n'
		middleLine = 'b '+self.boardValues[3]+' '+self.boardValues[4]+' '+self.boardValues[5]+'\n'
		bottomLine = 'c '+self.boardValues[6]+' '+self.boardValues[7]+' '+self.boardValues[8]+'\n'
		output = header+topLine+middleLine+bottomLine
		return output

	def getFirstPlayer(self):
		return self.firstPlayer

	def getSecondPlayer(self):
		return self.secondPlayer

	def changeFirstPlayer(self, newValue):
		self.firstPlayer = newValue

	def changeSecondPlayer(self, newValue):
		self.secondPlayer = newValue

	def getFirstPlayerSymbol(self):
		return self.firstPlayerSymbol

	def getSecondPlayerSymbol(self):
		return self.secondPlayerSymbol

	def changeFirstPlayerSymbol(self, newValue):
		self.firstPlayerSymbol = newValue

	def changeSecondPlayerSymbol(self, newValue):
		self.secondPlayerSymbol = newValue

	def checkGameEndCondition(self):
		if ((self.boardValues[0] == self.boardValues[1] == self.boardValues[2] == self.firstPlayerSymbol)
			or (self.boardValues[3] == self.boardValues[4] == self.boardValues[5] == self.firstPlayerSymbol)
			or (self.boardValues[6] == self.boardValues[7] == self.boardValues[8] == self.firstPlayerSymbol)
			or (self.boardValues[0] == self.boardValues[3] == self.boardValues[6] == self.firstPlayerSymbol)
			or (self.boardValues[1] == self.boardValues[4] == self.boardValues[7] == self.firstPlayerSymbol)
			or (self.boardValues[2] == self.boardValues[5] == self.boardValues[8] == self.firstPlayerSymbol)
			or (self.boardValues[0] == self.boardValues[4] == self.boardValues[8] == self.firstPlayerSymbol)
			or (self.boardValues[2] == self.boardValues[4] == self.boardValues[6] == self.firstPlayerSymbol)):
			return getFirstPlayer()
		if ((self.boardValues[0] == self.boardValues[1] == self.boardValues[2] == self.secondPlayerSymbol)
			or (self.boardValues[3] == self.boardValues[4] == self.boardValues[5] == self.secondPlayerSymbol)
			or (self.boardValues[6] == self.boardValues[7] == self.boardValues[8] == self.secondPlayerSymbol)
			or (self.boardValues[0] == self.boardValues[3] == self.boardValues[6] == self.secondPlayerSymbol)
			or (self.boardValues[1] == self.boardValues[4] == self.boardValues[7] == self.secondPlayerSymbol)
			or (self.boardValues[2] == self.boardValues[5] == self.boardValues[8] == self.secondPlayerSymbol)
			or (self.boardValues[0] == self.boardValues[4] == self.boardValues[8] == self.secondPlayerSymbol)
			or (self.boardValues[2] == self.boardValues[4] == self.boardValues[6] == self.secondPlayerSymbol)):
			return getSecondPlayer()
		return -1

	def getNextTurn(self, input):
		if input == self.secondPlayer or input == None:
			return self.firstPlayer
		return self.secondPlayer


@app.route("/",methods=['POST','GET'])
def game():
	channel_id = request.form['channel_id']
	token = request.form['token']
	command = request.form['command']
	team_id = request.form['team_id']
	user_id = request.form['user_id']
	response_url = request.form['response_url']
	team_domain = request.form['team_domain']
	channel_name = request.form['channel_name']
	text = request.form['text']
	user_name = request.form['user_name']
	output = str(executeParams(text,user_name,channel_id, user_id))
	return output,200



def executeParams(text,user_name, channel_id, user_id):
	global game 	
	global firebase


	params = str(text).split(" ")	
	subcommand = ''
	commandValue = ''
	if len(params)>1:
		commandValue = params[1]
	if params[0] == '':
		subcommand = 'help'


	intro = firebase.get('/game', None)
	everything = intro['master']


	if subcommand[0] == '@' and commandValue == '':
		if gameOn:
			return createGameYesResponse()
		else:
			if isValidUsername(subcommand[1:], channel_id, user_id):				
				'''board_json = { 'a1':everything['a1'], 'a2':everything['a2'], 'a3':everything['a3'], 'b1':everything['b1'], 'b2':everything['b2'], 'b3':everything['b3'],'c1':everything['c1'],'c2':everything['c2'],'c3':everything['c3'], 'first':user_name, 'second':subcommand[1:], 'firstS':everything['firstS'], 'secondS':everything['secondS'], 'gameOn':True, 'next':user_name }
				firebase.put('/game', 'master', board_json)
				game = tictactoe(user_name, subcommand[1:])
				'''
				return createGameListResponse()
			else:
				return createInvalidUserResponse()
	
	elif subcommand == 'ls' and commandValue == '':
		return createListResponseString()

	elif subcommand == 'put':
		if everything['next'] == user_name:	
			a = game.changeBoardValue(commandValue, 'X')
			pnextTurn = 'Turn: ' + everything['next']
			board_json = { 'a1':a[0], 'a2':a[1], 'a3':a[2], 'b1':a[3], 'b2':a[4], 'b3':a[5],'c1':a[6],'c2':a[7],'c3':a[8], 'first':user_name, 'second':everything['second'], 'firstS':everything['firstS'], 'secondS':everything['secondS'], 'gameOn':True, 'next':pnextTurn }
			firebase.put('/game', 'master', board_json)
			end = game.checkGameEndCondition()
			if end == -1:
				return game.currentBoardString()+pnextTurn
			else:
				game = tictactoe(None, None, False)
				return "The Winner is " + end
		else:
			return "Sorry but it doesn't seem like it's your turn"
	
	elif subcommand == 'help':
		return createHelpResponseString() 
	else:
		return createInvalidResponseString()

	return "This should not execute. What did you do?"

def createHelpResponseString():
	lsString = "/ttt ls: To see an ongoing game\n"
	challengeString = "/ttt @<username>: To challenge someone in the channel \n"
	moveString = "/ttt put <row alphabet><column number>: To put a mark at the position \n"
	helpString = "/ttt help: To see this menu again"
	outputString = lsString+challengeString+moveString+helpString
	return outputString

def createInvalidResponseString():
	invalidString = "Sorry, that doesn't seem like a valid command. \n Use /ttt help to know more"
	outputString  = invalidString
	return outputString

def createListResponseString():
	if gameOn:
		outputString = createGameListResponse()
	outputString = createNoGameListResponse()
	return outputString

def createGameListResponse():
	firstPlayerString = 'First Player : ' + '___GET PLAYER NAME___' + '___GET PLAYER SYMBOL__' 
	secondPlayerString = 'Second Player : '+ '___GET PLAYER NAME___' + '___GET PLAYER SYMBOL__'
	gameString = "__Get from some function__"
	nextTurnString = 'Turn: ' + '__GET FROM SOME FUNCTION OR VARIABLE__'
	outputString = firstPlayerString + secondPlayerString + gameString + nextTurnString
	return outputString

def createNoGameListResponse():
	noGameString = 'Seems like there isn't any ttt game on right now.\n Use /ttt @username to challenge someone'
	outputString = noGameString
	return outputString

def createGameYesResponse():
	gameOnString = 'A ttt game is already on.\n Use /ttt help to know more.'
	outputString = gameOnString
	return outputString

def createInvalidUserResponse():
	invalidString = 'Seems like this user is not in this channel'
	outputString = invalidString
	return outputString

def isValidUsername(username, channel_id, user_id):
	response = sc.api_call("channels.info",channel=channel_id)
	if user_id in response['channel']['members']:
		return True
	return False


if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 8000)


game = tictactoe(None, None, False)
sc = SlackClient('xoxp-98588410882-98566920132-101647984725-1587c9429306264be388b906421cf154')
firebase = firebase.FirebaseApplication('https://sttt-52a44.firebaseio.com/', None)

board_json = { 'a1':game.peekBoardValue('a1'), 'a2':game.peekBoardValue('a2'), 'a3':game.peekBoardValue('a3'), 'b1':game.peekBoardValue('b1'), 'b2':game.peekBoardValue('b2'), 'b3':game.peekBoardValue('b3'),'c1':game.peekBoardValue('c1'),'c2':game.peekBoardValue('c2'),'c3':game.peekBoardValue('c3'), 'first':game.getFirstPlayer(), 'second':game.getSecondPlayer(), 'firstS':game.getFirstPlayerSymbol(), 'secondS':game.getSecondPlayerSymbol(), 'gameOn':game.getGameStatus(), 'next':game.getFirstPlayer() }
