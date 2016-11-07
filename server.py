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
	print user_name


	return 'Test',200

if __name__ == "__main__":
    app.run()

