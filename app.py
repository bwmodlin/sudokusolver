from flask import Flask
from flask import render_template

app = Flask(__name__)

board = [[0, 6, 0, 0, 0, 0, 0, 1, 0],
        [0, 5, 0, 0, 3, 0, 0, 7, 0],
        [0, 2, 0, 5, 6, 0, 4, 0, 0],
        [0, 0, 8, 0, 4, 0, 0, 9, 0],
        [0, 0, 3, 0, 0, 9, 1, 0, 0],
        [0, 0, 0, 1, 0, 6, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 3, 0, 0, 9, 0, 0, 0, 2],
        [0, 0, 7, 0, 5, 0, 0, 4, 0]]

@app.route('/')
def hello_world():  # put application's code here

    return render_template('board.html', list=board)

@app.route("/test")
def test():
    return "test page"


if __name__ == '__main__':
    app.run()
