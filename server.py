from flask import Flask, request 

app = Flask(__name__)

@app.route("/",methods=['POST'])
def game():
	return request.get_json(force=True)
#    return 'Test',200

if __name__ == "__main__":
    app.run()

