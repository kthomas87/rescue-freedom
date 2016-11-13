import cPickle as pickle
import pandas as pd
from flask import Flask, request, render_template
app = Flask(__name__)


# home page
@app.route('/')
def index():
    return render_template('index.html')

app.route('/map')
def map():
    return render_template('world.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8181, debug=True)
