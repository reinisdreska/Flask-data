#Lai palaistu    py -m flask run
from flask import Flask, render_template, request
import mysql.connector
import config
from werkzeug.datastructures import ImmutableMultiDict

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

@app.route("/which_table")
def which_table():
    return render_template("which_table.html", title="Which table")

@app.route("/data", methods = ['POST'])
def data():
    if request.method == 'POST':
        remove = ["{", "}", ":", "'"]
        table_raw = request.form
        table_dict = table_raw.to_dict(flat=True)
        table_string = str(table_dict)
        table = table_string.replace("Table", "").replace("{", "").replace("}", "").replace(":", "").replace("'", "")
        print(table)
        mycursor.execute("SELECT  * FROM "+ table +" LIMIT 10;")
        data_tuples = mycursor.fetchall()
        
        return render_template("data.html", title="Data", data=data_tuples)

@app.route("/crate")
def crate():
    return render_template("crate.html", title="Crate Data")