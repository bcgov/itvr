describe('submit bceid application', () => {
  before(() => {
    cy.visit('/');
  });
  beforeEach(() => {
    cy.login({
      root: Cypress.env('KEYCLOAK_URL'),
      realm: Cypress.env('KEYCLOAK_REALM'),
      username: Cypress.env('BCEID_KEYCLOAK_USERNAME'),
      password: Cypress.env('BCEID_KEYCLOAK_PASSWORD'),
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
  let applicationId = '';
  const last_name = 'Smith';
  const first_name = 'John';
  const today = new Date();
  const date_of_birth_out = new Date(
    today.getFullYear() - 16,
    today.getMonth(),
    today.getDate()
  )
    .toISOString()
    .split('T')[0];
  const address = '111 Cambie Street';
  const city = 'Vancouver';
  const postal_code = 'V1V1V1';
  const email = Cypress.env('APPLICATION_EMAIL');
  const sin = '000000000';
  let dl = 0;
  while (dl < 1000000) {
    dl = Math.floor(Math.random() * 10000000);
  }
  it('fill out form and submit', () => {
    cy.visit('/form');
    cy.contains('Logged in as');
    cy.get('#last_name').type(last_name);
    cy.get('#first_name').type(first_name);
    cy.get('#address').type(address);
    cy.get('#city').type(city);
    cy.get('#postal_code').type(postal_code);
    cy.get('#email').type(email);
    cy.get('#sin').type(sin);
    cy.get('#drivers_licence').type(dl);
    cy.get('#consent_personal').check();
    cy.get('#consent_tax').check();
    cy.get('#documents').attachFile('file1.jpeg', {
      subjectType: 'drag-n-drop'
    });
    cy.get('#documents').attachFile('file2.jpeg', {
      subjectType: 'drag-n-drop'
    });
    cy.contains('Submit Application').click();
    cy.contains('Success');
    cy.get('#application_id').should(($element) => {
      applicationId = $element.text();
    });
  });
  it('verify form details', () => {
    cy.visit('/details/' + applicationId);
    cy.get('#last_name').should('have.text', last_name);
    cy.get('#first_name').should('have.text', first_name);
    cy.get('#date_of_birth').should('have.text', date_of_birth_out);
    cy.get('#address').should('have.text', address);
    cy.get('#city').should('have.text', city);
    cy.get('#postal_code').should('have.text', postal_code);
    cy.get('#email').should('have.text', email);
    cy.get('#drivers_licence').should('have.text', dl);
  });
});
