# Deployment

## On Cloud Foundry

The cloud.gov documentation provides some [general steps](https://cloud.gov/docs/apps/django/) for deploying a Django application.

### Creating the application

If no application exists yet, begin by targeting the correct space:

```
cf target -o gsa-acq-proto -s staging
```

Create a non-functioning app so that services can bind to something:

```
cf push -f manifest-staging.yml --no-start
```

Create and bind a database as discussed in [the cloud.gov database documentation](https://cloud.gov/docs/apps/databases/):

```
cf create-service aws-rds shared-psql acquisitions-staging-psql
cf bind-service acquisitions-staging acquisitions-staging-psql
```

Further configuration is stored in [**user-provided services**](https://docs.cloudfoundry.org/devguide/services/user-provided.html), as discussed below.

### New Relic

Create a user-provided service, replacing `the-license-key` with the New Relic license key:

```
cf create-user-provided-service acquisitions-new-relic -p '{"NEW_RELIC_LICENSE_KEY": "the-license-key"}'
```

### Pushing the application

Deployment is handled via Travis CI, so manual pushing is typically not required.

In the event that a manual push is required, a zero-downtime push is preferred. Make sure that `autopilot` is installed:

```
cf install-plugin autopilot -f -r CF-Community
```

Check the target:

```
cf target -o gsa-acq-proto -s staging
```

And push:

```
cf zero-downtime-push acquisitions-staging -f manifest-staging.yml
```
