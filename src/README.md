# Source

The project is split into several modules; one per micro-service. The description of each microservice is shown below:

## Backend Service

This module is responsible for responding to the web client's API queries. It is also the primary point of contact for the other micro-services

## ML Service

This module is responsible for all things related to predicting outcomes and classifying based on precedent data

## Web Client

This module contains the Web UI that users will interact with

## Postgresql

This module contains the data persistence layer of our system

## NLP Service

This module is responsible for all things related to natural language processing which the user interacts with