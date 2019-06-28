# Import libraries
import marshal,types,datetime,time,requests,json
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify
import os

from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
sia = SIA()
def days(num):
    return int(num*86400)
now = datetime.datetime.now()

year_graph_file = open('tmp/year_graph.txt', 'rb')
year_graph_file = marshal.loads(year_graph_file.read())
year_graph = types.FunctionType(year_graph_file, globals(), 'year_graph');

getyear_file = open('tmp/get_year.txt', 'rb')
getyear_file = marshal.loads(getyear_file.read())
getYear = types.FunctionType(getyear_file, globals(), 'getYear');

get_polscore_file = open('tmp/get_polscore.txt', 'rb')
get_polscore_file = marshal.loads(get_polscore_file.read())
get_polscore = types.FunctionType(get_polscore_file, globals(), 'get_polscore');

getmonthly_file = open('tmp/get_monthly.txt', 'rb')
getmonthly_file = marshal.loads(getmonthly_file.read())
getmonthly = types.FunctionType(getmonthly_file, globals(), 'getmonthly');

get_file = open('tmp/get.txt', 'rb')
get_file = marshal.loads(get_file.read())
get = types.FunctionType(get_file, globals(), 'get');

getPushshiftData_file = open('tmp/get_pushshift.txt', 'rb')
getPushshiftData_file = marshal.loads(getPushshiftData_file.read())
getPushshiftData = types.FunctionType(getPushshiftData_file, globals(), 'getPushshiftData');

collectSubData_file = open('tmp/collectSubData.txt', 'rb')
collectSubData_file = marshal.loads(collectSubData_file.read())
collectSubData = types.FunctionType(collectSubData_file, globals(), 'collectSubData');

get_utc_file = open('tmp/get_utc.txt', 'rb')
get_utc_file = marshal.loads(get_utc_file.read())
get_utc = types.FunctionType(get_utc_file, globals(), 'get_utc');


app = Flask(__name__)



@app.route('/api',methods=['POST'])
def predict():
    # Get the data from the POST request.
    data = request.get_json(force=True)
    
    # Take the first value of prediction
    img = year_graph(data['term'],data['sub'])
    return jsonify(img)
if __name__ == '__main__':
    app.run(port=4000, debug=True)