import sys
import os
from flask import Flask, render_template, request

app = Flask(__name__)
curr_dir = os.path.dirname(__file__)

sys.path.append(curr_dir + '../src')
from html_parser import HTMLParser

@app.route('/')
def url_input():
    return render_template('url-input.html')

@app.route('/', methods=['POST'])
def url_input_post():
    url = request.form['url']
    return render_template('report.html', notices=HTMLParser(url).waqc())

if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run()
