#!/bin/sh

mkdir -p /ubuntu/home/stage/Jusicool-Server

cd /ubuntu/home/stage/Jusicool-Server

if [ ! -d ".git" ]; then
  git clone -b develop https://github.com/bigbroCO-team/bigbro_company_server .
else
  git pull origin develop
fi

docker build . -t jusicool-stage

docker stop jusicool-stage  || true
docker rm jusicool-stage || true

docker run -d --name jusicool-stage -p 8000:8000 jusicool-stage