#!/bin/bash

master=$1
PRIMARY_HOST=$2
PRIMARY_PORT=$3

if [ "${master}" == true ] ;  then
    mongod --master
else
    mongod --slave --source ${PRIMARY_HOST}:${PRIMARY_PORT}
fi
