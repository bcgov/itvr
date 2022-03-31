# itvr

## Development

Unfortunately we do not have a licence to use Docker Desktop at BC Gov. If you are on a mac [here is a blogpost](https://naomiaro.hashnode.dev/replacing-docker-desktop-with-lima-on-mac-os) about how to setup Lima as an alternative solution for development purposes.

### Backend
The backend and all services are setup to run via docker. To start everything up you can run in the project folder:

```sh
docker-compose up --build
```

This will start up a [postgres](https://www.postgresql.org/) database, a [Django](https://www.djangoproject.com/) web app, and a [MinIO](https://docs.min.io/docs/minio-quickstart-guide.html) service with a bucket `itvr`

You can view the contents of the bucket in MinIO by visiting `http://minio:9001/login`. Use env variables `MINIO_ROOT_USER` and `MINIO_ROOT_PASSWORD` to login to the console. Default values are found in `minio.env`

We take advantage that MinIO is S3 compatible and use [django-storages](https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html) S3 backend for media files.

### Auth
We are using a shared realm [Keycloak](https://www.keycloak.org/) client. Shared realm clients can be accessed and configured via [Common Hosted Single Sign-on (CSS)](https://bcgov.github.io/sso-requests)

Once added as a team member to existing projects, you can configure the redirect urls for each environment (dev, test, prod). Installation json is available here as well as some helpful documentation about integrating the client.

### Email
We are using [CHES](https://digital.gov.bc.ca/common-components/common-hosted-email-service) to send email. Documentation is [available here](https://getok.nrs.gov.bc.ca/app/documentation)

### Frontend
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
npm run storybook
```

The storybook is available by default at `http://localhost:6006/`
