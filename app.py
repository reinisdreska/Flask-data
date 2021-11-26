#Lai palaistu    py -m flask run
from flask import Flask, render_template
import mysql.connector
import config

app = Flask(__name__)

mydb = mysql.connector.connect(
    host = config.host,
    user = config.user, 
    password = config.password,
    database = config.db
)

mycursor = mydb.cursor()

mycursor.execute("USE reinis_test")

@app.route("/")
def tables():
    mycursor.execute("SHOW TABLES")
    for tables in mycursor:
        continue
    tables_string = "".join(tables)
    
    return render_template("tables.html", title="Tables", tables=tables_string)

@app.route("/data")
def data():
    mycursor.execute("SELECT  * FROM app_errors LIMIT 10;")
    data_tuples = mycursor.fetchall()
    
    return render_template("data.html", title="Data", data=data_tuples)

@app.route("/crate")
def crate():
    return render_template("crate.html", title="Crate Data")