[![Build Status](https://travis-ci.org/18F/acquisitions.18f.gov.svg?branch=develop)](https://travis-ci.org/18F/acquisitions.18f.gov)
[![Code Climate](https://codeclimate.com/github/18F/acquisitions.18f.gov/badges/gpa.svg)](https://codeclimate.com/github/18F/acquisitions.18f.gov)
[![Test Coverage](https://codeclimate.com/github/18F/acquisitions.18f.gov/badges/coverage.svg)](https://codeclimate.com/github/18F/acquisitions.18f.gov/coverage)

# acquisitions.18f.gov

This is the homepage for the TTS Office of Acquisitions. Its goal is to be a
public-facing site for the office's efforts, as well as an internal site for
coordinating and tracking work.

## Installation

First, get a local copy of the project:

```
git clone https://github.com/18f/acquisitions.18f.gov.git
cd acquisitions.18f.gov
```

This is a Django project, built using Python 3. We recommend using [`pyenv`](https://github.com/yyuu/pyenv) to manage your Python versions. Additionally, some form of [`virtualenv`](https://github.com/pypa/virtualenv) is recommended, either as-is or using [`virtualenvwrapper`](http://virtualenvwrapper.readthedocs.io/en/latest/). (With `pyenv`, [`pyenv-virtualwrapper`](https://github.com/yyuu/pyenv-virtualenvwrapper) can help with this.) With that, you can:

```
pyenv install 3.5.1
python --version          # Should display Python 3.5.1
pyenv virtualenvwrapper   # not necessary if it's already loaded in your .bash_profile or .zshrc
mkvirtualenv acquisitions
pip install -r requirements.txt
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
```

Because of the authentication flow, a superuser should be created without a
password:

```
./manage.py createsuperuser --noinput --username foo --email foo@localhost
```

And then run the application:

```
./manage.py runserver
```

## Deployment

See [the deployment docs](./docs/deploy.md) for information on deploying the application.

## Elements

### Team API

This app includes information about the people on the team and provides an API
for retrieving that information. In the interest of API-first development,
information about the team on the site is built by consuming that API rather
than building it into the templates.

### Projects API

This app includes information about the projects that the team is working on and
provides an API for retrieving that information.

This includes a few elements:

- IAAs: A bundle of money authorized to be spent by a client on projects
- Projects: A grouping of work around a common goal
- Buys: The individual procurements in the service of completing the project
goal.

In the interest of API-first development, information about the projects on the
site is built by consuming that API rather than building it into the templates.

### Templated documents

Since many projects will require the same documents, the app includes some
templates that can be filled in automatically with data from the database.

Because the documents need to be frozen at some point in time, but we'd like to
be able to update the templates iteratively, the documents are generated and the
raw Markdown is saved as part of a buy's data. This means that later document
regeneration may be necessary, but also prevents surprise changes and allows a
buy's documents to be customized away from the template if necessary.

Templates are currently stored within [the `projects` app](./projects/templates/projects/markdown/), though it may make sense for them to get their own app at some point.

In creating new templates, there are a couple things to know:

- The top-level header should use the underline style rather than hashtags. For
whatever reason, the Markdown renderer doesn't seem to pick up a header in the
first line, and Django won't allow a blank first line for the field.
- blockquotes don't seem to work right now

### UAA Authentication

There are several potential tiers of users:

1. Public users with no authentication
1. Internal users with cloud.gov-supported email addresses (currently @gsa.gov
  and @epa.gov)
1. Internal users who are also "teammates"
1. Internal users who are also "teammates" and have write privileges.
1. Admins

Authentication is handled through users' cloud.gov accounts. The app is copied
[from the CALC project](https://github.com/18F/calc/tree/develop/uaa_client)
with minimal edits for templating.

Users with accounts in the database can log in using their cloud.gov
credentials, but admins must create the account through the Django admin interface
before the user is able to successfully do so.

The `fake_uaa_provider` app provides a mock version of the authenticator for use
in development

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for additional information.

### Branching

Release branch: `release`
Development branch: `develop`

### Dependencies

This project uses `pip-tools` to manage dependencies. As a result, developers
should edit `requirements.in` and not `requirements.txt`.

For example:

```
echo Django >> requirements.in
pip-compile --output-file requirements.txt requirements.in
pip-sync
```

## Public domain

This project is in the worldwide [public domain](LICENSE.md). As stated in [CONTRIBUTING](CONTRIBUTING.md):

> This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
>
> All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.
