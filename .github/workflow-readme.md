# How to build a pull request and deploy on Openshift Dev environment

## Register the redirect url on SSO Console

- Open a brower to https://bcgov.github.io/sso-requests
- My Dashboard -> My Projects: edit project "ITVR on Gold Cluster"
- Add a new redirect url for Development environment, https://itvr-frontend-dev-<pr number>.apps.silver.devops.gov.bc.ca/\*
- Submit the change

Notes: the change may take about 20 minutes to be promoted to ITVR development environment on Openshift

## Add the build-on-dev to the end of pull request's title

The "Build PR on Dev" pipeline will be triggered when it identified pull request's title ends with "build-on-dev"

# Production release

## Pre-production release

- Update the description of the tracking pull request, the description will be copied as teh release notes later on
- Verify the changes made during the previous post production release

## Production release

- Manually trigger the pipeline release-build.yaml (ITVR release-1.19.0)

## Post production release

### Merge the tracking pull request and create the new release branch

- Squash merge the tracking pull request to main
- Create the release on GitHub from main branch
- Create the new release branch from main branch
- Change the new release branch as the default branch in the repo and update the branch protection rules https://github.com/bcgov/itvr/settings/branches
- Update frontend/package.json
  - version
- Create the tracking pull request to merge the new release branch to main. Update the pull_request in .github/workflows/release-build.yaml after the tracking pull request is created

# ITVR Pipelines

## Primary Pipelines

- dev-ci.yaml: Build the tracking pull request and delpoy on Dev
- test-ci.yaml: Tag the running images on Dev to Test and delpoy on Test
- prod-ci.yaml: Tag the running images on Test to Test and delpoy on Prod

## Other Pipelines

- cleanup-cron-workflow-runs.yaml (Scheduled cleanup old workflow runs): cron job to cleanup the old workflows
- cleanup-workflow-runs.yaml (Cleanup old workflow runs): cleanup the old workflows
- pr-build.yaml pull request build

# Prerequisites before running the pipeline

All the followings are already on Openshift. The purpose of this section is for creating a brand new environment on cloud.

## Secrets

- itvr-keycloak
- itvr-django-secret
- itvr-django-salt
- itvr-email-service
- itvr-patroni-app
- itvr-patroni-admin
- itvr-object-storage
- itvr-ncda
- itvr-db-backup-s3

## Image Streams

- itvr-frontend
- itvr-backend
- itvr-task-queue
- itvr-cra
