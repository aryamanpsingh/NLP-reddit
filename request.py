import requests, os
from flask import Flask, render_template, request

import pandas as pd

APP_FOLDER = os.path.join('static', 'people_photo')

url = 'http://localhost:4000/api'
app = Flask(__name__)

@app.route('/send', methods=['GET','POST'])
def send():
    if request.method == 'POST':
        term = request.form["term"]
        subreddit = request.form["subreddit"]
        r = requests.post(url,json={'term':term,'sub':subreddit,})
        img = r.json()
        #full_filename = os.path.join('static', img)
        return render_template('result.html', img=img)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run()

