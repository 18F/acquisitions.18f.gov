[![Build Status](https://travis-ci.org/18F/acquisitions.18f.gov.svg?branch=develop)](https://travis-ci.org/18F/acquisitions.18f.gov)
[![Code Climate](https://codeclimate.com/github/18F/acquisitions.18f.gov/badges/gpa.svg)](https://codeclimate.com/github/18F/acquisitions.18f.gov)
[![Test Coverage](https://codeclimate.com/github/18F/acquisitions.18f.gov/badges/coverage.svg)](https://codeclimate.com/github/18F/acquisitions.18f.gov/coverage)
[![Dependency Status](https://gemnasium.com/badges/github.com/18F/acquisitions.18f.gov.svg)](https://gemnasium.com/github.com/18F/acquisitions.18f.gov)


# acquisitions.18f.gov

This is the homepage for the TTS Office of Acquisitions. Its goal is to be a
public-facing site for the office's efforts, as well as an internal site for
coordinating and tracking work. See [the elements below](#elements) for more
about what's included.

## Setup and local development

See [the setup docs](./docs/setup.md) for direct and Docker installation information.

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
templates that can be filled in automatically with data from the database. This
ends up being a light contract-writing system.

Because the documents need to be frozen at some point in time, but we'd like to
be able to update the templates iteratively, the documents are generated and the
raw Markdown is saved as part of a buy's data. This means that later document
regeneration may be necessary, but also prevents surprise changes and allows a
buy's documents to be customized away from the template if necessary.

Templates are currently stored within [the `projects` app](./projects/templates/projects/markdown/), though it may make sense for them to get their own app at some point.

In creating new templates, note that the top-level header should use the
underline style rather than hashtags. For whatever reason, the Markdown renderer
doesn't seem to pick up a header in the first line, and Django won't allow a
blank first line for the field.

### News

Since this is designed to be public-facing, there's a small CMS inside of [the
`news` app](./news/) to create posts and share updates and information publicly.
Posts that are not drafts and have a publication date in the past are shown on
the front page (for a few recent ones) and each gets permalink. A blog,
basically. There's an accompanying RSS feed for the latest 20 posts, as well.

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

This project uses [`pip-tools`](https://github.com/nvie/pip-tools) to manage
dependencies. As a result, developers should edit `requirements.in` and not
`requirements.txt`. Similarly, development dependencies are kept in
`requirements-dev.in` and `requirements-dev.txt`.

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
