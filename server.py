from flask import Flask, request
import json
from slackclient import SlackClient
from firebase import firebase

app = Flask(__name__)

class tictactoe:

	firstPlayer = 'NOPLAYER'
	secondPlayer = 'NOPLAYER'
	firstPlayerSymbol = 'X'
	secondPlayerSymbol = 'O'
	gameOn = False
	boardValues = ['-','-','-','-','-','-','-','-','-'] 
	nextTurn = 'NOPLAYER'

	def __init__(self, firstPlayer=None, secondPlayer=None,gameStatus=True):
		global firebase
		self.firstPlayer = 'NOPLAYER'
		self.secondPlayer = 'NOPLAYER'
		self.firstPlayerSymbol = 'X'
		self.secondPlayerSymbol = 'O'
		self.gameOn = False
		self.boardValues = ['-','-','-','-','-','-','-','-','-'] 
		self.nextTurn = 'NOPLAYER'
		json_format = self.serialize()
		firebase.put('/game', 'master', json_format)

	def serialize(self):
		return json.dumps(self, default=lambda o: o.__dict__)

	def deserialize(self, json_input):
		return json.loads(json_input)

	def updateFromServer(self):
		global firebase
		data = firebase.get('/game', None)
		dataValues = data['master']
		self.firstPlayer = dataValues['firstPlayer']
		self.secondPlayer = dataValues['secondPlayer']
		self.firstPlayerSymbol = dataValues['firstPlayerSymbol']
		self.secondPlayerSymbol = dataValues['secondPlayerSymbol']
		self.gameOn = dataValues['gameOn']
		self.boardValues = dataValues['boardValues'] 
		self.nextTurn = dataValues['nextTurn']

	def update(self):
		global firebase
		json_format = self.serialize()
		firebase.put('/game','master',json_format)

	def getSymbol(self, user):
		if user == self.firstPlayer:
			return self.firstPlayerSymbol
		return self.secondPlayerSymbol

	def changeBoardValue(self, position, newValue):
		i = self.getBoardIndex(position)
		if i != -1:
			self.boardValues[i] = newValue
			self.flipTurn()
			self.update()
		return "Invalid position"

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

	def getBoard(self):
		headerString = '*1 2 3  \n'
		topLineString = 'a '+self.boardValues[0]+' '+self.boardValues[1]+' '+self.boardValues[2]+'\n'
		middleLineString = 'b '+self.boardValues[3]+' '+self.boardValues[4]+' '+self.boardValues[5]+'\n'
		bottomLineString = 'c '+self.boardValues[6]+' '+self.boardValues[7]+' '+self.boardValues[8]+'\n'
		outputString = headerString+topLineString+middleLineString+bottomLineString
		return outputString

	def getFirstPlayer(self):
		print("Meow1")
		return self.firstPlayer

	def getSecondPlayer(self):
		return self.secondPlayer

	def changeFirstPlayer(self, newValue):
		self.firstPlayer = newValue

	def changeSecondPlayer(self, newValue):
		self.secondPlayer = newValue

	def getFirstPlayerSymbol(self):
		print("Meow")
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

	def getNextTurn(self):
		return self.nextTurn

	def changeNextTurn(self, newValue):
		self.nextTurn = newValue

	def flipTurn(self):
		if self.nextTurn == self.firstPlayer:
			self.nextTurn = self.secondPlayer
		else:
			self.nextTurn = self.firstPlayer

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

	params = str(text).split(" ")	
	subcommand = ''
	commandValue = ''
	if len(params)>1:
		commandValue = params[1]
	
	if params[0] == '':
		subcommand = 'help'
	else:
		subcommand = params[0]

	game.updateFromServer()

	if subcommand[0] == '@' and commandValue == '':
		print("Here")
		if game.getGameStatus():
			print("Here1")
			return createGameYesResponse()
		else:
			print("Here2")
			if isValidUsername(subcommand[1:], channel_id, user_id):
				print("Here3")				
				game.changeFirstPlayer(user_name)
				print("Here4")
				game.changeSecondPlayer(subcommand[1:])
				print("Here5")
				game.changeNextTurn(user_name)
				print("Here6")
				game.changeGameStatus(True)
				game.update()
				print(game.firstPlayer)
				print("Here7")
				return createGameListResponse()
			else:
				print("Here8")
				return createInvalidUserResponse()
	
	elif subcommand == 'ls' and commandValue == '':
		return createListResponseString()

	elif subcommand == 'put':
		print("Here9")
		if game.getGameStatus():
			print("Here10")
			return createPutResponseString(user_name, commandValue)
		return createNoGameListResponse()

	elif subcommand == 'help':
		return createHelpResponseString() 
	
	else:
		return createInvalidResponseString()

	return "This should not execute. What did you do?"

def createPutResponseString(user_name, commandValue):
	global game
	if game.getNextTurn() == user_name:
		return createCorrectUserResponse(user_name, commandValue)
	return createInvalidTurnResponse()

def createCorrectUserResponse(user_name, commandValue):
	global game
	game.changeBoardValue(commandValue, game.getSymbol(user_name))
	gameString = createGameListResponse()
	endCondition = game.checkGameEndCondition()
	winString = ''
	if endCondition != -1:
		winString = 'The winner is '+ endCondition
		game = tictactoe()
	outputString = gameString + winString
	return outputString

def createInvalidTurnResponse():
	global game
	invalidTurnString = "Sorry, It's "+game.getNextTurn()+" turn"
	outputString = invalidTurnString
	return outputString

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
	global game
	if game.getGameStatus():
		outputString = createGameListResponse()
	else:
		outputString = createNoGameListResponse()
	return outputString

def createGameListResponse():
	print("gamelist")
	global game
	print("gamelist1")
	firstPlayerString = 'First Player : ' + game.getFirstPlayer() +' '+ game.getFirstPlayerSymbol() 
	print("gamelist2")
	secondPlayerString = 'Second Player : '+ game.getSecondPlayer() +' '+ game.getSecondPlayerSymbol()
	print("gamelist3")
	gameString = game.getBoard()
	print("gamelist4")
	nextTurnString = 'Turn: ' + game.getNextTurn()
	print("gamelist5")
	outputString = firstPlayerString + secondPlayerString + gameString + nextTurnString
	print(outputString)
	return outputString

def createNoGameListResponse():
	noGameString = 'Seems like there isn\'t any ttt game on right now.\n Use /ttt @username to challenge someone'
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

sc = SlackClient('xoxp-98588410882-98566920132-101647984725-1587c9429306264be388b906421cf154')
firebase = firebase.FirebaseApplication('https://sttt-52a44.firebaseio.com/', None)
game = tictactoe()