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
        table_raw = request.form
        table_dict = table_raw.to_dict(flat=True)
        table_string = str(table_dict)
        table = table_string.replace("Table", "").replace("{", "").replace("}", "").replace(":", "").replace("'", "")
        print(table)
        mycursor.execute("SELECT  * FROM "+ table)
        data_tuples = mycursor.fetchall()
        field_names = [i[0] for i in mycursor.description]
        return render_template("data.html", title="Data", data = data_tuples, field_names = field_names)

@app.route("/crate_table_variable")
def crate_table_variable():
    return render_template("crate_table_variable.html", title="How mmany variables")

@app.route("/crate_table", methods = ['POST'])
def crate_table():
    if request.method == 'POST':
        variable_raw = request.form
        variable_dict = variable_raw.to_dict(flat=True)
        variable_string = str(variable_dict)
        variable = variable_string.replace("Variables", "").replace("{", "").replace("}", "").replace(":", "").replace("'", "")
        variable_int = int(variable)
        return render_template("crate_table.html", title = "Crate Table", variable = variable_int)

@app.route("/crate_table_end", methods = ['POST'])
def crate_table_end():
    if request.method == 'POST':
        table_raw = request.form
        table_dict = table_raw.to_dict(flat=True)
        table_string = str(table_dict)
        table = table_string.replace("Table", "").replace("{", "").replace("}", "").replace(":", "").replace("'", "").replace(",", "")
        length_table = len(table_dict) - 1
        for i in range(length_table):
            table = table.replace("variable_"+ str(i),"")
        table_arr = table.split()
        length_table_string = len(table_arr) - 1
        create_table_string = "CREATE TABLE "+ table_arr[0] +" ( "
        for i in range(length_table_string):
            create_table_string = create_table_string + table_arr[i+1] + " VARCHAR(100), "
        create_table_string = create_table_string [:-2]+ ")"
        mycursor.execute(create_table_string)
        return render_template("crate.html", title="Crate")

@app.route("/crate_row")
def crate_row():
    return render_template("crate_row.html", title="Crate Row")

@app.route("/crate_row_table", methods = ['POST'])
def crate_row_table():
    if request.method == 'POST':
        table_raw = request.form
        table_dict = table_raw.to_dict(flat=True)
        table_string = str(table_dict)
        table = table_string.replace("Table", "").replace("{", "").replace("}", "").replace(":", "").replace("'", "")
        mycursor.execute("SELECT  * FROM "+ table)
        field_names = [i[0] for i in mycursor.description]
        return render_template("crate_row_table.html", title="Crate Row", field_names = field_names)

# @app.route("/crate_row_end", methods = ['POST'])
# def crate_row_end():
#     if request.method == 'POST':
#         table_raw = request.form
#         table_dict = table_raw.to_dict(flat=True)
#         table_string = str(table_dict)
#         table = table_string.replace("Table", "").replace("variable_1", "").replace("variable_2", "").replace("variable_3", "").replace("variable_4", "").replace("variable_5", "").replace("{", "").replace("}", "").replace(":", "").replace("'", "").replace(",", "")
#         table_arr = table.split()
#         print(table_arr)
#         mycursor.execute("CREATE TABLE "+ table_arr[0] +" ( "+ table_arr[1] + " VARCHAR(100), "+ table_arr[2] + " VARCHAR(100), "+ table_arr[3] + " VARCHAR(100), "+ table_arr[4] + " VARCHAR(100), "+ table_arr[5] + " VARCHAR(100))")
#         return render_template("crate.html", title="Crate ")