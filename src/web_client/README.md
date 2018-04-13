# Web Client

## 0. Table of Contents
1. [Overview](#overview)
2. [File Structure](#file-structure)
3. [Installation Instruction](#installation)
4. [File Structure](#file-structure)
5. [ML API](#api)
6. [Command Line](#command-line)

## Overview <a name="overview"></a>
The web client is a Vue.js application that integrates all micro-services and provides user interface to end users. The main focus of the web client is to 1) provides on-screen chatbot experience to the users and 2) delivery the system features as a whole.

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

The web client does not work if other micro-services are not running concurrently. In production and continue integration, all services including web client are built in docker; however, when developing in local, the docker does not build web client. The reason is docker doesn't rebuild itself when web client is updated, therefore not very efficient to work in docker environment.

To start work on web client, please makre sure you have installed [Node.js](https://nodejs.org/en/) 8 (Do not install v9.0+), and follow the following steps:
1. If you have not built the docker images for other micro-services yet, run `./cjl up` in the root directory of the repository. For more information, check the main README.
2. Once the micro-services are up, run `npm install` in web client directory.
3.
