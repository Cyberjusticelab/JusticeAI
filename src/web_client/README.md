# Web Client Service

## Run Tests and Lints

```
export COMPOSE_FILE=ci
./cjl up -d && ./cjl run web_client
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

