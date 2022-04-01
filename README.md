# itvr

## Development

Unfortunately we do not have a licence to use Docker Desktop at BC Gov. If you are on a mac [here is a blogpost](https://naomiaro.hashnode.dev/replacing-docker-desktop-with-lima-on-mac-os) about how to setup Lima as an alternative solution for development purposes.

### Backend
The backend and all services are setup to run via docker. To start everything up you can run in the project folder:

```sh
docker-compose up --build
```

This will start up a [postgres](https://www.postgresql.org/) database, a [Django](https://www.djangoproject.com/) web app, and a [MinIO](https://docs.min.io/docs/minio-quickstart-guide.html) service with a bucket `itvr`

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

#### MinIO
You can view the contents of the bucket in MinIO by visiting `http://localhost:9001/login`. Use env variables `MINIO_ROOT_USER` and `MINIO_ROOT_PASSWORD` to login to the console. Default values are found in `minio.env`

We take advantage that MinIO is S3 compatible and use [django-storages](https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html) S3 backend for media files.

### Auth
We are using a shared realm [Keycloak](https://www.keycloak.org/) client. Shared realm clients can be accessed and configured via [Common Hosted Single Sign-on (CSS)](https://bcgov.github.io/sso-requests)

Once added as a team member to existing projects (this project is called `itvr`), you can configure the redirect urls for each environment (dev, test, prod). Installation json is available as well as some helpful documentation about integrating the client.

### Email
We are using [CHES](https://digital.gov.bc.ca/common-components/common-hosted-email-service) to send email. Documentation is [available here](https://getok.nrs.gov.bc.ca/app/documentation)

To get access to the created client, go [request account](https://getok.nrs.gov.bc.ca/app/requestAccount) with application acronym `ITVR`. This will allow you to reset client secrets for environments (dev, test, prod) as needed.

### Frontend
We've decided to run the frontend outside of docker at this time mostly because of mounted Lima volumes causing issues with npm permissions. [Track the open issue](https://github.com/lima-vm/lima/issues/693) 


To run the frontend you will need [node.js](https://nodejs.org/en/) installed. A good way to manage node these days is with [asdf](https://asdf-vm.com/guide/getting-started.html#_1-install-dependencies). File `.tool-versions` contains current versions of tools used in this application. After setting up asdf run this at the project root:

```sh
asdf plugin add nodejs https://github.com/asdf-vm/asdf-nodejs.git
asdf install
```

The frontend is built using [Create React App](https://create-react-app.dev/). To run the frontend:

```sh
cd frontend
npm i
npm start
```

The app is available by default at `http://localhost:3000/`

### Storybook
To use [Storybook](https://storybook.js.org/) for developing a component:

```sh
cd frontend
npm run storybook
```

The storybook is available by default at `http://localhost:6006/`

## Deployment
We use [Openshift](https://www.redhat.com/en/technologies/cloud-computing/openshift) to deploy our applications. [Access the console here](https://console.apps.silver.devops.gov.bc.ca/k8s/cluster/projects)

There's training on Openshift offered by BCDevExchange. Check the [schedule here](https://bcdevexchange.org/learning)

