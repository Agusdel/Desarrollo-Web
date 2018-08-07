from flask import Flask
from flask import render_template
app = Flask(__name__)

userList = ['Agustin', 'Pablo', 'Guillermo']

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user")
def users():
	return render_template("users.html", userList = userList)

@app.route("/user/<user>")
def user(user):
    return render_template("user.html", user = user)

if __name__ == "__main__":	
	app.run(host="0.0.0.0")