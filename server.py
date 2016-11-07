from flask import Flask, request

app = Flask(__name__)

@app.route("/",methods=['POST','GET'])
def game():
    return 'Test',200

if __name__ == "__main__":
    app.run()

