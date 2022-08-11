describe('submit bcsc application', () => {
  before(() => {
    cy.visit('/');
  });
  beforeEach(() => {
    cy.login({
      root: Cypress.env('KEYCLOAK_URL'),
      realm: Cypress.env('KEYCLOAK_REALM'),
      username: Cypress.env('BCSC_KEYCLOAK_USERNAME'),
      password: Cypress.env('BCSC_KEYCLOAK_PASSWORD'),
      client_id: Cypress.env('KEYCLOAK_CLIENT_ID'),
      redirect_uri: 'http://localhost:3000/form'
    });
  });
  afterEach(() => {
    cy.logout({
      root: Cypress.env('KEYCLOAK_URL'),
      realm: Cypress.env('KEYCLOAK_REALM'),
      redirect_uri: 'http://localhost:3000'
    });
  });
  it('fill out form and submit', () => {
    cy.visit('/form');
    cy.contains('Logged in as');
  });
});
