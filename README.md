# ProceZeus

[![Travis](https://img.shields.io/travis/Cyberjusticelab/JusticeAI.svg)](https://travis-ci.org/Cyberjusticelab/JusticeAI/) [![Codecov](https://img.shields.io/codecov/c/github/codecov/example-python.svg)](https://codecov.io/gh/Cyberjusticelab/JusticeAI)

## Getting Started

### Prerequisites

All of the project's services are split into separate Docker images. All application dependencies are contained within the Docker images. The dependencies required to run this project locally are:

- `docker`
- `docker-compose`

### Installing

To install Docker and Docker Compose, you can follow the instructions [here](https://docs.docker.com/).

## Running the Entire Application Stack

We've developed a script to help with running the entire application with all its components. All you need is:

```
./cjl up -d
```

In order to shut down all containers:

```
./cjl down
```

## Running or Testing Specific Services

The following services can run individually or tested against:
- [Web Client](src/web_client/README.md)

## Deployment

We intend to deploy our application with continuous delivery. This is a task is expected to be completed by Iteration #2.

## Architecture

The following architecture diagram represents the various services and the relationships they have with one another.

![High Level Architecture](/images/high-level-architecture.png)

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Versioning

There are currently no releases versions of our software.

## Authors

TBD

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

TBD
