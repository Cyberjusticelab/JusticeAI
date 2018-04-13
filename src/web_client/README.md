# Web Client

1. [Overview](#overview)
2. [File Structure](#file-structure)
3. [Installation Instruction](#installation)
4. [Develop on Components](#component)
5. [Testing](#testing)
6. [Reference](#reference)

## Overview <a name="overview"></a>
The web client is a Vue.js application that integrates all micro-services and provides a user interface to end users. The main focus of the web client is to 1) provides on-screen chatbot experience to the users and 2) delivery the system features as a whole.

The major technologies we use in web client are:
- Build Tool: [Webpack](https://webpack.js.org/)
- Framework: [Vue.js](https://vuejs.org/)
- UI Library: [ElementUI](http://element.eleme.io/#/en-US)

## File Structure<a name="file-structure"></a>

Below is a list of the most important files and directories
```
-/build                             // includes all webpack build configuration
-/config                            // includes all webpack environment configuration
-/src                               // source code of the vue.js application
-/test                              // unit test
index.html                          // main index file
Dockerfile                          // docker configuration
package.json                        // application dependencies
```
When developing on UI and features, you should mostly work on `src` folder without touching the other directories and files.

## Installation Instruction<a name="installation"></a>

The web client does not work if other micro-services are not running concurrently. In production and continuous integration, all services including web client are built in docker; however, when developing in local, the docker does not build web client. The reason is docker doesn't rebuild itself when web client is updated, therefore not very efficient to work in docker environment.

To start work on the web client, please make sure you have installed [Node.js](https://nodejs.org/en/) 8 (Do not install v9.0+), and follow the following steps:
1. If you have not built the docker images for other micro-services yet, run `./cjl up` in the root directory of the repository. For more information, check the main README.
2. Once the micro-services are up, run `npm install` in web client directory.
3. When the installation is finished, run `npm run start` to start the application
4. When the application is running, you can edit the source code. The latest changes will be shown in the browser.

## Develop on Components<a name="component"></a>

Under `src` directory, you should see the application source code with the following folders:
```
-/assets                            // static assets such as images
-/components                        // reusable components
-/router                            // url router
-/theme                             // styling
```

Vue.js is component based Javascript framework, therefore each `.vue` file creates a reusable component.  Each component is able to be run independently.

So far in our application, we have:
- `Landing.vue`: the landing page component is used to handle first-time users
- `Dashboard.vue`: the main component that contains `Sidebar.vue` component and `Chat.vue` component. When `Sidebar.vue` component handles the data display on the UI, the `Chat.vue` component handles all the logic related to the chatbot.
- `Legal.vue`: the legal page component is used to fetch and show the latest Privacy Policy and End User License Agreement.
- `Eventbus.js`: a bus for component communications.

`.vue` file usually contains all necessary codes for a component (Javascript, HTML, and CSS). To make our lives easier, all styling is configurated and written in SASS format and stored in the `theme` folder. To change the styling of the UI, you only need to edit the corresponding `.scss` file without touching the functional codes.

 Due to the simplicity of the nature of the application, we did not implement state management architecture. As mentioned above, we use `Eventbus.js` to handle component communication. If you want to have major refactoring in the future, you can check out [Vuex](https://vuex.vuejs.org/en/).

We use ElementUI as the UI library. It is the best library available for Vue.js. For the best practice and code consistency, you should always check if the feature can be implemented using Element component.

## Testing<a name="testing"></a>

The unit test of the web client is using the default [Vue.js unit test library](https://vuejs.org/v2/guide/unit-testing.html), which is built with Mocha. To test the application locally, run `npm run test`.

All unit test files are stored in `test/unit` directory. Each `.spec.js` file contains the unit tests for the corresponding component. You should always make sure your new changes are well tested. Once you run the test, the test report will be generated in `test/unit/converage`. You can open `test/unit/converage/icov-report/index.html` to see the visual report.

Due to the scope of the project, we did not implement E2E automation test. To do so, please check [Nightwatch.js](http://nightwatchjs.org/).

## Reference<a name="reference"></a>

- [Vue.js 2.x Documentation](https://vuejs.org/)
- [ElementUI Documentation](http://element.eleme.io/#/en-US)



