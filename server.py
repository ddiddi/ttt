from flask import Flask, request

app = Flask(__name__)

class tictactoe:
	'Base class from Tic Tac Toe Game'

	boardValues = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
	gameOn = False
	firstPlayerSymbol = 'X'
	secondPlayerSymbol = 'O'

	def __init__(self, firstPlayer=None, secondPlayer=None,gameStatus=True):
		self.firstPlayer = firstPlayer
		self.secondPlayer = secondPlayer
		self.gameOn = gameStatus

	def peekBoardValue(self, position):
		idx = getBoardIndex(position) 
		if idx != -1:
			return self.boardValues[idx]
		return -1

	def changeBoardValue(self, position, newValue):
		idx = getBoardIndex(position)
		if idx != -1:
			self.boardValues[idx] = newValue
			return 0
		return -1

	def getBoardIndex(position):
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
		header = '    1   2   3  \n'
		topLine = 'a | '+self.boardValues[0]+' | '+self.boardValues[1]+' | '+self.boardValues[2]+' |\n'
		breakLine = ' |---+---+---|\n'
		middleLine = 'b | '+self.boardValues[3]+' | '+self.boardValues[4]+' | '+self.boardValues[5]+' |\n'
		bottomLine = 'c | '+self.boardValues[6]+' | '+self.boardValues[7]+' | '+self.boardValues[8]+' |\n'
		return header+topLine+breakLine+middleLine+breakLine+bottomLine

	def getFirstPlayer(self):
		return self.firstPlayer

	def getSecondPlayer(self):
		return self.SecondPlayer

	def changeFirstPlayer(self, newValue):
		self.firstPlayer = newValue

	def changeSecondPlayer(self, newValue):
		self.secondPlayer = newValue

	def getFirstPlayerSymbol(self):
		return self.firstPlayerSymbol

	def getSecondPlayerSymbol(self):
		return self.SecondPlayerSymbol

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
		else if ((self.boardValues[0] == self.boardValues[1] == self.boardValues[2] == self.secondPlayerSymbol)
			or (self.boardValues[3] == self.boardValues[4] == self.boardValues[5] == self.secondPlayerSymbol)
			or (self.boardValues[6] == self.boardValues[7] == self.boardValues[8] == self.secondPlayerSymbol)
			or (self.boardValues[0] == self.boardValues[3] == self.boardValues[6] == self.secondPlayerSymbol)
			or (self.boardValues[1] == self.boardValues[4] == self.boardValues[7] == self.secondPlayerSymbol)
			or (self.boardValues[2] == self.boardValues[5] == self.boardValues[8] == self.secondPlayerSymbol)
			or (self.boardValues[0] == self.boardValues[4] == self.boardValues[8] == self.secondPlayerSymbol)
			or (self.boardValues[2] == self.boardValues[4] == self.boardValues[6] == self.secondPlayerSymbol)):
			return getSecondPlayer()
		return -1

@app.route("/",methods=['POST','GET'])
def game():
	print("****Logging*****In main function")
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
	return executeParams(request.form()),200
	#print user_name
	#return '| X | 0 | 0 |\n|---+---+---|\n| X | 0 | 0 |\n|---+---+---|\n| X | 0 | 0 |',200



def executeParams(input_command_form):
	text = input_command_form['text']
	params = text.split(" ")
	subcommand = params[0]
	commandValue = params[1]

	if subcommand[0] == '@' and isValidUsername(subcommand[1:]):
		game = tictactoe(input_command_form['user_name'], subcommand[1:])

	return game.currentBoardString()


def isValidUsername(username):
	return True

if __name__ == "__main__":
    app.run()
    game = tictactoe(None, None. False)

