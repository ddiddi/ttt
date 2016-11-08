import json
from firebase import firebase

class tictactoe:
	'Base class from Tic Tac Toe Game'

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

firebase = firebase.FirebaseApplication('https://sttt-52a44.firebaseio.com/', None)
game = tictactoe()
print("Finish")
a = firebase.get('/game',None)
print(a['master'])