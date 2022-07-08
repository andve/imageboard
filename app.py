from flask import Flask, render_template, abort

app = Flask(__name__)
board_names = {"tech", "lit", "film"}
board_list = {
	"tech": [0, {}],
	"lit": [0, {}],
	"film": [0, {}]
}

class Post:
	def __init__(self, num, timestamp, name, content, image):
		self.num = num
		self.timestamp = timestamp
		self.name = name
		self.content = content
		self.image = image

class Thread(Post):
	def __init__(self, board, num, timestamp, subject, name, content, image):
		self.board = board
		self.subject = subject
		self.posts = []
		super().__init__(num, timestamp, name, content, image)

@app.route("/")
def home():
	return render_template("home.html")

@app.route("/<board>", methods=["GET", "POST"])
def board(board):
	return board

@app.route("/<board>/<int:thread_num>")
def thread(board, thread_num):
	return str(thread_num)

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=8000)
