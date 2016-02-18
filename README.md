[![Build Status](https://travis-ci.org/MicrowavedScrambledEggs/Kaka.svg?branch=mongosearch)](https://travis-ci.org/MicrowavedScrambledEggs/Kaka)

# Let the Kea Fly-integrating genotype storage with KEA

Kaka has three major aims:

- Provide a document based database to store genotype information like GBS results
- The database has to be decentrally distributable
- Continuous integration as well as unit testing techniques shall be used in order to make the deployment safer

## Techniques

Kaka has been developed using 
- Python 3.5
- The web framework Django 1.8. 
- Travis
- Docker
- PostGreSQL
- MongoDB

## How to run it

Clone github repo from (GitHub)[https://github.com/hdzierz/Kaka]

```
git clone https://github.com/hdzierz/Kaka
cd Kaka
```

then, either set up a primary (master) or a replica (slave) to connect to a kaka primary

To set up a primary:

```
bash env_setup.sh true
docker-compose build
docker-compose up -d
```

To set up a replica:

```
bash env_setup.sh false [host ip address of primary to connect to] [port of primary to connect to]
docker-compose build
docker-compose up -d
```

You might have to configure Kaka. Please look into (docker-compose.yml)[docker-compose.yml]. Please refer to the (docker compose)[https://docs.docker.com/compose/compose-file/].

## Configure PostGreSQL

Kaka has been configured for running it within the PFR infrastructure. The web servicie will cionnect to it internally so no configuration needed. In case you want to access the DB directly you might have to set the forwarded port to a different value (Change the first value (5434).

Also if not used with PFr you might want to set the proxy servers.

```
db:
  image: postgres
  volumes:
    - .:/dat
  ports:
    - "5434:5432"
  environment:
     - dummy:dummy
     - http_proxy:http://proxy.pfr.co.nz:8080
     - https_proxy:http://proxy.pfr.co.nz:8080
     - no_proxy:localhost,127.0.0.1,*.pfr.co.nz,::1
```

## Configure the web service


If outside PFR you would like to configure the proxy servers, forwarded port (change first number) and the volumes. Don't vchaneg any of the other configurations.

```
web:
  build: .
  dockerfile: Dockerfile_web
  command: python manage.py runserver 0.0.0.0:8000
  volumes:
    - .:/code
    - /input:/input
    - /output:/output
    - /workspace:/workspace
  ports:
    - "8000:8000"
  links:
    - db
  environment:
     - dummy:dummy
     - http_proxy:http://proxy.pfr.co.nz:8080
     - https_proxy:http://proxy.pfr.co.nz:8080
     - no_proxy:localhost,127.0.0.1,*.pfr.co.nz,::1
```

## How to use it

To use the web app: in a browser go to
```
[host address of kaka]/experimentsearch/
```

Logical operators that can be used in the text search fields are:
- '%' : wildcard
  - '%' : matches anything
  - '%[text]' : matches anything that ends in [text]
  - '[text]%' : matches anything that starts in [text]
  - '%[text]%' : matches [text] with anything either side of text
- whitespace : OR operator
- '+' : AND operator

To use the API to download a csv file listing all the experiments, go to
```
[host address of kaka]/api/experiments/csv/
```

To use the API to download a csv file listing all the data sources, go to
```
[host address of kaka]/api/data_source/csv/
```

To use the API to get experiment(s) data, go to
```
[host address of kaka]/api/genotype/?[GET query string]
```
The GET query string can contain the following queries:
- search_name=[experiment's name] : Queries experiments by name
- search_pi=[experiment's primary investigator] : Queries experiments by primary investigator
- from_date_day=[day as integer]&from_date_month=[month as integer]&from_date_year=[year as integer] : Matches experiments whose date created follows from_date
- to_date_day=[day as integer]&to_date_month=[month as integer]&to_date_year=[year as integer] : Matches experiments whose date created precedes to_date

Queries can be joined together using the character '&'

Logic operators (see above) can be used in the GET query string. Replace
- '%' with '%25'
- '+' with '%2B'
- whitespace with '+'

Example:
```
127.0.0.1:8000/api/genotype/?search_name=GBS+kiwi%25&search_pi=John%2BMcCallumn&from_date_month=1&from_date_day=1&from_date_year=2013&to_date_month=12&to_date_day=1&to_date_year=2016
```