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
def dr_information(name):              # Return ⟶ (Json of queried data) `otu_ids`, `otu_labels`& `sample_values`d
 # sample_columns = ['otu_ids', 'sample_values', 'otu_labels']
 # samples_df_all = pd.DataFrame(columns=sample_columns).fillna(0)
	dr_info = engine.execute('SELECT * FROM OrthoFix WHERE Name = "{}"'.format(name)).fetchall()
	#orthofix_df = pd.read_sql_query('SELECT Name FROM OrthoFix', connectionURI)
	#print([dict(r) for r in temp]) 
	doctor_json = json.dumps([dict(name) for name in dr_info])
	return  doctor_json

	# query = db.\
	# 	session.\
	# 	query(sample_data_table_ref).\
	# 	statement

	# samples_df = pd.read_sql_query(query, db.session.bind)
	# # Filter samples w/ values > 1
	# samples_df_filtered = samples_df.loc[samples_df[sample] > 1, ["otu_id", "otu_label", sample]] #only care for sample values that are present
	# samples_df_filtered = samples_df_filtered.sort_values(by=[sample], ascending=False)           #sort <sample> column ↓
	# samples_df_filtered = samples_df_filtered[0:10][:]					      #splice 1st 10 rows; 

	# sample_data = { # (Json of queried data) `otu_ids`, `otu_labels`& `sample_values`
	# 	"otu_ids": samples_df_filtered.otu_id.values.tolist(),
	# 	"sample_values": samples_df_filtered[sample].values.tolist(),
	# 	"otu_labels": samples_df_filtered.otu_label.tolist(),
	# 	}
	# return jsonify(sample_data)

if __name__ == "__main__":
    app.run()
