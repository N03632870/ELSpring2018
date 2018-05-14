from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io


from flask import Flask, render_template, send_file, make_response, request
app = Flask(__name__)

import sqlite3

# Retrieve data from database

conn=sqlite3.connect('../code/Database/temperature.db')
curs=conn.cursor()
def getLastData():
	for row in curs.execute("SELECT * FROM TempData ORDER BY date_time DESC limit 1"):
		time = str(row[0])
		tempC = row[1]
		tempF = row[2]
	#conn.close()
	return time, tempC, tempF
def getHistData (numSamples):
	curs.execute("SELECT * FROM TempData ORDER BY date_time DESC LIMIT "+str(numSamples))
	data = curs.fetchall()
	dates = []
	tempCs = []
	tempFs = []
	for row in reversed(data):
		dates.append(row[0])
		tempCs.append(row[1])
		tempFs.append(row[2])
	return dates, tempCs, tempFs

# sets number of rows
def maxRowsTable():
	for row in curs.execute("select COUNT(temp) from  TempData"):
		maxNumberRows=row[0]
	return maxNumberRows

# define and intialize global variables
global numSamples
numSamples = maxRowsTable()
if(numSamples > 101):
	numSamples = 100
# main route 
@app.route("/")
def index():	
	time, tempC, tempF = getData()
	templateData = {
		'time': time,
		'tempC': tempC,
		'tempF': tempF,
		'numSamples'	: numSamples
	}
	return render_template('index.html', **templateData)




@app.route('/', methods=['POST'])
def my_form_post():
    global numSamples
    numSamples = int (request.form['numSamples'])
    numMaxSamples = maxRowsTable()
    if (numSamples > numMaxSamples):
        numSamples = (numMaxSamples-1)
    time, tempC, tempF = getLastData()
    templateData = {
	  	'time'	: time,
      		'tempC'	: tempC,
      		'tempF'	: tempF,
      		'numSamples'	: numSamples
	}
    return render_template('index.html', **templateData)

@app.route('/plot/tempC')
def plot_tempC():
	times, tempCs, tempFs = getHistData(numSamples)
	ys = tempCs
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Temperature [C]")
	axis.set_xlabel("Samples")
	axis.grid(True)
	xs = range(numSamples)
	axis.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

@app.route('/plot/tempF')
def plot_tempF():
	times, tempCs, tempFs = getHistData(numSamples)
	ys = tempFs
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Temperature [F]")
	axis.set_xlabel("Samples")
	axis.grid(True)
	xs = range(numSamples)
	axis.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=81, debug=False)
