# waqc

## setup

If Ubuntu 17:10:

```bash
$ sudo apt install software-properties-common python-software-properties
$ sudo add-apt-repository ppa:pypa/ppa
$ sudo apt update
$ sudo apt install pipenv
```
Otherwise:

```bash
$ pip install pipenv
```

To start the virtual environment:
```bash
$ pipenv shell
```

To install everything in the pipfile:
```bash
$ pipenv install
```

More information on pipenv [here](https://docs.pipenv.org/ "Pipenv docs").
