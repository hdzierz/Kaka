#!/bin/bash

source bin/activate

docker exec -it kaka_web_1  ./manage.py runscript load_from_config 
#--script-args=override


