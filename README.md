[![Build Status]https://travis-ci.org/Muchogo/Politico.svg?branch=develop](https://travis-ci.org/Muchogo/Politico)
[![Coverage Status](https://coveralls.io/repos/github/Muchogo/Politico/badge.svg)](https://coveralls.io/github/Muchogo/Politico)
[![Maintainability](https://api.codeclimate.com/v1/badges/93ca3eed08af43f26039/maintainability)](https://codeclimate.com/github/Muchogo/Politico/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/93ca3eed08af43f26039/test_coverage)](https://codeclimate.com/github/Muchogo/Politico/test_coverage)

# Politico
## Project Overview
The application is meant to help increase transparency and efficiency in the election process.

To view this site : https://github.com/Muchogo/Politico


## Technologies used.

* Python 3

* flask
* flask-restful

## [Pivotal Tacker Stories](https://www.pivotaltracker.com/n/projects/2242705)

## Current endpoints

| Method  | Endpoint  | Usage  |
|---|---|---|
|POST | api/v1/signup | Register a user.  |   
|POST | api/v1/login | Login a new user  |  
|POST | api/v1/parties  | Create a new party  |   
|GET| api/v1/parties| Get all the created parties|
|GET| api/v1/parties/ (partiesId) | Get a single party|
|PUT|	api/v1/parties/ (partiesId)/headquaters |	Update a single parties headquaters.|
|PUT|	api/v1/parties/(partiesId)/manifesto |	Update a single parties manifesto.|
|DELETE	| api/v1/parties/(partiesId)/manifesto	| Delete a single parties.|
|POST | api/v1/aspirants  | Create a new aspirants  |   
|GET| api/v1/aspirants| Get all the created aspirants|
|GET| api/v1/aspirants/ (aspirantsId) | Get a single aspirant|
|PUT|	api/v1/aspirants/ (aspirantsId)/parties |	Update a single aspirants parties.|
|PUT|	api/v1/aspirants/(aspirantsId)/memorandum |	Update a single aspirants memorandum.|
|DELETE	| api/v1/aspirants/(aspirantsId)/memorandum	| Delete a single aspirant.|
## Installation guide and usage

#### **Clone the repo.**
  ```
   $ git clone https://github.com/Muchogo/Politico
  ```

#### **Create virtual environment & Activate.**
  ```
   $ virtualenv env -p python3
   $ source venv/bin/activate
   ```
#### **Install Dependancies.**
  ```
    (env)$ pip3 install -r requirements.txt
  ```

#### **Run the app**
```
(venv)$ cd Politico/
```

On Linux set the enviroment variables for the project
```
(env)$ export FLASK_APP=run.py
(env)$ export FLASK_DEBUG=1
(env)$ export FLASK_ENV=development
(env)$ flask run
```

#### **Run Tests**

  ```
    (env)$ pytest --cov=tests
  ```