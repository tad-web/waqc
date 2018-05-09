# waqc : Web Accessibility Quick Check

The Web Accessibility Quick Checker, or WAQC, is a webapp that checks a website for some basic accessibility violations. WAQC provides non-technical output and is accessible to screenreaders. This tool was specifically designed for and with the Carroll Center for the Blind in Newton, MA in the context of the course Technology, Accessibility and Design at Olin College of Engineering in Needham, MA.

## Use the tool

Navigate to [the WAQC web app](http://waqc.herokuapp.com/ "Link to WAQC web app home page") to use the website. Please insert a URL and click Submit to receive a quick check of that website's basic accesibility violations.
While the website currently works on Chrome (version 66), Mozilla Firefox, Internet Explorer 11 and Microsoft Edge, their accessibility still depends on the screenreader involved. We have tested with NVDA, which works well with Internet Explorer and Chrome. We did not have the capability to test with JAWS, but our community partner used JAWS without issue. Also, we collectively use Ubuntu and Windows and have tested on OSX.

For more information about what exactly we check, please see the description on our [url input page](http://waqc.herokuapp.com "web app") on our web app. For more information on our design methods, ideas and motivation, please see the [About page on the web app](http://waqc.herokuapp.com/about "Link to WAQC app about page").

## Set up your environment:

All of these instructions are intended for a Linux development environment.

### pipenv

```bash
$ sudo apt install software-properties-common python-software-properties
$ sudo add-apt-repository ppa:pypa/ppa
$ sudo apt update
$ sudo apt install pipenv
$ pipenv install
$ pipenv shell
```

## Run:

The following command will host a local version of our tool. You can view it by navigating to `localhost:5000` in your browser.

```bash
$ python app/routes.py
```

To run the accessibility checks without using the Flask app, modify `src/main.py` as appropriate and run:

```bash
$ python src/main.py
```

## System description:

We built a [Flask](http://flask.pocoo.org/docs/0.12/ "Flask documentation") app (`app/routes.py`) using [Jinja2](http://jinja.pocoo.org/docs/2.10/ "Jinja documentation") templates and [skeleton](http://getskeleton.com/ "Skeleton CSS") CSS. The back end of the app is an object-oriented accessibility checker (`src/html_parser.py`) written in [Python 3](https://docs.python.org/3/ "Python documentation") and using [Requests](http://docs.python-requests.org/en/master/ "Requests documentation") and [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/ "Beautiful Soup documentation"). The app is set up to work with [postgreSQL](https://www.heroku.com/postgres "PostgreSQL with Heroku documentation") but does not actually use a database at the moment. The app is deployed on [Heroku](https://devcenter.heroku.com/ "Heroku documentation").
