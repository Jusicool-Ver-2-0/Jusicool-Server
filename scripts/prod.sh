#!/bin/sh

mkdir -p /ubuntu/home/prod/Jusicool-Server

cd /ubuntu/home/prod/Jusicool-Server

if [ ! -d ".git" ]; then
  git clone -b develop https://github.com/bigbroCO-team/bigbro_company_server .
else
  git pull origin develop
fi

docker build . -t jusicool-prod

docker stop jusicool-prod  || true
docker rm jusicool-prod || true

docker run -d --name jusicool-prod -p 3000:3000 jusicool-prod