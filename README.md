# Lecture Quiz App

## Overview

This is an app for hosting educational content with interactive and auto-graded comprehension questions.

Teachers should be able to upload `lectures` which contain a title and text body.

Teachers should be able to create `problem_sets` for each lecture. Each problem set should reference several `problems`. Each problem should have a prompt, several multiple choice options and an answer.

Students should be able to view the lectures, submit answers to the problem sets, and instantly get feedback.

## Architecture

The backend consists of a REST API server build in [Python Flask](https://flask.palletsprojects.com) which is connected to a MySQL database.

The frontend client will be written in JavaScript.

![architecture](./docs/architecture_diagram.png)

## Infrastructure

The `infrastructure` folder defines the infrastructure necessary to deploy the application, as code.

`infrastructure/docker-compose.yml` defines a deployment template to run all the necesssary services on a single host.

The template includes
* a MySQL server with a database schema defined in `infrastructure/schema.sql`
* A REST server for the backend defined in `infrastructure/Dockerfile.backend`

To run the deployment, navigate to the `infrastructure` folder and run `docker compose up --build`

## Backend

### REST Interface

#### /lectures

List the IDs of available lectures from the database.

The `/lecture/{lecture_id}` can be used to fetch details about the lecture.

Example Request:
```
GET /lectures
```

#### /lecture/{lecture_id}

List the lecture title and body content for a specific lecture.

Example Request:
```
GET /lecture/1
```

#### /lecture/create

Priveledged users may add new lectures to the database.

For authorization, a `token` must be passed in the request headers.

Example Request:
```
POST /lecture/create
HEADERS:
    Content-Type: application/json
    token: <secret>
BODY:
    {
        "title": "Introduction to C++, Unit 1: Primitive Data Type",
        "body": "Lorum Ipsumn ..."
    }
```