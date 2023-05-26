
# ITVR Post Release Work
After the release is deployed on Prod
* Merge the tracking pull request to master
* Create the release from master amd make it as the lasted release 
* Create the new release branch from master
* Update the following fields .github/workflows/build-release.yaml
    * name
    * branches
    * PR_NUMBER
    * RELEASE_NAME
* Update .pipeline/lib/config.js
    * const version
* Update frontend/package.json
    * version
* Create the tracking pull request to merge the new release branch to master

# Pre-required Secrets before running the pipeline
itvr-keycloak
itvr-django-secret
itvr-django-salt
itvr-email-service
itvr-patroni-app
itvr-patroni-admin
itvr-object-storage
itvr-ncda
itvr-db-backup-s3

# Pre-required Image Streams before running the pipeline
itvr-frontend
itvr-backend
itvr-task-queue

