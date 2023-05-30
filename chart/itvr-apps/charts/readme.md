# Sample pull request build

## Frontend

openshift/templates/frontend $
oc process -f ./frontend-bc-docker.yaml \
NAME=itvr \
SUFFIX=-build-497 \
VERSION=build-release-1.17.0-497 \
GIT_URL=https://github.com/bcgov/itvr.git \
GIT_REF=refs/pull/497/head \
| oc apply --wait=true -f - -n <tools-namespace>

## Backend

oc process -f ./backend-bc.yaml \
NAME=itvr \
SUFFIX=-build-497 \
VERSION=build-release-1.17.0-497 \
GIT_URL=https://github.com/bcgov/itvr.git \
GIT_REF=refs/pull/497/head \
| oc apply --wait=true -f - -n <tools-namespace>

## Task Queue

oc process -f ./task-queue-bc.yaml \
NAME=itvr \
SUFFIX=-build-497 \
VERSION=build-release-1.17.0-497 \
GIT_URL=https://github.com/bcgov/itvr.git \
GIT_REF=refs/pull/497/head \
| oc apply --wait=true -f - -n <tools-namespace>

# Deploy

## Single pull request Deploy on Dev

helm template -f ./values-dev.yaml \
--set suffix=-dev-497 \
--set namespace=ac294c-dev \
--set frontendImageTagName=dev-release-1.17.0-497 \
--set envName=dev \
-n ac294c-dev -f ./values-dev.yaml itvr-frontend-dev-497 .

## Backend

helm template -f ./values-dev.yaml \
--set suffix=-dev-497 \
--set namespace=ac294c-dev \
--set backendImageTagName=dev-release-1.17.0-497 \
--set suffix=-dev-497 \
--set envName=dev \
-n ac294c-dev -f ./values-dev.yaml itvr-backend-dev-497 .

## Task Queue

helm template -f ./values-dev.yaml \
--set suffix=-dev-497 \
--set namespace=ac294c-dev \
--set taskQueueTagName=dev-release-1.17.0-497 \
--set suffix=-dev-497 \
--set envName=dev \
-n ac294c-dev -f ./values-dev.yaml itvr-task-queue-dev-497 .

Notes: For tracking pull request Deploy on Dev, set suffix=dev-497 from previous command line and everything else is same

