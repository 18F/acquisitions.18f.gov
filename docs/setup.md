# Setup and Local Development

## Installation

First, get a local copy of the project:

```
git clone https://github.com/18f/acquisitions.18f.gov.git
cd acquisitions.18f.gov
```

This is a Django project, built using Python 3. From here, you can proceed to install and execute the project directly on to your computer, or you can skip down to the [Docker instructions](#docker) to get everything into Docker containers.

We recommend using [`pyenv`](https://github.com/yyuu/pyenv) to manage your Python versions. Additionally, some form of [`virtualenv`](https://github.com/pypa/virtualenv) is recommended, either as-is or using [`virtualenvwrapper`](http://virtualenvwrapper.readthedocs.io/en/latest/). (With `pyenv`, [`pyenv-virtualwrapper`](https://github.com/yyuu/pyenv-virtualenvwrapper) can help with this.) With Python installed, you can:

```
pyenv install 3.5.1
python --version          # Should display Python 3.5.1
pyenv virtualenvwrapper   # not necessary if it's already loaded in your .bash_profile or .zshrc
mkvirtualenv acquisitions
pip install -r requirements.txt requirements-dev.txt
```

The project runs a PostgreSQL database. Set up the database and create the user groups:

```
createdb acquisitions
./manage.py migrate
./manage.py init_groups
```

Optionally, populate the database with some fake data:

```
./manage.py create_team
./manage.py create_projects
./manage.py create_buys --add
./manage.py create_content
```

Because of the authentication flow, a superuser should be created without a
password:

```
./manage.py createsuperuser --noinput --username foo --email foo@localhost
```

You can use the superuser's email to log in to the system.

Finally, run the application:

```
./manage.py runserver
```

## Docker

To get started, you will need to have [Docker installed](https://www.docker.com/products/overview).
Once you have Docker installed, you can install all of the project dependencies,
setup a database, and start the project website by running the following:

```shell
docker-compose up -d
```

The project should now be available at http://localhost:8000.

The `-d` flag causes Docker to "detach" and run the project in the background
once it's running.  This `docker-compose` step takes care of installing
everything that the project needs and setting up the database structure, but
it doesn't actually put any data into the database or users, so there's not
much to view and there's no way to login.

To create a superuser account, run the following:

```shell
docker-compose exec web ./manage.py createsuperuser --noinput --username foo --email foo@localhost
```

You can change the username and email to whatever you want, but note that
whatever email you use is what you will use to log into the website.

You can also load some dummy data into the project using the following commands:

```shell
docker-compose exec web ./bin/seed-db.sh
```
