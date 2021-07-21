
export const environment = {
  production: true,
  apiServerUrl: 'http://a10c0040a80a34e79b18528824d77a5a-882124262.us-east-1.elb.amazonaws.com', // the running FLASK api server url
  auth0: {
    url: 'gavinguo.au', // the auth0 domain prefix
    audience: 'coffeeshop', // the audience set for the auth0 app
    clientId: 'bqSGYXo9iNZqfKFzKQNA0O5ZHDWFjpSq', // the client id generated for the auth0 app
    callbackURL: 'http://a7dbc7ee8db49478cbf6f134b3ecef23-2109055788.us-east-1.elb.amazonaws.com', // the base url of the running ionic application. 
  }
};
