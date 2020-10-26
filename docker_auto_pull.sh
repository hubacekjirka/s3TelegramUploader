#!/bin/bash

set -e

# Change directory to the directory of the script ==> where docker-compose file is
cd "$(dirname "$0")"

echo "$(date +"%Y-%m-%d_%H-%M-%S") Scipt started" >> docker_auto_pull.log 2>&1

/usr/bin/docker pull hubacekjirka/s3-telegram-uploader:latest >> docker_auto_pull.log 2>&1

/usr/local/bin/docker-compose up -d --remove-orphans >> docker_auto_pull.log 2>&1

echo "$(date +"%Y-%m-%d_%H-%M-%S") Scipt finished" >> docker_auto_pull.log 2>&1
