import requests

url='https://docs.python.org/2/library/csv.html#examples'
filename = 'grabbedhtml.html'

# in case you need a session
# cd = { 'sessionid': '123..'}

#with a session
# r = requests.get(url, cookies=cd)
# or without a session:
r = requests.get(url)
r.content

with open(filename, 'w') as file:
    file.write(str(r.content))
file.close()
