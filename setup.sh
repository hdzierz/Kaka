#!/bin/bash

# Based on https://github.com/soldotno/elastic-mongo/blob/master/scripts/setup.sh

MONGODB=`ping -c 1 mongo | head -1  | cut -d "(" -f 2 | cut -d ")" -f 1`

echo "Waiting for startup.."
until curl http://${MONGODB}:28017/serverStatus\?text\=1 2>&1 | grep uptime | head -1; do
  printf '.'
  sleep 1
done

echo curl http://${MONGODB}:28017/serverStatus\?text\=1 2>&1 | grep uptime | head -1
echo "Started.."

echo SETUP.sh time now: `date +"%T"`

master= true
primary= false

read -p "Is this a primary set up? (y/n): "
[ "$REPLY" != "y" ] || master= "$primary"

if [ "$master" ] ;  then
   mongo --host ${MONGODB}:27017 <<EOF
       var cfg = {
            "_id": "rs",
            "version": 1,
            "members": [
                {
                    "_id": 0,
                    "host": "${MONGODB}:27017",
                    "priority": 50,
                }
            ]
       };
       rs.initiate(cfg, { force: true });
       rs.reconfig(cfg, { force: true });
    EOF
else
    echo "Please enter the host of Kaka's database primary: "
    read PRIMARY

    mongo --host ${PRIMARY}:27017 <<EOF
       rs.add("${MONGODB}:27017");
    EOF
fi