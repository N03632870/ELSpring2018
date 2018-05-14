from flask import Flask, render_template, request
import sqlite3
import json

DATABASE = '../code/Database/dth22.db'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/data.json")
def data():
   connection = sqlite3.connect(app.config['DATABASE'])
   cursor = connection.cursor()
   cursor.execute(SELECT * from data01)
   results = cursor.fetchall()
   print results
   return json.dumps(results)

@app.route("/graph")
def graph():
   return render_template('graph.html')

if __name__ == "__main__":
   app.run(host='0.0.0.0', threaded=True, port=100, debug=True)
