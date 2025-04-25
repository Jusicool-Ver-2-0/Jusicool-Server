#!/bin/sh

mkdir -p /home/ubuntu/stage/Jusicool-Server

cd /home/ubuntu/stage/Jusicool-Server

if [ ! -d ".git" ]; then
  git clone -b develop https://github.com/Jusicool-Ver-2-0/Jusicool-Server .
else
  git pull origin develop
fi

docker build . -t jusicool-stage

docker stop jusicool-stage  || true
docker rm jusicool-stage || true

docker run -d --name jusicool-stage --env-file /.stage.env --network jusicool -p 8000:8000 jusicool-stage