
# Bid Tracker

[![Build Status](https://travis-ci.com/rcmadruga/bid_tracker.svg?branch=master)](https://travis-ci.com/rcmadruga/bid_tracker)
[![Assertible status](https://assertible.com/tests/287735e8-a6cb-4bfa-bafa-2da1a4a9e700/status)](https://assertible.com/dashboard#/services/c50fc991-ceb0-4f86-a189-d60579d7b9fe/tests/287735e8-a6cb-4bfa-bafa-2da1a4a9e700)>

# Start of task

For a simple python backend system, a few libraries exists. Two of the most used ones are Flask and Django. 
Django is a full batteries included kind of solution. If you don't want face problems in the long run, it is better to design you solutions
according to Django-way. It seems like an overkill for a simple system as requested for this task.

Flask is a micro-framework, with lots of extensions to better suit our needs and desires. It gives us freedom to start simple and grow in complexity as the solution evolves.

Being mainly a REST API, I will use flask-restful to easyly map routes with resources

# Dev environment

Using pipenv to manage virtual environment to make it easier building/deploying later

# Database

não precisa, só uso direto na memória, mas qualquer outro sistema precisa de uma camada de persistência, adicionando uma biblioteca ORM (SQLAlchemy, marshmallow) nessa etapa

