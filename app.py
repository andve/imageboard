from datetime import datetime
from flask import Flask, render_template, abort, request, redirect, url_for
import requests

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

@app.route("/<board_name>", methods=["GET", "POST"])
def board(board_name):
	if board_name not in board_names:
		return abort(404)
	if request.method == "POST":
		timestamp = str(datetime.utcnow())[:19]
		board_list[board_name][0] += 1
		num = board_list[board_name][0]
		try:
			image_res = requests.head(request.form["image"])
		except:
			image = None
		else:
			image = request.form["image"] if "image" in image_res.headers["Content-Type"] else None
		thread = Thread(
			board_name,
			num,
			timestamp,
			request.form["subject"],
			request.form["name"].strip() or "Anonymous",
			request.form["content"],
			image)
		board_list[board_name][1][num] = thread
		return redirect(url_for("thread", board_name=board_name, thread_num=num))
	return render_template("board.html", board_name=board_name, threads=board_list[board_name][1])

@app.route("/<board_name>/<int:thread_num>", methods=["GET", "POST"])
def thread(board_name, thread_num):
	if board_name in board_list and thread_num in board_list[board_name][1]:
		if request.method == "POST":
			timestamp = str(datetime.utcnow())[:19]
			board_list[board_name][0] += 1
			post_num = board_list[board_name][0]
			try:
				image_res = requests.head(request.form["image"])
			except:
				image = None
			else:
				image = request.form["image"] if "image" in image_res.headers["Content-Type"] else None
			post = Post(
				post_num,
				timestamp,
				request.form["name"].strip() or "Anonymous",
				request.form["content"],
				image)
			board_list[board_name][1][thread_num].posts.append(post)
		return render_template("thread.html", thread=board_list[board_name][1][thread_num])
	return abort(404)

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=8000)
