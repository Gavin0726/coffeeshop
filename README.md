
## Final Project

The project aims to develop infrastructure on AWS and utilise CircleCI to develop a CI/CD pipeline to deploy Docker container. 

This project is full stack nano project by udacity. 


### The files in the repository

1.  `.circleci`has one configuration file config.yml that includes the necessary instructions to setup a CICD pipeline to fully automate the process

2.  `./backend` directory contains a Flask server with a sqlite database and integrate Auth0 for authentication.

3.  `./frontend` directory contains a Ionic frontend to consume the data from the Flask server with the Auth0 configuration. 

4.  `./k8s_yml` directory contains the infra yml files to create VPC, eks cluster, eks nodes, and auth_cm. also contains deployment yml files to deploy backend and frontend.

