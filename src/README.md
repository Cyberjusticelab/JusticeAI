# Archicture and Infrastructure

## Services

The project is split into several modules; one per micro-service. The description of each microservice is shown below:

### Backend Service

This module is responsible for responding to the web client's API queries. It is also the primary point of contact for the other micro-services

### ML Service

This module is responsible for all things related to predicting outcomes and classifying based on precedent data

### Web Client

This module contains the Web UI that users will interact with

### Postgresql

This module contains the data persistence layer of our system

### NLP Service

This module is responsible for all things related to natural language processing, which the user interacts with

## Infrastructure and Continuous Integration/Deployment

The ProceZeus application has many components with a and requires lots of binaries for the various machine learning models. We use `docker` and `docker-compose` to manage all of that complexity. Although you'll need to have these tools installed to build ProceZeus, we've hidden the gory details from you by providing a handy `cjl` script.

`cjl` is a thin wrapper around the `docker-compose` command, so any command that would work for `docker-compose` should also work for `cjl`. However, `cjl` contains utility functions to automatically lint your code, run tests, reset the database, remove all Docker images, and more! You can read more about the functions available in `cjl` in the "Getting Started" section.

`docker-compose` configuration files are currently split based on the environment. Running `./cjl build && ./cjl up` will default to a dev environment, which uses the `docker-compose.dev.yml` configuration. This can be changed by specifying the environment you like with the `COMPOSE_FILE` environment variable. For example, this technique is used in the CI environment to run tests and upload the code coverage reports instead of running the application.

We're using [Travis CI](https://travis-ci.org/Cyberjusticelab/JusticeAI/branches) for as a continuous integration service to run our tests on our latest changes pushed to Git. The details are in `.travis.yml`, but Travis uses a build matrix in order to test each service in a separate process. We've also added an additional constraint where every commit message must begin with a reference to an issue (eg. `[#123]`) in order to improve the trackability of our work. If a build fails, GitHub will not let you merge in your changes.

Once a service's tests have completed running, the test line code covereage is uploaded to [CodeCov.io](https://codecov.io/gh/Cyberjusticelab/JusticeAI). This service ensures that we're always maintaining a reasonable number of tests for our application over time. This check is more informational, and is not required to pass for a build to be merged.

We do currently have some sort of continuous deployment onto a VPS provided to us by UdeM at `capstone.cyberjustice.ca`. It's currently configured to deploy after the end of a successful Travis build, but with the parallelization, it often fails and is extremely error prone. We've begun investigating standing up a webhook notification server on `capstone.cyberjustice.ca` that GitHub can push a notification to once a PR is merged, but it has not been flawless either.

## Future Improvement

- [ ] Investigate a more robust solution to continous deployment


