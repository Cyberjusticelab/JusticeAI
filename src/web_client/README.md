# ProceZeus

## Building the Web Client Docker Image

Before running any command, the Docker image for the web client must first be built.

```bash
docker build -t web_app .
```

## Running and Testing

### Run the Web Client

```bash
docker run -t --rm -p 127.0.0.1:3039:3039 web_app
```

### Run Unit Tests
```bash
docker run -t --rm -p 127.0.0.1:3039:3039 web_app bash -c "npm run test"
```

### Run Linting
```bash
docker run -t --rm -p 127.0.0.1:3039:3039 web_app bash -c "npm run lint"
```

## Technologies

The following technologies are in use in this service:

### Bootstrap

[Bootstrap](https://getbootstrap.com) is an open source front end framework developed by Twitter. It contains styling for various common web components, such as forms and inputs, as well as providing a convenient grid system that greatly facilitates web page styling and layout.
- Alternatives: Foundation Framework, pure.css, skeleton
- Reason Chosen:
  - Team member’s past experiences
  - Industry standard

### Vue.js

(Vue.js)[https://vuejs.org/] is an open source front end framework for building single page applications. It leverages component based architecture that allows for the creation of an interactive website. Its primary purpose will be to power the visible portion of the chatbot, displaying messages, sending messages to the server, and prompting the user for various interactions such as answering questions or providing files to use as evidence.
- Alternatives: AngularJS, Angular 4, ReactJs
- Reason Chosen:
  - Low learning curve
  - High performance
  - Small footprint and minimal API

