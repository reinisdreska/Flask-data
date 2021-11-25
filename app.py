#Lai palaistu    py -m flask run
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", title="Index")

@app.route("/data")
def data():
    return render_template("data.html", title="Data")

@app.route("/crate")
def crate():
    return render_template("crate.html", title="Crate Data")