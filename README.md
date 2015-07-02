# Warehouse Management System

## Installation

```
./install.sh
```

## Running

```
./run.sh
```

## Basic data import and index creation

```
./data_generator.py
```

## Endpoints
```
/lamps -> CRUD API, REST 100%
/feed/lamps -> Listening for changes in the engine, useful for handling server->client communication
```
## What's the port for now?
```
8888, 127.0.0.1:8888 or 10.1.2.55:8888
```


## Where should client/interface go?
```
templates/index.html
```
## Accessing database

If you need to access database for debuging purposes, web admin is here

```
http://127.0.0.1:8080 or http://10.1.2.55:8080
```

## Supervisord
```
sudo apt-get install -y supervisor

sudo ln -s ~/rethink-lms/supervisor/rethink-lms.conf /etc/supervisor/conf.d/rethink-lms.conf

sudo supervisorctl reread

sudo supervisorctl update
```

## Rethink DB setup
Follow: http://rethinkdb.com/docs/start-on-startup/
```
sudo update-rc.d service_name defaults
```