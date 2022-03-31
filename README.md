# itvr

## Development

Unfortunately we do not have a licence to use Docker Desktop at BC Gov. If you are on a mac [here is a blogpost](https://naomiaro.hashnode.dev/replacing-docker-desktop-with-lima-on-mac-os) about how to setup Lima as an alternative solution for development purposes.

### Backend
The backend and all services are setup to run via docker. To start everything up you can run in the project folder:

```sh
docker-compose up --build
```

This will start up a postgres database, a Django web app, and a minio service with a bucket `itvr`

### Frontend
The frontend is built using Create React App. To run the frontend:

```sh
cd frontend
npm i
npm start
```

To use Storybook for developing a component:

```sh
npm run storybook
```
