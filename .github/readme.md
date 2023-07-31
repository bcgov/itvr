
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

# ITVR Pipelines

## Primary Pipelines

* release-build.yaml (ITVR release-1.19.0): build release and deploy on test and prod
* dev-cicd.yaml (ITVR Dev release-1.19.0): continuous to build teh tracking pull request and deploy on dev
* pr-dev-cicd.yaml (ITVR PR Dev CICD): build pull request if it's title ends with build-on-dev

## Other Pipelines

* cleanup-cron-workflow-runs.yaml (Scheduled cleanup old workflow runs): cron job to cleanup the old workflows
* cleanup-workflow-runs.yaml (Cleanup old workflow runs): cleanup the old workflows
* pr-build-template.yaml (PR Build Template): pull request build template
* pr-deploy-template.yaml (PR Deploy Template): pull request deploy template
* pr-dev-database-template (ITVR PR Dev Database Template): template to setup database for pull request build
* pr-teardown.yaml (ITVR PR DEV Teardown on Dev): tear down pull request deployment on dev

# Prerequisites before running the pipeline

## Secrets 
* itvr-keycloak  
* itvr-django-secret  
* itvr-django-salt  
* itvr-email-service  
* itvr-patroni-app  
* itvr-patroni-admin  
* itvr-object-storage  
* itvr-ncda  
* itvr-db-backup-s3  

## Image Streams 
* itvr-frontend  
* itvr-backend  
* itvr-task-queue  