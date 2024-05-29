[![SonarCloud](https://sonarcloud.io/images/project_badges/sonarcloud-white.svg)](https://sonarcloud.io/summary/new_code?id=bcgov_itvr)

# ITVR
[![Lifecycle:Stable](https://img.shields.io/badge/Lifecycle-Stable-97ca00)](https://goelectricbc.gov.bc.ca/)

## Project description 

The Clean Transportation Branch within the Ministry of Energy, Mines and Low Carbon Innovation instructed the build of the ITVR application. The instruction was to build an online portal to allow the public to apply for pre-approval, based on their income level, to receive a provincial rebate on the purchase of a new zero-emission vehicle. The application was launched to the public in August 2022. 

The provincial program providing rebates has been running for several years and was open to anyone regardless of income. Changes to means-test the program created the need for a pre-approval process where applicants identities are verified, and their incomes checked with Canada Revenue Agency (CRA). 

The program is managed by a government appointed delivery agent, the New Car Dealers Association (NCDA). They are responsible for working with car dealerships to provide the actual vehicle rebates to the public.  

The ITVR application consists of these main elements: 
* Online public application form, accessed using BCeID or Services Card app 
* Internal console for government to search, review and process applications 
* Ability to send/receive applicant data with CRA to check incomes (using FTP) 
* Ability to send/receive income approved applicant data with NCDA (using API) 
* Automated email functionality to provide applicants with information on their application 

## System

ITVR system statuses and workflow can be [found documented in the flowchart](https://preview.uxpin.com/7f6104a26108508bb185e1b602677a5f91f49724#/pages/148655810/simulate/no-panels?mode=mf)

### Development

All services are setup to run via docker. To start everything up you can run in the project folder:

```sh
docker-compose up --build
```

This will start up a [postgres](https://www.postgresql.org/) database, a [Django](https://www.djangoproject.com/) web app, a [React](https://react.dev/) frontend app, a [Spring](https://spring.io/projects/spring-boot) REST service, and a [MinIO](https://docs.min.io/docs/minio-quickstart-guide.html) service with a private bucket `itvr`

Add this entry to your `/etc/hosts` file:

```sh
127.0.0.1 minio
```

#### Django

Django offers many helpful [mangement commands](https://docs.djangoproject.com/en/4.0/ref/django-admin/) out of the box. To be able to use these with docker you can access the python environment with bash:

```sh
docker-compose exec api bash
```

To create a Django admin user try running this command in the shell:

```sh
python manage.py createsuperuser
```

The admin panel is available here: `http://localhost:8000/admin/`

You can view Django Restframework's browseable api here: `http://localhost:8000/api/`

Use a created superuser to login and view the api.

### postgres
To get into postgres in terminal
docker-compose exec db psql -U postgres itvr


#### MinIO

You can view the contents of the bucket in MinIO by visiting `http://localhost:9001/login`. Use env variables `MINIO_ROOT_USER` and `MINIO_ROOT_PASSWORD` to login to the console. Default values are found in `minio.env`

We take advantage that MinIO is S3 compatible and use [django-storages](https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html) S3 backend for media files.

### Auth

We are using a shared realm [Keycloak](https://www.keycloak.org/) client. Shared realm clients can be accessed and configured via [Common Hosted Single Sign-on (CSS)](https://bcgov.github.io/sso-requests)

Once added as a team member to existing projects (this project is called `itvr`), you can configure the redirect urls for each environment (dev, test, prod). Installation json is available as well as some helpful documentation about integrating the client.

### Email

We are using [CHES](https://digital.gov.bc.ca/common-components/common-hosted-email-service) to send email. Documentation is [available here](https://getok.nrs.gov.bc.ca/app/documentation)

To get access to the created client, go [request account](https://getok.nrs.gov.bc.ca/app/requestAccount) with application acronym `ITVR`. This will allow you to reset client secrets for environments (dev, test, prod) as needed.

### CRA

Submitting wage requests can be done manually by logging into
ftp://ftp-ot.cra-arc.gc.ca/pub/BC/iv/bcvr/ anonymously and dropping any encrypted files in the uaclient2cra folder. Within a short time the encrypted response will be available within the uacra2client folder. All security is trusted within the encryption algorithm. Anybody can download a file from here. Only the target user/computer can decrypt the file.

For the next valid sequence number:

If you ever are not sure, Susan can verify with ITB or send a request with the last sequence you are aware of and it will will fail but you will get an email notification indicating the error and what the next available sequence is.

Example of the contents of the error email for wrong sequence number:

THE FOLLOWING FILENAME IS EXCLUDED FROM PROCESSING PLEASE INVESTIGATE THE FILE LISTED BELOW:
INPUT FILENAME: DEMO.A00154
REASON : INVALID SEQUENCE NUMBER ON INPUT FILENAME

        THE NEXT VALID SEQUENCE NUMBER TO USE IS :   00155

### Spring

This is a service that uses Entrust's Java toolkit to encrypt/decrypt files.

## Frontend

The frontend is built using [Create React App](https://create-react-app.dev/).

The app is available by default at `http://localhost:3000/`

## Deployment

We use [Openshift](https://www.redhat.com/en/technologies/cloud-computing/openshift) to deploy our applications. [Access the console here](https://console.apps.silver.devops.gov.bc.ca/k8s/cluster/projects)

There's training on Openshift offered by BCDevExchange. Check the [schedule here](https://bcdevexchange.org/learning)

### Git Process/ Rebasing

We use git for version control.
Each developer has their own fork of the repo and works off of branches from there
If another branch is merged in (eg from another developer) then the branch in progress will need
to be rebased before it gets merged in.

Steps:
git checkout release-branch
git fetch upstream
git pull --rebase upstream release-branch
git checkout featurebranch
git rebase release-branch

If there are any conflicts, you will have to step through each commit and fix them. After
conflicts are fixed and added (git add) then:

git rebase --continue

until all of the conflicts are fixed.

If you already have a branch at origin you'll have to force push, otherwise doing a
regular push will just give errors:
git push -f origin <feature-branch>

### Testing

backend tests will be recognized and run with other tests if they have follow this naming convention:
test\_[name].py
eg. test_calculate_rebate.py

to run tests use a terminal in the api container and type
python manage.py test

or to run specific test files, point to the folder or file
python manage.py test api.services.tests.test_calculate_rebate

### Scheduled Jobs

Currently, when the task-queue application starts, it creates scheduled jobs only if those jobs don't already exist in the database. This means that if some aspects of a job are changed (e.g. its arguments concerning timeout time, etc), one has to delete the job first in the admin console before deploying, or update the job manually in the admin console after deploying.

# List of Dev Work | What to do before bringing in a new ticket into a Sprint

This is a list that was created on 2023-02-01 with all Zelda Devs to provide alternative work instead of bringing in a new ticket.

\*_Team Rule_ Do not bring in ticket After Friday

1. Help another Dev - see if other Devs need help to finish their ticket

2. PR Reviews – linked to the task above

3. Writing additional tests – for both tront and back end

4. Take a look at Tech Debt tickets - If we bring in tickets let's bring in Tech Debt first

5. Learning time:

- Take the opportunity to familiarize yourself with business logic, tech (anything around work we do)

- New learning and applying it to our work

- Innovation work
