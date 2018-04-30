# waqc : Web Accessibility Quick Check 

This website was made for Technology, Accessibility and Design course at Olin College of Engineering in Needham, MA. It was specifically designed for and with the Carroll Center for the Blind in Newton, MA. 

## How to use the website
Navigate to [the WAQC web app] (http://waqc.herokuapp.com/ "Link to WAQC web app home page") to use the website. Please insert a URL and click Submit to receive a quick check of that website's basic accesibility violations. 
While the website currently works on Chrome (version 66), Mozilla Firefox, Internet Explorer 11 and Microsoft Edge, their accessibility still depends on the screenreader involved. We have tested with NVDA, which works well with Internet Explorer and Chrome. We did not have the capability to test with JAWS, but our community partner used JAWS without issue. Also, we collectively use Ubuntu and Windows and have tested on a MAC. 
For more information on our design methods, ideas and motivation, please see the [About page on the web app] (http://waqc.herokuapp.com/about "Link to WAQC app about page"). 

## Setup for the program: 

All of these instructions are meant for Ubuntu 16. They are likely supported on other forms of Ubuntu and easily translated into other forms of Linux. They are also similar to the instructions for Windows users, but certain pieces of software, like postgreSQL, are much harder to install on Windows. 

### pipenv

```bash
$ sudo apt install software-properties-common python-software-properties
$ sudo add-apt-repository ppa:pypa/ppa
$ sudo apt update
$ sudo apt install pipenv
```

## Sources

A lot our documentation is borrowed from [here](https://github.com/HALtheWise/baby-harvester/wiki/Local-Gateway-Development "BabyHarvester wiki").

## Limitations 

At the end of the project, we will post our limitations here. 