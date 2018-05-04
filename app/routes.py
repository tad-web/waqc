import os, sys
curr_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(curr_dir + '/../src')


from flask import Flask, render_template, request, session

from html_parser import HTMLParser


app = Flask(__name__)
app.secret_key = b'_#y2L"F4a%hQ8\n\xec]/'  # can be on git because we aren't storing private things

@app.route('/')
def url_input():
  return render_template('url-input.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/subpage-selection', methods=['POST'])
def url_input_post():
  session['urls'] = []
  url = request.form['url to check']
  if not url.startswith(('http://', 'https://')):
    url = 'http://' + url
  session['urls'].append(url)
  navbar_links = HTMLParser([url]).get_navbar_links(url)
  if navbar_links:
    return render_template('subpage-selection.html', links=navbar_links)
  else:
    url_notices = HTMLParser(session['urls']).run()
    return render_template('report.html', url_notices=url_notices )

@app.route('/report-output', methods=['POST'])
def subpage_selection_post():
  url = request.form['subpage to check']
  session['urls'].append(url)
  url_notices = HTMLParser(session['urls']).run()
  return render_template('report.html', url_notices=url_notices )
  # try:
  #   url_notices = HTMLParser(url).run()
  #   return render_template('report.html', url_notices=url_notices )
  # except:
  #   return render_template('url-error.html', url=url)

if __name__ == '__main__':
  app.config['DEBUG'] = True
  app.run()
