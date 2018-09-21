
# Bid Tracker

[![Build Status](https://travis-ci.com/rcmadruga/bid_tracker.svg?branch=master)](https://travis-ci.com/rcmadruga/bid_tracker)
[![Assertible status](https://assertible.com/apis/c50fc991-ceb0-4f86-a189-d60579d7b9fe/status)](https://assertible.com/dashboard#/services/c50fc991-ceb0-4f86-a189-d60579d7b9fe/results)

For a simple python backend system, a few libraries exist. Two of the most used ones are Flask and Django.
Django is a full battery included kind of solution. If you don't want to face problems in the long run, it is better to design your solutions
according to Django-way. It seems like an overkill for a simple system as requested for this task.

Flask is a micro-framework, with lots of extensions that better suit our initial needs. It gives us a freedom to start simple and grow in complexity as the solution evolves.

Being a REST API, I will use flask-restful to easily map routes with resources and parameters.

## Development environment

We need a complete overview of the software life cycle to select our libs and frameworks to make things easy and portable. Knowing that any system must have automated build, tests and deployment, we will structure our dev environment using pipenv. According to its docs:

> (pipenv) It automatically creates and manages a virtualenv for your projects, as well as adds/removes packages from your Pipfile as you install/uninstall packages. It also generates the ever-important Pipfile.lock, which is used to produce deterministic builds.

This way the code is easily ported to run in any OS and cloud environment.

During development, Postman was used to test the API. A collection of all requests was generated for easier sharing: `bid_tracker.postman_collection.json`. Another tool used to help API design was Swagger/OpenAPI, integrated directly in code via [flasgger](http://flasgger.pythonanywhere.com). This enables a direct comment on each route making the API self-documenting. The SwaggerUI page is reached at [http://localhost:5000/apidocs](http://localhost:5000/apidocs), enabling live testing and interaction with the API. Another advantage of this integration, is that a client code generator could be used to create clients to consume this API in various languages.

![SwaggerUI](/docs/swagger.png?raw=true "SwaggerUI")

## Git and Continous Integration Support

This repository is hosted on GitHub. Every commit trigger a TravisCI build pipeline for testing. API test is handled by Assertible, triggered by a build pipeline script. Visit `.travis.yml` for more information.

- Github: [https://github.com/rcmadruga/bid_tracker](https://github.com/rcmadruga/bid_tracker)
- TravisCI: [https://travis-ci.com/rcmadruga/bid_tracker](https://travis-ci.com/rcmadruga/bid_tracker)
- Assertible: [https://assertible.com/dashboard#/services/c50fc991-ceb0-4f86-a189-d60579d7b9fe](https://assertible.com/dashboard#/services/c50fc991-ceb0-4f86-a189-d60579d7b9fe). Not public, get in touch to request access.

![Assertible](/docs/Assertible.png?raw=true "Assertible")

## Installation

To install use the following steps:

- Extract ZIP or clone git repository
- `pip install pipenv`
- `pipenv install`
- `python api.py`
- Access `http://localhost:5000/apidocs` to test and play with API

## Production

Being a more Proof of Concept kind of task, the embedded server available in Flask will be enough for the development phase. While lightweight and easy to use, Flask’s built-in server is not suitable for production as it doesn't scale well and by default serves only one request at a time.

For a robust and fast production solution, the stack would also have a dedicated application server that supports WSGI (Web Server Gateway Interface) such as gunicorn, and a dedicated web server such as Nginx on top.

Another option would be hosting this flask app in a PaaS offering, such as Google's AppEngine.

A container/kubernetes solution should also be investigated, using its power and flexibility to scale dinamically on a larger field.

## Database

In this example, the data is being used in memory for fast access and easy initial development speed. Going forward, a proper persistent layer must be used. The data is mainly relational, as resources have 0-N relations with each other. A ORM library such as SQLAlchemy should be used to help this issue. A proven RDMS as Postgres, MySQL or a managed cloud database should be used. Another library that could be used to make the integration with database easily is marshmallow, a great library for data formatting and schema validation.

## User Authentication and Authorization

A proper user management system should be used. Integrated with OAuth provider according to the userbase. For example: with GitHub/BitBucket/GitLab if tech inclined or Google/Facebook/Twitter if more general userbase.

## Security

Flask protects us against one of the most common security problems of modern web applications: cross-site scripting (XSS). But there are many more ways to cause security problems.
Flask is no different from any other framework in that we must build with caution, watching for exploits when building to your requirements. Any system, especially ones available on the web is at risk of exploiting by malicious agents. One kind of attack that an API must be secure is DDOS, in which a distributed attack with legit requests renders the servers unavailable for all clients. It could me mitigated with rate-limiting the access to API acording to IP, by example.

## Logging and metrics

The solution should have a proper logging structure in place. Ideally, forwarding the logs to a central logging system that analyzes and notify a operation engineer in case of failures and lower performance. One app that is becomming the _defacto_ solution for API metrics is Prometheus. It should be levered to measure API performance and generate insights about runnning this app in production.
