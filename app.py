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
    tables_arr = []
    for tables in mycursor:
        tables_arr += tables
    separator = ", "
    tables_string = separator.join(tables_arr)

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
        mycursor.execute("SELECT  * FROM "+ table)
        data_tuples = mycursor.fetchall()
        
        return render_template("data.html", title="Data", data=data_tuples)

@app.route("/crate_table")
def crate_table():
    return render_template("crate_table.html", title="Crate Table ")

@app.route("/crate", methods = ['POST'])
def crate():
    if request.method == 'POST':
        remove = ["{", "}", ":", "'"]
        table_raw = request.form
        table_dict = table_raw.to_dict(flat=True)
        table_string = str(table_dict)
        table = table_string.replace("Table", "").replace("variable_1", "").replace("variable_2", "").replace("variable_3", "").replace("variable_4", "").replace("variable_5", "").replace("{", "").replace("}", "").replace(":", "").replace("'", "").replace(",", "")
        table_arr = table.split()
        print(table_arr)
        mycursor.execute("CREATE TABLE "+ table_arr[0] +" ( "+ table_arr[1] + " VARCHAR(100), "+ table_arr[2] + " VARCHAR(100), "+ table_arr[3] + " VARCHAR(100), "+ table_arr[4] + " VARCHAR(100), "+ table_arr[5] + " VARCHAR(100))")
        return render_template("crate.html", title="Crate ")