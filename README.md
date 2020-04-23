# Test BLVO


Application for data consumption for different dating sites

## Getting Started

To have a copy of the repository on your machine we must clone the repository

* Clone repository
```ssh
    git clone git@github.com:pollitosabroson/test-blv.git
```

### Prerequisites

Make sure that you have met the following prerequisites before continuing with this tutorial.

* Logged in as a user with sudo privileges or Admin user for MAC.
* Have [Docker](https://docs.docker.com/install/) installed

### Installing

To install the project, we must access the docker folder, after the environment we are going to execute, in this case it is the one of dev and we execute the following commands.

* access folder
```ssh
  cd test-blv/docker/dev
```
* Create dockers
```ssh
  docker-compose build --no-cache --force-rm
```
* Run dockers
```ssh
  docker-compose up -d
```
* Apply migrations
```ssh
  docker exec -it api_dev_api-belvo_1 python manage.py migrate
```

* Access

    * API: [localhost:8091](http://localhost:8091/)

### Endpoints

- Users
    - Create users
        -  http://localhost:8091/api/v1/users/
    - List Users
        - http://localhost:8091/api/v1/users/
    -  List transactions for users
        -  http://localhost:8091/api/v1/users/{user_id}/transactions
- Transactions
    - Create Multiple transactions
        - http://localhost:8091/api/v1/transactions/
    - Transaction category
        - http://localhost:8091/api/v1/transactions/users/{user_id}/category
    - Summary transaction for users
        - http://localhost:8091/api/v1/transactions/users/{user_id}
    - Summary transaction for users range darte
        - http://localhost:8091/api/v1/transactions/users/{user_id}?r_d_date=2020-01-01,2020-01-30
            - Filter the summary by a date range in the date format "YYYY-MM-DD", the range must be in the following format:
            - from_date, to_date
            - from_date,
            - to_date,
            - examples:
                - r_d_date = 2020-01-01,2020-01-30
                - r_d_date = 2020-01-01,
                - r_d_date =, 2020-01-30


## Running the tests

To run the tests just execute them via docker exec
* API
```ssh
  docker exec -it api_dev_api-belvo_1 pytest -v
```

## Project scaffolding

- Coreapi
    - Core
        - Application that manages functions that are used in multiple applications
    - Transaction
        - Application to manage all user Transactions
    - Users
        - Application to manage all user
- Docker
    - Dev
        - All configs for development

## Features

### Transactions
* Create Transaction.
* Filter transactions

### Users

* Create useres
* List users
