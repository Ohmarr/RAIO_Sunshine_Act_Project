import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask import (
    Flask, 
    jsonify, 
    render_template)
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.debug = True

#################################################
# Database Setup
#################################################
# SQL Alchemy ⟷ import module; 
from sqlalchemy import create_engine

# PyMySQL ⟷ Connector
import pymysql
pymysql.install_as_MySQLdb()
# Create Engine & Pass in MySQL Connection; 
from config import dbuser, dbpasswd, dburi, dbport
connectionURI = f"mysql://{dbuser}:{dbpasswd}@{dburi}:{dbport}/sunshinedb"
engine = create_engine(connectionURI)
conn = engine.connect()
# #app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/bellybutton.sqlite"
# #engine = create_engine("mysql://Omar:9461@local:3306/sunshinedb")
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:9461@localhost/sunshinedb"
# db = SQLAlchemy(app)

Base = automap_base() # reflect an existing database into a new model
Base.prepare(engine, reflect=True) # reflect the tables

Orthofix = Base.classes.OrthoFix # orthofix table pointer #failing due to bad automap_base, table has no PK; 

# # –––––––––––––––– **NOTE** –––––––––––––––––––––
# 	# DATABASE: sunshinedb
# 	# TABLE: orthofix
# #################################################
# # Routes
# #################################################

@app.route("/")		          # Default Route
def index():			  # Return ⟶ Rendered Homepage	
	print('success loading homepage')
	return render_template("index.html")

@app.route("/names")              # Visit route ⟶ query `samples_data`
def names():		          # Return ⟶ list(JSON): sample
	#query = ('OrthoFix', connectionURI) # SAME AS RUNNING QUERY ON MySQL WORKBENCH; db.\

	print('query succesful')
	name_list = engine.execute('SELECT Name FROM OrthoFix').fetchall()
	#orthofix_df = pd.read_sql_query('SELECT Name FROM OrthoFix', connectionURI)
	#print([dict(r) for r in temp]) 
	names_json = json.dumps([dict(name) for name in name_list])
	return names_json   

@app.route("/names/<name>")   # Parameter=sample ⟶ Visit route; query `sample_data`
def dr_information(name):              # Return ⟶ (Json of queried data)
	dr_info = engine.execute('SELECT * FROM OrthoFix WHERE Name = "{}"'.format(name)).fetchall()
	#orthofix_df = pd.read_sql_query('SELECT Name FROM OrthoFix', connectionURI)
	#print([dict(r) for r in temp]) 
	doctor_json = json.dumps([dict(name) for name in dr_info])
	return  doctor_json

if __name__ == "__main__":
    app.run()
