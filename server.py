from flask import Flask, request, Response
import json
from slackclient import SlackClient
from firebase import firebase

app = Flask(__name__)

class tictactoe:

	_firstPlayer = 'NOPLAYER'
	_secondPlayer = 'NOPLAYER'
	_firstPlayerSymbol = 'X'
	_secondPlayerSymbol = 'O'
	_gameOn = False
	_boardValues = ['-','-','-','-','-','-','-','-','-'] 
	_nextTurn = 'NOPLAYER'

	def __init__(self):
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
		return(json.loads(json_input))

	def updateFromServer(self):
		global firebase
		data = firebase.get('/game', None)
		dataValues = self.deserialize(data['master'])
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
			temp = self.boardValues
			temp[i] = newValue
			self.boardValues = temp
			self.flipTurn()
			self.update()
		return "Invalid position"

	@property 
	def boardValues(self):
		return self.__class__._boardValues

	@property 
	def gameOn(self):
		return self.__class__._gameOn

	@gameOn.setter
	def gameOn(self, newValue):
		self.__class__._gameOn = newValue

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
		headerString = '\n*1 2 3  \n'
		topLineString = 'a '+self.boardValues[0]+' '+self.boardValues[1]+' '+self.boardValues[2]+'\n'
		middleLineString = 'b '+self.boardValues[3]+' '+self.boardValues[4]+' '+self.boardValues[5]+'\n'
		bottomLineString = 'c '+self.boardValues[6]+' '+self.boardValues[7]+' '+self.boardValues[8]+'\n'
		outputString = headerString+topLineString+middleLineString+bottomLineString
		return outputString

	@property
	def firstPlayer(self):
		return self.__class__._firstPlayer

	@property 
	def secondPlayer(self):
		return self.__class__._secondPlayer

	@firstPlayer.setter
	def firstPlayer(self, newValue):
		self.__class__._firstPlayer = newValue

	@secondPlayer.setter
	def secondPlayer(self, newValue):
		self.__class__._secondPlayer = newValue

	@property
	def firstPlayerSymbol(self):
		return self.__class__._firstPlayerSymbol

	@property
	def secondPlayerSymbol(self):
		return self.__class__._secondPlayerSymbol
	
	@firstPlayerSymbol.setter
	def firstPlayerSymbol(self, newValue):
		self.__class__._firstPlayerSymbol = newValue

	@secondPlayerSymbol.setter
	def secondPlayerSymbol(self, newValue):
		self.__class__._secondPlayerSymbol = newValue

	def checkGameEndCondition(self):
		tboardValues = self.boardValues
		if ((tboardValues[0] == tboardValues[1] == tboardValues[2] == self.firstPlayerSymbol)
			or (tboardValues[3] == tboardValues[4] == tboardValues[5] == self.firstPlayerSymbol)
			or (tboardValues[6] == tboardValues[7] == tboardValues[8] == self.firstPlayerSymbol)
			or (tboardValues[0] == tboardValues[3] == tboardValues[6] == self.firstPlayerSymbol)
			or (tboardValues[1] == tboardValues[4] == tboardValues[7] == self.firstPlayerSymbol)
			or (tboardValues[2] == tboardValues[5] == tboardValues[8] == self.firstPlayerSymbol)
			or (tboardValues[0] == tboardValues[4] == tboardValues[8] == self.firstPlayerSymbol)
			or (tboardValues[2] == tboardValues[4] == tboardValues[6] == self.firstPlayerSymbol)):
			return self.firstPlayer
		if ((tboardValues[0] == tboardValues[1] == tboardValues[2] == self.secondPlayerSymbol)
			or (tboardValues[3] == tboardValues[4] == tboardValues[5] == self.secondPlayerSymbol)
			or (tboardValues[6] == tboardValues[7] == tboardValues[8] == self.secondPlayerSymbol)
			or (tboardValues[0] == tboardValues[3] == tboardValues[6] == self.secondPlayerSymbol)
			or (tboardValues[1] == tboardValues[4] == tboardValues[7] == self.secondPlayerSymbol)
			or (tboardValues[2] == tboardValues[5] == tboardValues[8] == self.secondPlayerSymbol)
			or (tboardValues[0] == tboardValues[4] == tboardValues[8] == self.secondPlayerSymbol)
			or (tboardValues[2] == tboardValues[4] == tboardValues[6] == self.secondPlayerSymbol)):
			return self.secondPlayer
		if ((tboardValues[0] != '-') and (tboardValues[1] != '-') and (tboardValues[2] != '-') 
			and (tboardValues[3] != '-') and (tboardValues[4] != '-') and (tboardValues[5] != '-')
			and (tboardValues[6] != '-') and (tboardValues[7] != '-') and (tboardValues[8] != '-')):
			return "Draw"
		return -1

	@property
	def nextTurn(self):
		return self.__class__._nextTurn

	@nextTurn.setter
	def nextTurn(self, newValue):
		self.__class__._nextTurn = newValue

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
	return_text = str(executeParams(text,user_name,channel_id, user_id))
	a = {'text':return_text, 'response_type': 'in_channel'}
	return Response(json.dumps(a),  mimetype='application/json')



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
		if game.gameOn:
			return createGameYesResponse()
		else:
			if isValidUsername(subcommand[1:], channel_id, user_id):
				game.firstPlayer = user_name
				game.secondPlayer = subcommand[1:]
				game.nextTurn = user_name
				game.gameOn = True
				game.update()
				return createGameListResponse()
			else:
				return createInvalidUserResponse()
	
	elif subcommand == 'ls' and commandValue == '':
		return createListResponseString()

	elif subcommand == 'put':
		if game.gameOn:
			return createPutResponseString(user_name, commandValue)
		return createNoGameListResponse()

	elif subcommand == 'help':
		return createHelpResponseString() 
	
	else:
		return createInvalidResponseString()

	return "This should not execute. What did you do?"

def createPutResponseString(user_name, commandValue):
	global game
	if game.nextTurn == user_name:
		return createCorrectUserResponse(user_name, commandValue)
	return createInvalidTurnResponse()

def createCorrectUserResponse(user_name, commandValue):
	global game
	game.changeBoardValue(commandValue, game.getSymbol(user_name))
	gameString = createGameListResponse()
	endCondition = game.checkGameEndCondition()
	winString = ''
	if endCondition != -1:
		if endCondition == 'Draw'
			winString = 'It is a draw!'
		else:
			winString = 'The winner is '+ endCondition +' \n'
		game = tictactoe()
	outputString = gameString + winString
	return outputString

def createInvalidTurnResponse():
	global game
	invalidTurnString = "Sorry, It's "+game.nextTurn+" turn"
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
	if game.gameOn:
		outputString = createGameListResponse()
	else:
		outputString = createNoGameListResponse()
	return outputString

def createGameListResponse():
	global game
	firstPlayerString = 'First Player : ' + game.firstPlayer +' '+ game.firstPlayerSymbol+' \n'
	secondPlayerString = 'Second Player : '+ game.secondPlayer +' '+ game.secondPlayerSymbol+' \n'
	gameString = game.getBoard()
	nextTurnString = 'Turn: ' + game.nextTurn+ '\n'
	outputString = firstPlayerString + secondPlayerString + gameString + nextTurnString
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
	response = sc.api_call("users.list")
	for user in response['members']:
		if user['name'] == username:
			return True
	return False


if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 8000)

sc = SlackClient('xoxp-98588410882-98566920132-101647984725-1587c9429306264be388b906421cf154')
firebase = firebase.FirebaseApplication('https://sttt-52a44.firebaseio.com/', None)
game = tictactoe()