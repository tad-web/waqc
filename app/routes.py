import os, sys
curr_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(curr_dir + '/../src')


from flask import Flask, render_template, request

from html_parser import HTMLParser


app = Flask(__name__)

@app.route('/')
def url_input():
  return render_template('url-input.html')

@app.route('/', methods=['POST'])
def url_input_post():
  url = request.form['url to check']
  return render_template('report.html', notices=HTMLParser(url).waqc())

if __name__ == '__main__':
  app.config['DEBUG'] = True
  app.run()
