#!/bin/bash

MONGODB=`ping -c 1 mongo | head -1  | cut -d "(" -f 2 | cut -d ")" -f 1`

echo "Waiting for startup.."
until curl http://${MONGODB}:28017/serverStatus\?text\=1 2>&1 | grep uptime | head -1; do
  printf '.'
  sleep 1
done

echo curl http://${MONGODB}:28017/serverStatus\?text\=1 2>&1 | grep uptime | head -1
echo "Started.."

echo SETUP.sh time now: `date +"%T"`

mongo --host ${MONGODB}:27017 <<EOF
   var cfg = {
        "_id": "rs",
        "version": 1,
        "members": [
            {
                "_id": 0,
                "host": "${MONGODB}:27017",
            }
        ]
   };
   rs.initiate(cfg, { force: true });
   rs.reconfig(cfg, { force: true });
EOF
