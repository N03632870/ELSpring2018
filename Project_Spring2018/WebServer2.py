from flask import *
from functools import wraps
import sqlite3
#import matplotlib.pyplot as plt

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

DATABASE = '../code/Database/dth22.db'

app = Flask(__name__)
app.config.from_object(__name__)

app.secret_key = 'my precious'

def connect_db():
   return sqlite3.connect(app.config['DATABASE'])

def getHistData()
   
@app.route('/')
def home():
   return render_template('home.html')

@app.route('/graph', methods=['POST])
def graph():
     
   return render_template('graph.html')

def login_required(test):
   @wraps(test)
   def wrap(*args, **kwargs):
      if 'logged_in' in session:
         return test(*args, **kwargs)
      else:
         flash('You need to login first.')
         return redirect(url_for('log'))
   return wrap

@app.route('/data', methods=['GET','POST'])
#@login_required
#####

@app.route('/plot/temp')
def plot_temp():
	times, temps, hums = getHistData(numSamples)
	ys = temps
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Temperature [�C]")
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

@app.route('/plot/hum')
def plot_hum():
	times, temps, hums = getHistData(numSamples)
	ys = hums
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Humidity [%]")
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




######     
def data():	
      
      g.db = connect_db()
      cur = g.db.execute('select * from data01 where date BETWEEN "'+str(fromTime)+'" AND "'+str(toTime)+'" ORDER BY Date DESC limit '+str(num))
      data = [dict(Date=row[0], Temp=row[1], Humidity=row[2]) for row in cur.fetchall()]
      g.db.close()
      return render_template('data.html', data=data)


@app.route('/logout')
def logout():
   session.pop('logged_in',None)
   flash("You are logged out")
   return redirect (url_for('log'))

@app.route('/log', methods=['GET', 'POST'])
def log():
   error = None 
   
   if request.method == 'POST':
      #if request.form['username'] != 'admin' or request.form['password'] != 'admin':
         #error = 'Invalid Credentials. Please try again.'
      #else:
         global num
         global fromDate
         global toDate
         global fromTime
         global toTime
         num = request.form['number']
         #fromDate = request.form['fromDate']
         #toDate = request.form['toDate']
         fromTime = request.form['fromTime']
         toTime = request.form['toTime']
         
         return redirect(url_for('data'))
   return render_template('log.html', error=error)
global num
num =5
global fromDate
fromDate = "03/01/2018"
global toDate
toDate = "06/05/2018"

if __name__ == "__main__":
   app.run(host='0.0.0.0',threaded=True, port=900, debug=True)


