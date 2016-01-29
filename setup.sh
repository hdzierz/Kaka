#!/bin/bash

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