# waqc

## Setup

### pipenv

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

### postgreSQL

Note: only tested on Ubuntu 16.04

#### Install

For development, a local postgresql db is recommended.

Install postgres:

```bash
$ sudo apt install postgresql
```

On Ubuntu, this installs authorized to a dedicated unix account 'postgres'.

#### Config

To create a separate account with a password:

```bash
$ sudo -i -u postgres
$ createuser <username>
$ createdb <dbname>
$ psql
# ALTER USER <username> WITH ENCRYPTED PASSWORD '<password>';
# GRANT ALL PRIVILEGES ON DATABASE <dbname> TO <username> ;
# \q
```

#### Use

To connect to postgreSQL from the command line:
```bash
$ sudo -u <username> psql <dbname>

```

### Environment variables

Copy `env.template` to `env.local` edit the variables inside to match your configuration. To set the environment, simply `$ source env.local`.

### Database migrations

Note: only tested on Ubuntu 16.04

To change db schema, modify `models.py` then commit migration:

```bash
$ pipenv run flask db migrate -m "message"
```

Apply with:
```bash
$ pipenv run flask db upgrade
```

Note: if the commit results in `alembic.util.exc.CommandError: Target database is not up to date.`, you may need to run this to mark the current database as up to date.
```bash
$ pipenv run flask db stamp head
```

## Run

```bash
$ python src/main.py
```


## Sources, I guess?

I'm borrowing a lot of this documentation from [here](https://github.com/HALtheWise/baby-harvester/wiki/Local-Gateway-Development "BabyHarvester wiki").
