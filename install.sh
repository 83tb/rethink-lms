#!/bin/bash

wiringpi = 0

# if not rasapberry install Rethinkdb from repo
if [[ $(uname -m) != arm* ]]
then
    source /etc/lsb-release && echo "deb http://download.rethinkdb.com/apt $DISTRIB_CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list
    wget -qO- http://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add -
    sudo apt-get update
    sudo apt-get install rethinkdb
fi

sudo apt-get install python-pip supervisor python-dev
# pip install rethinkdb
sudo pip install rethinkdb pyserial bitstring tornado

# install and prepare GPIO support
if [[ $(uname -m) != arm* ] && $wiringpi]
then
    sudo pip install wiringpi2
    sudo usermod -a -G dialout $USER
fi

# Phrase, copy and symlink rethink and supervisord config files
#...
#... ;)
#...
