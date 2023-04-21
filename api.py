from flask import Flask, request, render_template, redirect, url_for
import redis
from datetime import datetime
import requests
import mpld3
from StockDataVisualizer import StockDataVisualizer


app = Flask(__name__)
app.secret_key = 'my_secret_key'
cache = redis.Redis(host='localhost', port=6379)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    symbol = request.form.get('symbol')
    chart = request.form.get('chart')
    timeseries = request.form.get('timeseries')
    startdate = datetime.strptime(request.form.get('startdate'), '%Y-%m-%d')
    enddate = datetime.strptime(request.form.get('enddate'), '%Y-%m-%d')
    plot = StockDataVisualizer(symbol, chart, timeseries, startdate, enddate)
    fig = plot.graphData()
    cache.set('fig', fig)
    return redirect(url_for('graph'))

@app.route('/graph')
def graph():
    fig = cache.get('fig')
    mpld3.fig_to_html(fig)
    mpld3.show()
    url = f'http://localhost:8888'
    response = requests.get(url)
    return response.content
    
    
    

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    