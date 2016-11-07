from flask import Flask, request 

app = Flask(__name__)

@app.route("/",methods=['POST'])
def game():
	input_json = request.get_json(force=True)
	return str(input_json),200
#    return 'Test',200

if __name__ == "__main__":
    app.run()

