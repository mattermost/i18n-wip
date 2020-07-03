#!/usr/bin/env bash

sed -i "s/SED_PROJECT/$1/g" /home/circleci/project/.circleci/webhook-data.json
curl -i -X POST -H 'Content-Type: application/json' \
     -d @/home/circleci/project/.circleci/webhook-data.json $2
