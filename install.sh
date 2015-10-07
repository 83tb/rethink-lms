#!/usr/bin/env bash
source /etc/lsb-release && echo "deb http://download.rethinkdb.com/apt $DISTRIB_CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list
wget -qO- http://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get install rethinkdb python-pip rabbitmq-server
pip install rethinkdb kombu
sudo rabbitmq-plugins enable rabbitmq_management
sudo service rabbitmq-server restart

