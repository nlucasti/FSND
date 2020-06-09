export const environment = {
  production: true,
  apiServerUrl: 'https://fsnd-casting-app.herokuapp.com/', // the running FLASK api server url
  auth0: {
    url: 'nl-fsnd', // the auth0 domain prefix
    audience: 'casting', // the audience set for the auth0 app
    clientId: 'iXBHbMKRXOs8Krk3TfioJQ8WOckcDH0e', // the client id generated for the auth0 app
    callbackURL: 'https://fsnd-casting-frontend.herokuapp.com', // the base url of the running ionic application.
  }
};
