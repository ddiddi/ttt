from flask import Flask, request
import json
import pymongo

SEED_DATA = [
    {
        'decade': '1970s',
        'artist': 'Debby Boone',
        'song': 'You Light Up My Life',
        'weeksAtOne': 10
    },
    {
        'decade': '1980s',
        'artist': 'Olivia Newton-John',
        'song': 'Physical',
        'weeksAtOne': 10
    },
    {
        'decade': '1990s',
        'artist': 'Mariah Carey',
        'song': 'One Sweet Day',
        'weeksAtOne': 16
    }
]

MONGODB_URI = 'mongodb://heroku_k89bf523:c2e67sq8bm6cgs8qdpslhbjmrv@ds147267.mlab.com:47267/heroku_k89bf523'

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

	def peekBoardValue(self, position):
		idx = self.getBoardIndex(position) 
		if idx != -1:
			return self.boardValues[idx]
		return -1

	def changeBoardValue(self, position, newValue):
		i = self.getBoardIndex(position)
		self.changeNextTurn()
		if i != -1:
			self.boardValues[i] = newValue
			return 0
		return -1

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
		print(self.boardValues)
		print(self.boardValues[0])
		print(self.boardValues[2])
		topLine = 'a '+self.boardValues[0]+' '+self.boardValues[1]+' '+self.boardValues[2]+'\n'
		print(topLine)
		middleLine = 'b '+self.boardValues[3]+' '+self.boardValues[4]+' '+self.boardValues[5]+'\n'
		bottomLine = 'c '+self.boardValues[6]+' '+self.boardValues[7]+' '+self.boardValues[8]+'\n'
		output = header+topLine+middleLine+bottomLine
		print(output) 
		return output

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

	def changeNextTurn(self):
		if self.nextTurn == self.firstPlayer:
			self.nextTurn = self.secondPlayer
		self.nextTurn == self.firstPlayer


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
	output = str(executeParams(text,user_name))
	return output,200
	#print user_name
	#return '| X | 0 | 0 |\n|---+---+---|\n| X | 0 | 0 |\n|---+---+---|\n| X | 0 | 0 |',200



def executeParams(text,user_name):
	"""query = {'song': 'One Sweet Day'}

	songs.update(query, {'$set': {'artist': 'Mariah Carey ft. Boyz II Men'}})
	cursor = songs.find({'weeksAtOne': {'$gte': 10}}).sort('decade', 1)

	for doc in cursor:
		print ('In the %s, %s by %s topped the charts for %d straight weeks.' % (doc['decade'], doc['song'], doc['artist'], doc['weeksAtOne']))
	"""
	global game 	
	
	"""print("ASDDDDDDDDD")
	board_json = [ { 'a1':game.peekBoardValue('a1'), 'a2':game.peekBoardValue('a2'), 'a3':game.peekBoardValue('a3'), }]
	game_json = json.dumps(board_json)
	print(SEED_DATA)
	print(game_json)
	gamedb.insert(board_json)

	cursor = gamedb.find_one()
	print("ASDDDDDDDDDwsss")
	print(cursor)
	"""
	db.drop_collection('gamedb')
	client.close()



	params = str(text).split(" ")
	commandValue = ''
	subcommand = params[0]
	if len(params)>1:
		commandValue = params[1]
	
	if subcommand[0] == '@' and isValidUsername(subcommand[1:]) and commandValue == '':
		if game.getGameStatus():
			return "A ttt game is already on.\n Use /ttt help to know more."
		else:
			if isValidUsername(subcommand[1:]):
				game = tictactoe(user_name, subcommand[1:])
			else:
				return "Seems like this user is not in this channel"
	
	elif subcommand == 'ls' and commandValue == '':
		if game.getGameStatus():
			op1 = 'First Player : ' + game.getFirstPlayer() +'\n'
			op2 = 'Second Player: ' + game.getSecondPlayer()+'\n'
			nextTurn = 'Turn: ' + game.getNextTurn()
			return op1+op2+game.currentBoardString()+nextTurn
		else:
			return "Seems like there isn't any ttt game on right now"
			
	elif subcommand == 'put':
		m = game.changeBoardValue(commandValue,game.getFirstPlayerSymbol())
		op1 = 'First Player : ' + game.getFirstPlayer() +'\n'
		op2 = 'Second Player: ' + game.getSecondPlayer()+'\n'
		nextTurn = 'Turn: ' + game.getNextTurn()
		return op1+op2+game.currentBoardString()+nextTurn
	
	elif subcommand == 'help':
		return ("/ttt ls: To see an ongoing game\n /ttt @<username>: To challenge someone in the channel \n/ttt put <row alphabet><column number>: To put a mark at the position \n/ttt help: To see this menu again")
	else:
		return "Sorry, that doesn't seem like a valid command. \n Use /ttt help to know more"

	return "Never Executes"


def isValidUsername(username):
	return True

if __name__ == "__main__":
    app.run()


game = tictactoe(None, None, False)

client = pymongo.MongoClient(MONGODB_URI)
db = client.get_default_database()
gamedb = db['gamedb']
