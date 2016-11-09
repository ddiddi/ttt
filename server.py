from flask import Flask, request, Response
import json
from slackclient import SlackClient
from firebase import firebase

app = Flask(__name__)

class tictactoe:
	"""
	Class to keep track of game conditions.
	Member variable are:

	_firstPlayer : Username of the first player
	_secondPlayer : Username of the second player
	_firstPlayerSymbol : Symbol of the first player
	_secondPlayerSymbol : Symbol of the second player
	_gameOn	: Game status variable to track if there in an ongoing game
	_boardValues : Values on the board
	_nextTurn : Variable to keep track of next turn

	"""

	_firstPlayer = 'NOPLAYER'			#First Player Username
	_secondPlayer = 'NOPLAYER'			#Second Player Username
	_firstPlayerSymbol = 'X'			#First Player Symbol
	_secondPlayerSymbol = 'O'			#Second Player Symbol
	_gameOn = False						#Game Status Variable
	_boardValues = ['-','-','-','-','-','-','-','-','-'] 
	_nextTurn = 'NOPLAYER'				#Next Turn

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
		"""
		Used to serialize the class object to JSON to put into the server.
		Args: 
			self: instance of the class
		Returns:
			JSON representation of the the class object
		"""
		return json.dumps(self, default=lambda o: o.__dict__)

	def deserialize(self, json_input):
		"""
		Used to deserialize JSON input into a dictionary.
		Args:
			self: instance of the class
			json_input: input to put converted to dict representation
		Returns:
			dictionary of the JSON input
		"""
		return(json.loads(json_input))

	def updateFromServer(self):
		"""
		Used to update game conditions from the firebase server.
		Args:
			self: instance of the class
		Returns:
			None
		"""
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
		"""
		Used to update game conditions to the firebase server.
		Args:
			self: instance of the class
		Returns:
			None
		"""
		global firebase
		json_format = self.serialize()
		firebase.put('/game','master',json_format)

	def getSymbol(self, user):
		"""
		Used to get corresponding symbol to input player/username.
		Args:
			self: instance of the class
			user: string of username to get symbol
		Returns:
			string Symbol of the provideed user, if present.
		"""
		if user == self.firstPlayer:
			return self.firstPlayerSymbol
		return self.secondPlayerSymbol

	def changeBoardValue(self, position, newValue):
		"""
		Used to update board values. After making the change, the next turn 
		is decided and new game conditions are updated to the server. 
		Args:
			self: instance of the class
			position: position to update the value of in row-col format
			newValue: character to update into board position
		Returns:
			Success or Invalid position string
		"""
		i = self.getBoardIndex(position)
		if i != -1:
			temp = self.boardValues
			temp[i] = newValue
			self.boardValues = temp
			self.flipTurn()
			self.update()
			return "Success"
		return "Invalid position"


	def getBoardIndex(self, position):
		"""
		Used to convert row-col index to list index
		Args:
			self: instance of the class
			position: row-col representation of position
		Returns:
			corresponding index for values on the board
		"""
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
		"""
		Used to get string with current board values.
		Args:
			self: instance of the class
		Returns:
			formatted string with current board values
		"""
		headerString = ' 1     2     3\n'
		topLineString = ' '+self.boardValues[0]+'      '+self.boardValues[1]+'     '+self.boardValues[2]+'  a\n'
		middleLineString = ' '+self.boardValues[3]+'      '+self.boardValues[4]+'     '+self.boardValues[5]+'  b\n'
		bottomLineString = ' '+self.boardValues[6]+'      '+self.boardValues[7]+'     '+self.boardValues[8]+'  c\n'
		outputString = headerString+topLineString+middleLineString+bottomLineString
		return outputString

	@property 
	def boardValues(self):
		return self.__class__._boardValues

	@property 
	def gameOn(self):
		return self.__class__._gameOn

	@gameOn.setter
	def gameOn(self, newValue):
		self.__class__._gameOn = newValue

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
		"""
		Used to check if the game has ended
		Args:
			self: instance of the class
		Returns:
			username if game has ended with a win
			Draw if game has reached a draw stage
			-1 if game is ongoing
		"""
		if ((boardValues[0] == boardValues[1] == boardValues[2] == self.firstPlayerSymbol)
			or (boardValues[3] == boardValues[4] == boardValues[5] == self.firstPlayerSymbol)
			or (boardValues[6] == boardValues[7] == boardValues[8] == self.firstPlayerSymbol)
			or (boardValues[0] == boardValues[3] == boardValues[6] == self.firstPlayerSymbol)
			or (boardValues[1] == boardValues[4] == boardValues[7] == self.firstPlayerSymbol)
			or (boardValues[2] == boardValues[5] == boardValues[8] == self.firstPlayerSymbol)
			or (boardValues[0] == boardValues[4] == boardValues[8] == self.firstPlayerSymbol)
			or (boardValues[2] == boardValues[4] == boardValues[6] == self.firstPlayerSymbol)):
			return self.firstPlayer
		if ((boardValues[0] == boardValues[1] == boardValues[2] == self.secondPlayerSymbol)
			or (boardValues[3] == boardValues[4] == boardValues[5] == self.secondPlayerSymbol)
			or (boardValues[6] == boardValues[7] == boardValues[8] == self.secondPlayerSymbol)
			or (boardValues[0] == boardValues[3] == boardValues[6] == self.secondPlayerSymbol)
			or (boardValues[1] == boardValues[4] == boardValues[7] == self.secondPlayerSymbol)
			or (boardValues[2] == boardValues[5] == boardValues[8] == self.secondPlayerSymbol)
			or (boardValues[0] == boardValues[4] == boardValues[8] == self.secondPlayerSymbol)
			or (boardValues[2] == boardValues[4] == boardValues[6] == self.secondPlayerSymbol)):
			return self.secondPlayer
		if ((boardValues[0] != '-') and (boardValues[1] != '-') and (boardValues[2] != '-') 
			and (boardValues[3] != '-') and (boardValues[4] != '-') and (boardValues[5] != '-')
			and (boardValues[6] != '-') and (boardValues[7] != '-') and (boardValues[8] != '-')):
			return "Draw"
		return -1

	@property
	def nextTurn(self):
		return self.__class__._nextTurn

	@nextTurn.setter
	def nextTurn(self, newValue):
		self.__class__._nextTurn = newValue

	def flipTurn(self):
		"""
		Used to update next turn variable.
		Args:
			self: instance of the class
		Returns:
			None
		"""
		if self.nextTurn == self.firstPlayer:
			self.nextTurn = self.secondPlayer
		else:
			self.nextTurn = self.firstPlayer

@app.route("/",methods=['POST','GET'])
def game():
	"""
	Used to handle / routes and parse request into variables.
	Args:
		None
	Returns:
		Response to Slack interface
	"""	
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
	return_text_json = {'text':return_text, 'response_type': 'in_channel'}
	return Response(json.dumps(return_text_json),  mimetype='application/json')



def executeParams(text,user_name, channel_id, user_id):
	"""
	Used to execute server code based on parsed commands.
	Args:
		text: request from slack
		user_name: username of request creator
		channel_id: channel_id for request
		user_id: unique id for request creator
	Returns:
		String according to params
	"""
	global game 	

	#Split input by space to get subcommand and flags
	params = str(text).split(" ")	
	subcommand = ''
	commandValue = ''
	if len(params)>1:
		commandValue = params[1]
	
	if params[0] == '':
		subcommand = 'help'
	else:
		subcommand = params[0]

	#Update local game instance from server variables
	game.updateFromServer()

	#If request is to challenge another player
	if subcommand[0] == '@' and commandValue == '':
		#Check if a game is already ongoing 
		if game.gameOn:
			return createGameYesResponse()
		else:
			#Check validity of Username
			if isValidUsername(subcommand[1:], channel_id, user_id):
				game.firstPlayer = user_name
				game.secondPlayer = subcommand[1:]
				game.nextTurn = user_name
				game.gameOn = True
				game.update()
				return createGameListResponse()
			else:
				return createInvalidUserResponse()
	
	#If request is to list current game
	elif subcommand == 'ls' and commandValue == '':
		return createListResponseString()

	#If request is to put value in an ongoing game
	elif subcommand == 'put':
		if game.gameOn:
			return createPutResponseString(user_name, commandValue)
		return createNoGameListResponse()

	#If request if to invoke help menu
	elif subcommand == 'help':
		return createHelpResponseString() 
	
	#If request input is invalid
	else:
		return createInvalidResponseString()

	return "This should not execute."

def createPutResponseString(user_name, commandValue):
	"""
	Used to create response if put command is invoked.
	Args:
		user_name: username of put command invoker
		commandValue: value to put in board
	Returns:
		String of put response with updated game variables
	"""
	
	global game
	if game.nextTurn == user_name:
		return createCorrectUserResponse(user_name, commandValue)
	return createInvalidTurnResponse()

def createCorrectUserResponse(user_name, commandValue):
	"""
	Used to put value in board if its users turn
	Args:
		user_name: username of put command invoker
		commandValue: value to put in board
	Returns:
		String of put response with updated game variables
	"""
	global game
	game.changeBoardValue(commandValue, game.getSymbol(user_name))
	gameString = createGameListResponse()
	endCondition = game.checkGameEndCondition()
	winString = ''
	# If a Win or Draw condition is detected
	if endCondition != -1:
		if endCondition == 'Draw':
			winString = 'It is a draw!'
		else:
			winString = 'The winner is '+ endCondition +' \n'
		#New game instance to be created
		game = tictactoe()
	outputString = gameString + winString
	return outputString

def createInvalidTurnResponse():
	"""
	Used to create string response when turn is invalid
	Args:
		None
	Returns:
		String of put response with error response
	"""
	global game
	invalidTurnString = "Sorry, It's "+game.nextTurn+" turn"
	outputString = invalidTurnString
	return outputString

def createHelpResponseString():
	"""
	Used to create string response when help command is invoked
	Args:
		None
	Returns:
		String of put response with help response
	"""
	lsString = "/ttt ls: To see an ongoing game\n"
	challengeString = "/ttt @<username>: To challenge someone in the channel \n"
	moveString = "/ttt put <row alphabet><column number>: To put a mark at the position \n"
	helpString = "/ttt help: To see this menu again"
	outputString = lsString+challengeString+moveString+helpString
	return outputString

def createInvalidResponseString():
	"""
	Used to create string response when command is invalid
	Args:
		None
	Returns:
		String of put response with error response
	"""
	invalidString = "Sorry, that doesn't seem like a valid command. \n Use /ttt help to know more"
	outputString  = invalidString
	return outputString

def createListResponseString():
	"""
	Used to create string response when list command is invoked after
	checking ongoing game condition
	Args:
		None
	Returns:
		String of put response with updated game conditions response
	"""
	global game
	if game.gameOn:
		outputString = createGameListResponse()
	else:
		outputString = createNoGameListResponse()
	return outputString

def createGameListResponse():
	"""
	Used to create string response when list command is invoked after
	checking ongoing game condition
	Args:
		None
	Returns:
		String of put response with updated game conditions response
	"""
	global game
	firstPlayerString = 'First Player : ' + game.firstPlayer +' '+ game.firstPlayerSymbol+' \n'
	secondPlayerString = 'Second Player : '+ game.secondPlayer +' '+ game.secondPlayerSymbol+' \n'
	gameString = game.getBoard()
	nextTurnString = 'Turn: ' + game.nextTurn+ '\n'
	outputString = firstPlayerString + secondPlayerString + gameString + nextTurnString
	return outputString

def createNoGameListResponse():
	"""
	Used to create string response when list command is invoked and no 
	ongoing game exists
	Args:
		None
	Returns:
		String of put response with updated error response
	"""
	noGameString = 'Seems like there isn\'t any ttt game on right now.\n Use /ttt @username to challenge someone'
	outputString = noGameString
	return outputString

def createGameYesResponse():
	"""
	Used to create string response when challenge command is invoked after
	checking ongoing game condition
	Args:
		None
	Returns:
		String of put response with updated game status response
	"""
	gameOnString = 'A ttt game is already on.\n Use /ttt help to know more.'
	outputString = gameOnString
	return outputString

def createInvalidUserResponse():
	"""
	Used to create string response when challenge command is invoked with invalid user
	Args:
		None
	Returns:
		String of put response with error response
	"""
	invalidString = 'Seems like this user is not in this channel'
	outputString = invalidString
	return outputString

def isValidUsername(username, channel_id, user_id):
	"""
	Used to check if challenge user is in slack channel
	Args:
		username: username of challengee 
		channel_id: channel to check user validity 
		user_idL unique ID of challenger
	Returns:
		True if challenge in channel else False
	"""
	response = sc.api_call("users.list")
	for user in response['members']:
		if user['name'] == username:
			return True
	return False


if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 8000)

#Slack Client creation with Token
sc = SlackClient('xoxp-98588410882-98566920132-101647984725-1587c9429306264be388b906421cf154')

#Firebase client creation
firebase = firebase.FirebaseApplication('https://sttt-52a44.firebaseio.com/', None)

#Game Object creation
game = tictactoe()