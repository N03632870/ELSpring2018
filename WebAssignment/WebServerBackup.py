from datetime import datetime

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io

from flask import Flask, render_template, send_file, make_response, request
app = Flask(__name__)

import sqlite3

# Retrieve data from database

conn=sqlite3.connect('../code/Database/temperature.db')
curs=conn.cursor()
# Gets the last entry remove 2
def getLastData2():
	for row in curs.execute("SELECT * FROM TempData ORDER BY date_time DESC limit 1"):
		time = str(row[0])
		tempC = row[1]
		tempF = row[2]
	#conn.close()
	return time, tempC, tempF

# gets a range of data
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
##################
def getLastData(fromDate,toDate): 
	curs.execute("SELECT * FROM TempData WHERE date_time BEWEEN '"+fromDate+"' AND '"+toDate+"'")
	data = curs.fetchall()
	date = []
	tempCs = []
	tempFs = []
	for row in reversed(data):
		dates.append(row[0])
		tempCs.append(row[1])
		tempFs.append(row[2])
	return dates, tempCs, tempFs


# sets number of rows
def maxRowsTable():
	for row in curs.execute("select COUNT(tempC) from  TempData"):
		maxNumberRows=row[0]
	return maxNumberRows

# Get sample frequency in minutes
def freqSample():
	times, tempCs, tempFs = getHistData (2)
	fmt = '%m/%d/%y %H:%M:%S %Z'
	tstamp0 = datetime.strptime(times[0], fmt)
	tstamp1 = datetime.strptime(times[1], fmt)
	freq = tstamp1-tstamp0
	freq = int(round(freq.total_seconds()/60))
	return (freq)



# define and intialize global variables
global numSamples
numSamples = maxRowsTable()
if(numSamples > 101):
	numSamples = 100
global fromDate
fromDate = "03/04/18 21:00:00"
global toDate
toDate = "03/04/18 23:30:00"


global freqSamples
freqSamples = freqSample()

global rangeTime
rangeTime = 100


# main route 
@app.route("/")
def index():	
	time, tempC, tempF = getLastData2()
	templateData = {
		'time': time,
		'tempC': tempC,
		'tempF': tempF,
		'freq' : freqSamples,
		'rangeTime'	: rangeTime
	}
	return render_template('index.html', **templateData)




@app.route('/', methods=['POST'])
def my_form_post():
    global numSamples
    global freqSamples
    global rangeTime
    rangeTime = int (request.form['rangeTime'])
    if (rangeTime < freqSamples):
        rangeTime = freqSamples + 1
    numSamples = rangeTime//freqSamples
    numMaxSamples = maxRowsTable()
    if (numSamples > numMaxSamples):
        numSamples = numMaxSamples - 1
    time, tempC, tempF = getLastData2()
    templateData = {
	  	'time'	: time,
      		'tempC'	: tempC,
      		'tempF'	: tempF,
      		'freq'	: freqSamples,
		'rangeTime' : rangeTime
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
   app.run(host='0.0.0.0', port=100, debug=False)
