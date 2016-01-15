# Warehouse Management System

## Installation

```
./install.sh


- git
- python-pip
- rehtink-lms repo
- wiringPi2 repo
- wiringPi2 python repo?
- pip install pyserial
- pip install bitstring
- pip install rethinkdb

- sudo apt-get install git rethinkdb python-pip python-dev supervisor
- sudo pip install pyserial bitstring rethinkdb tornado

# If running on raspberry You may wish to support GPIO, e.g. to hookup buttons
- sudo pip install wiringpi2
```

## Config
```

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

sudo ln -s $HOME/rethink-lms/ubuntu/supervisor/rethink-lms.conf /etc/supervisor/conf.d/rethink-lms.conf

sudo supervisorctl reread

sudo supervisorctl update

# Restart lms workers
sudo supervisorctl restart rethink-lms:*

```

## Rethink DB setup
Follow: http://rethinkdb.com/docs/start-on-startup/
when building from source on Raspberry, You may need to set more swap
https://www.bitpi.co/2015/02/11/how-to-change-raspberry-pis-swapfile-size-on-rasbian/
```
sudo adduser --system --quiet --group --no-create-home rethinkdb
sudo invoke-rc.d rethinkdb start
sudo update-rc.d rethinkdb defaults
sudo service rethinkdb start 
sudo service rethinkdb stop 

```

## Wiring Pi
 - http://wiringpi.com/
 - http://raspi.tv/how-to-install-wiringpi2-for-python-on-the-raspberry-pi#install
 - https://github.com/WiringPi/WiringPi2-Python
 - Disable tty console with raspi-config
 - add User to dialup group ```sudo usermod -a -G dialout $USER```

On Brix:
Edit: /etc/default/grub
```
# If you change this file, run 'update-grub' afterwards to update

# Uncomment to disable graphical terminal (grub-pc only)
#GRUB_TERMINAL=console
GRUB_TERMINAL=console

```
# To do
 - boot from system image
