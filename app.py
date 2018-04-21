"""
Put your Flask app code here.
"""

from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
import os

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])

# DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Handles deprecation warning
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
db = SQLAlchemy(app)
migrate = Migrate(app,db)

from models import Result

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
    app.config['DEBUG'] = True
    app.run()
