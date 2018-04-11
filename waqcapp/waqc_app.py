"""
Put your Flask app code here.
"""

from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_something', methods=['POST'])
def send_something():
    submission = request.form['text']
    print(submission)
    return redirect(url_for('results', words=submission))


@app.route('/results/<words>')
def results(words=None):
    print(words)
    return render_template('results.html', submission=words)

if __name__ == '__main__':
    app.run()
