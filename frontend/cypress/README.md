(1) To open the Cypress app, cd to the frontend project, and run "npx cypress open" (you may need to run "npm install" first if you don't have cypress installed yet). Then, select "E2E Testing" and choose a browser where you want to conduct the tests.

(2) You will also need to configure some environment variables in order to allow cypress to log in to the app. See the "cypress.env.json" file in the frontend project; the login credentials can be supplied by setting them in your bash/zsh/other profile; see https://docs.cypress.io/guides/guides/environment-variables#Option-3-CYPRESS_.
