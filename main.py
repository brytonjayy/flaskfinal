from flask import Flask, render_template, request, url_for
from searchWTF import AskForTitle
app = Flask(__name__)
app. secret_key = b'(YTPffrgrgr)'
app.config.form_object(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/aboutme")
def aboutme():
    