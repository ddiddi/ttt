from flask import Flask, request

app = Flask(__name__)

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
	return checkValidParams(text),200
	#print user_name
	#return '| X | 0 | 0 |\n|---+---+---|\n| X | 0 | 0 |\n|---+---+---|\n| X | 0 | 0 |',200


def checkValidParams(text):
	params = text.split(" ")
	return {
		'@username': 1,
		'check':2
	}.get(params[0], "Sorry input command seems invalid")

if __name__ == "__main__":
    app.run()

