#! /bin/bash

source ~/.bash_profile

# INSTALL API DEPENDENCIES
sudo pip install -r requirements.txt

# INSTALL CANVAS && SHIELDS
npm install canvas
cd lib/SHIELDS
npm install