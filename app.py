from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
	return "home"

@app.route("/<board>")
def board(board):
	return board

@app.route("/<board>/<int:thread_num>")
def thread(board, thread_num):
	return str(thread_num)

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=8000)
