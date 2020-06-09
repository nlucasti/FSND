/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

 export const environment = {
   production: false,
   apiServerUrl: 'https://fsnd-casting-app.herokuapp.com', // the running FLASK api server url
   auth0: {
     url: 'nl-fsnd', // the auth0 domain prefix
     audience: 'casting', // the audience set for the auth0 app
     clientId: 'iXBHbMKRXOs8Krk3TfioJQ8WOckcDH0e', // the client id generated for the auth0 app
     callbackURL: 'https://fsnd-casting-frontend.herokuapp.com', // the base url of the running ionic application.
   }
 };
// export const environment = {
//   production: false,
//   apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
//   auth0: {
//     url: 'nl-fsnd', // the auth0 domain prefix
//     audience: 'casting', // the audience set for the auth0 app
//     clientId: 'iXBHbMKRXOs8Krk3TfioJQ8WOckcDH0e', // the client id generated for the auth0 app
//     callbackURL: 'http://localhost:8100', // the base url of the running ionic application.
//   }
// };
