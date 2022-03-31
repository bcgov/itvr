# itvr

## Development

Unfortunately we do not have a licence to use Docker Desktop at BC Gov. If you are on a mac [here is a blogpost](https://naomiaro.hashnode.dev/replacing-docker-desktop-with-lima-on-mac-os) about how to setup Lima as an alternative solution for development purposes.

### Backend
The backend and all services are setup to run via docker. To start everything up you can run in the project folder:

```sh
docker-compose up --build
```

This will start up a [postgres](https://www.postgresql.org/) database, a [Django](https://www.djangoproject.com/) web app, and a [minio](https://docs.min.io/docs/minio-quickstart-guide.html) service with a bucket `itvr`

You can view the contents of the bucket in minio by visiting `http://minio:9001/login`. Use env variables `MINIO_ROOT_USER` and `MINIO_ROOT_PASSWORD` to login to the console. Default values are found in `minio.env`

### Auth
We are using a shared realm [Keycloak](https://www.keycloak.org/) client. Shared realm clients can be accessed and configured via [Common Hosted Single Sign-on (CSS)](https://bcgov.github.io/sso-requests)

### Frontend
The frontend is built using [Create React App](https://create-react-app.dev/). To run the frontend:

```sh
cd frontend
npm i
npm start
```

To use [Storybook](https://storybook.js.org/) for developing a component:

```sh
npm run storybook
```
